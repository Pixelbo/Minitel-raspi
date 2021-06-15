#! /bin/sh

echo ============================== Report v1.2 Start ==============================  > /tmp/sqlog.txt 2>&1
echo --------------- Linux version:  ---------------  >> /tmp/sqlog.txt 2>&1
UNAMEOUTPUT=$(uname -a)
[ -f /etc/os-release ] && OS_PRETTY_NAME=$(cat /etc/os-release | grep PRETTY_NAME)
[ -f /etc/os-release ] && OS_RELEASE=$(cat /etc/os-release | grep VERSION=)
[ -f /usr/share/doc/tc/release.txt ] && OS_RELEASE=$(cat /usr/share/doc/tc/release.txt; echo;)
PI_MODEL=$(cat  /proc/device-tree/model; echo;)

echo "uname info:" $UNAMEOUTPUT >> /tmp/sqlog.txt 2>&1
[ -n "$OS_PRETTY_NAME" ] && echo "os pretty name:" $OS_PRETTY_NAME >> /tmp/sqlog.txt 2>&1
echo "os release:" $OS_RELEASE >> /tmp/sqlog.txt 2>&1
echo "pi model:" $PI_MODEL >> /tmp/sqlog.txt 2>&1

echo --------------- Hostname: ---------------   >> /tmp/sqlog.txt 2>&1
cat /etc/hostname  >> /tmp/sqlog.txt 2>&1
cat /etc/hosts | grep 127.0.1.1  >> /tmp/sqlog.txt 2>&1

echo --------------- Squeezelite: ---------------  >> /tmp/sqlog.txt  2>&1
ls -l /usr/bin/squee*  >> /tmp/sqlog.txt  >> /tmp/sqlog.txt 2>&1
echo --------------- Squeezelite daemon script: ---------------   >> /tmp/sqlog.txt 2>&1
ls -l /etc/init.d/*squee*  >> /tmp/sqlog.txt 2>&1
echo --------------- Squeezelite init.d daemon settings: ---------------   >> /tmp/sqlog.txt 2>&1
ls -l /etc/rc*.d/*squeeze*  >> /tmp/sqlog.txt 2>&1
echo --------------- Squeezelite systemd status: ---------------   >> /tmp/sqlog.txt 2>&1
sudo systemctl status  -l squeezelite.service >> /tmp/sqlog.txt 2>&1

echo --------------- List sound devices: ---------------   >> /tmp/sqlog.txt 2>&1
sudo /usr/bin/squeezelite-armv6hf -l  >> /tmp/sqlog.txt 2>&1

echo --------------- Squeezelite daemon script settings: ---------------   >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_SOUNDCARD=  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_NAME=\"  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_ALSA_PARAMS=  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_MAC_ADDRESS=\"  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SB_SERVER_IP=  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_LOGFILE=  >> /tmp/sqlog.txt 2>&1
cat /usr/local/bin/squeezelite_settings.sh | grep SL_LOGLEVEL=  >> /tmp/sqlog.txt 2>&1

echo --------------- Squeezelite running? : ---------------   >> /tmp/sqlog.txt 2>&1
ps -A |grep squeeze  >> /tmp/sqlog.txt 2>&1
  
echo --------------- Restart-at-night job? : ---------------   >> /tmp/sqlog.txt 2>&1
crontab -u pi -l | grep shutdown  >> /tmp/sqlog.txt 2>&1
echo ============================== Report End ==============================  >> /tmp/sqlog.txt 2>&1

cat /tmp/sqlog.txt

