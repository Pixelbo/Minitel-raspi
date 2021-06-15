pkill -f "bash -c export TERM='m1b-x80'; export LANG='fr_FR.iso88591'; while true; do clear; cd '/home/Minitel'; runuser -l 'Minitel'; sleep 1; done"
pkill -f "python3 /home/Minitel/Minitel-raspi/Minitel_related/tty.py ttyUSB0 Minitel"
pkill -f "runuser -l Minitel"