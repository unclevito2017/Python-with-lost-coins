import subprocess
import time
import os
import pickle
import random
import psutil

Tips = 'bc1qus09g0n5jwg79gje76zxqmzt3gpw80dcqspsmm'

# Function to save the checkpoint
def save_checkpoint(start_keyspace, end_keyspace):
    checkpoint_data = {
        'start_keyspace': start_keyspace,
        'end_keyspace': end_keyspace
    }
    with open('checkpoint.pkl', 'wb') as f:
        pickle.dump(checkpoint_data, f)

# Function to load the checkpoint
def load_checkpoint():
    if os.path.exists('checkpoint.pkl'):
        try:
            with open('checkpoint.pkl', 'rb') as f:
                checkpoint_data = pickle.load(f)
            return checkpoint_data['start_keyspace'], checkpoint_data['end_keyspace']
        except EOFError:
            print("Checkpoint file is corrupted. Starting from default keyspace values.")
            os.remove('checkpoint.pkl')
            return '20000000000000000', '20100000000000000'
    else:
        return '20000000000000000', '20100000000000000'

# Function to delete the checkpoint
def delete_checkpoint():
    if os.path.exists('checkpoint.pkl'):
        os.remove('checkpoint.pkl')

def run_lostcoins(start_keyspace, end_keyspace, k):
    output_filename = f'{start_keyspace[:3]}.txt'  # Generate the output filename based on the start keyspace
    command = f'LostCoins.exe -t 0 -g -i 0 -x 256,256 -k 3 -f 66-9.bin -r 1 -s {start_keyspace} -z {end_keyspace} -d 4 -n 5'

    process = subprocess.Popen(command, shell=True)
    time.sleep(220)  # Wait for 220 seconds

    # Use psutil to terminate the process tree
    parent = psutil.Process(process.pid)
    for child in parent.children(recursive=True):
        child.terminate()
    parent.terminate()
    process.wait()  # Wait for the process to exit

# Load the checkpoint if it exists, otherwise start from the beginning
start_keyspace, end_keyspace = load_checkpoint()

# Loop until explicitly interrupted
last_save_time = time.time()  # Track the last save time
save_interval = 60  # Save interval in seconds (1 minute)
iteration_counter = 0
k = 14  # Initial value of k

while True:
    try:
        increment = ''.join(random.choices('123456789ABCDEF', k=k))  # Generate a random hexadecimal value
        log_entry = f"Iteration {iteration_counter}: Random Increment: {increment}, k={k}\n"
        
        # Write log entry to file and flush the buffer
        with open('output.log', 'a') as log_file:
            log_file.write(log_entry)
            log_file.flush()
        
        print(log_entry, flush=True)  # Display the randomly chosen increment in console
        
        start_keyspace = start_keyspace[:-len(increment)] + increment  # Append the increment to the right side of the start keyspace

        # Calculate the new end keyspace, making sure it does not exceed the maximum value
        new_end_keyspace = hex(int(start_keyspace, 16) + int(increment, 16) - 1)[2:]
        end_keyspace = min(new_end_keyspace, '3ffffffffffffffff')  # Choose the smaller value between the new end keyspace and the maximum value

        run_lostcoins(start_keyspace, end_keyspace, k)
        start_keyspace = hex(int(end_keyspace, 16) + 1)[2:]

        # Save the checkpoint every minute
        current_time = time.time()
        elapsed_time = current_time - last_save_time
        if elapsed_time >= save_interval:
            save_checkpoint(start_keyspace, end_keyspace)
            last_save_time = current_time

        time.sleep(2)  # Wait for 2 seconds before restarting

        # Increment the iteration counter
        iteration_counter += 1

        # Update k based on iteration_counter
        if iteration_counter % 3 == 0:
            k = 15
        else:
            k = 14

        # Check if we've reached the end of the keyspace
        if int(start_keyspace, 16) > int('3ffffffffffffffff', 16):
            delete_checkpoint()  # Call the delete_checkpoint function
            start_keyspace, end_keyspace = '20000000000000000', '3ffffffffffffffff'  # Reset the keyspaces

    except KeyboardInterrupt:
        save_checkpoint(start_keyspace, end_keyspace)  # Save the checkpoint if interrupted by KeyboardInterrupt
        break
    except Exception as e:
        # Log any unexpected exceptions
        with open('error.log', 'a') as error_file:
            error_file.write(f"Unexpected error: {str(e)}\n")
        print(f"Unexpected error: {str(e)}", flush=True)
