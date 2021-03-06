
useradd -m -p 'Minitel' -G sudo 'Minitel'
cd '/home/Minitel'

git clone 'https://github.com/Pixelbo/Minitel-raspi'
cd 'Minitel-raspi'

git clone 'https://github.com/paullouisageneau/PyMinitel'
cd 'PyMinitel'
python3 setup.py install
cd ..
rm -r PyMinitel

pip3 install -r requirements.txt

echo 'export LANG=fr_FR.iso88591'>> /home/Minitel/.bashrc
echo 'cd /home/Minitel/Minitel-raspi/Project/'>> /home/Minitel/.bashrc #comment this line if u don't want the project at startup
echo './Main.py' >> /home/Minitel/.bashrc
sudo tic "/home/Minitel/Minitel-raspi/Minitel_related/term.ti"
