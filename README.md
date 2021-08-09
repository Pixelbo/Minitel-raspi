
# Minitel-Raspi
<details open="open">
  <summary>Chapters</summary>
  <ol>
    <li>
      <a href="#About-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#auto-installation">Automatic Installation</a></li>
        <li><a href="#man-installation">Manual Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#HELP!">HELP!</a></li>
  </ol>
</details>

# About-the-project

Minitel-Raspi is a project that reunites the famous french Minitel and the famous Raspberry Pi.
This project did not modify the Minitel, I used the external serial port for printing into the screen.
Originaly begun in 2020 this project is driven by a kid, so go easy on me, I can't use github proprely.

# Getting Started
## Prerequisites

 - For this project we obviously need a Minitel, I use the Minitel 2B;
   other Minitel works probably fine but I havn't tested yet. 
   
 - We need
   also a Raspberry Pi; I use the model 2B. It's better to have a wi-fi
   connection for this because it's impossible to work directly with the
   Minitel (slow frame-rate). 
   
 - For the conversion from the Raspi to the
   Minitel, you will need a FTDI USB to serial UART converter, it need
   to be at 3.3V; If you don't have this, I suggest you to take a look
   at the HELP! chapter.

-Finally the communication will not be wireless, so you will need a wire; the minitel has a back DIN socket serial port (for more information see HELP!)

##  Automatic Installation

Ok so you have everything and you want of course a terminal on your Minitel!

Lucky for you, I've made an automatic setup that will do everything for you!

Just download the `setup.sh` in the releases and execute it in sudo mode;
 
**!!!!NEVER execute it twice, it will break everything; if there was an error during installation, report to te Manual Installation!!!**

The installation process will do various things that is explained just below.

![Installation diagram](https://raw.githubusercontent.com/Pixelbo/Minitel-raspi/main/Installation%20Diagram.png)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEwMjU1ODY0ODVdfQ==
-->