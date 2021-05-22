
useradd -m -p 'Minitel' -G sudo 'Minitel'
cd '/home/Minitel'
git clone 'https://github.com/Pixelbo/Minitel-raspi'
cd 'Minitel-raspi'
git clone 'https://github.com/paullouisageneau/PyMinitel'
cd 'PyMinitel'
python3 setup.py install
cd ..
pip3 install pyserial

rm -r PyMinitel
sed -i '$d' /etc/rc.local
echo '/home/Minitel/Minitel-raspi/Source/init.py ttyUSB0'>> /etc/rc.local  # Minitel initialization
echo '/home/Minitel/Minitel-raspi/Source/tty.py ttyUSB0 Minitel & '>> /etc/rc.local  # Minitel terminal converter
echo 'exit 0' >>/etc/rc.local 

echo 'export LANG=fr_FR.iso88591'>> /home/Minitel/.bashrc
tic "/home/Minitel/Minitel-raspi/Source/term.ti"
