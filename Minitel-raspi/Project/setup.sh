cd "/home/Minitel/Minitel-raspi/Project/"
git clone "https://github.com/Pixelbo/PyLMS"
cd PyLMS
python3 setup.py install
cd ..
rm -R PyLMS

pip3 install whiptail