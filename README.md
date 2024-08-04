# Python-with-lost-coins<br>
pip3 install psutil<br>
python3 lost-coins-psutil.py<br>
Do not use cpu and gpu together. Slower speed<br>
Twice as fast as bitcrack<br>
Time sleep controls increment running time currently set to 180 seconds<br>
K= value sets the increment value k=15 approx 59 bit, k=14 approx 56 bit, k-13 approx 31 bit etc. random value  selection<br>
Usage: LostCoins [options...]
Options:
    -v, --version          Print version.<br>
    -c, --check            Check the working of the code LostCoins<br>
    -u, --uncomp           Search only uncompressed addresses<br>
    -b, --both             Search both (uncompressed and compressed addresses)<br>
    -g, --gpu              Enable GPU calculation<br>
    -i, --gpui             GPU ids: 0,1...: List of GPU(s) to use, default is 0<br>
    -x, --gpux             GPU gridsize: g0x,g0y,g1x,g1y, ...: Specify GPU(s) kernel gridsize, default is 8*(MP number),128<br>
    -t, --thread           ThreadNumber: Specify number of CPUs thread, default is number of core<br>
    -o, --out              Outputfile: Output results to the specified file, default: Found.txt<br>
    -m, --max              -m  1-10000 For GPU: Reloads random started hashes every billions in counter. Default: 100 billion<br>
    -s, --seed             PassPhrase   (Start bit range)<br>
    -z, --zez              PassPhrase 2 (End bit range)<br>
    -e, --nosse            Disable SSE hash function<br>
    -l, --list             List cuda enabled devices<br>
    -r, --rkey             Number of random modes<br>
    -n, --nbit             Number of letters and number bit range 1-256<br>
    -f, --file             RIPEMD160 binary hash file path<br>
    -d, --diz              Display modes -d 0 [info+count], -d 1 SLOW speed [info+hex+count], Default -d 2 [count] HIGH speed<br>
    -k, --color            Text color: -k 1-255 Recommended 3, 10, 11, 14, 15 (default: -k 15)<br>
    -h, --help             Shows this page<br>
