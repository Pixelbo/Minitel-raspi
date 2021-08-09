#!/bin/bash
 
waitButton ()
{

while [ ` gpio -g read 7` = 0 ]; do
        echo  "Minitel OFF!"
        
        if [ $x = 1 ]; then
          echo "Minitel Shutdown!"
          x=0
          sleep 5
          sudo sh "/home/Minitel/Minitel-raspi/Minitel_related/Shutdown.sh" 
        fi
        
        sleep 1
done

echo "Minitel ON!"

if [ $x = 0 ]; then
  echo "Minitel Startup!"
  x=1
  sleep 5
  sudo sh "/home/Minitel/Minitel-raspi/Minitel_related/Startup.sh" 
fi

sleep 1
#gpio -g read 7 > /home/pi/etat
}
 
x=0 

while true; do
waitButton
done