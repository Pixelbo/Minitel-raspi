# Minitel-Raspi
![Dat minitel](https://raw.githubusercontent.com/Pixelbo/Minitel-raspi/main/minitel.jpg)

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
        <li><a href="#Automatic-Installation">Automatic Installation</a></li>
        <li><a href="#Manual-Installation">Manual Installation</a></li>
        <li><a href="#Finishing-Installation">Finishing Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#help">HELP!</a></li>
  </ol>
</details>

# About-the-project

Minitel-Raspi is a project that reunites the famous french Minitel and the famous Raspberry Pi.

I've created a small gui with whiptail that control for now the  Logitec Music Server.
I need to think about another API ; Ths is the main project
It uses the Telnet protocol that is enabled in the LMS settings, you can see he docs <a href="https://github.com/elParaguayo/LMS-CLI-Documentation/blob/master/LMS-CLI.md">here</a>

This project did not modify the Minitel, I used the external serial port for printing into the screen.

Originaly begun in 2020 this project is driven by a kid, so go easy on me, I can't use github proprely.


# Getting Started
## Prerequisites

 - For this project we obviously need a Minitel, I use the Minitel 1B;
   other Minitel works probably fine but I havn't tested yet. 
   
 - We need
   also a Raspberry Pi; I use the model 2B. It's better to have a wi-fi
   connection for this because it's impossible to work directly with the
   Minitel (slow frame-rate). 
   
 - For the conversion from the Raspi to the
   Minitel, you will need a FTDI USB to serial UART converter, it need
   to be at 3.3V; If you don't have this, I suggest you to take a look
   at the <a href="#HELP!">HELP!</a> chapter.

-Finally the communication will not be wireless, so you will need a wire; the minitel has a back DIN socket serial port (for more information see <a href="#HELP!">HELP!</a>)

##  Automatic Installation

Ok so you have everything and you want of course a terminal on your Minitel!

Lucky for you, I've made an automatic setup that will do everything for you!

Just download the `setup.sh` in the releases and execute it in sudo mode;
 Go to <a href="#fin-installation">Finishing Installation</a> for finishing the installation!
**!!!!NEVER execute it twice, it will break everything; if there was an error during installation, report to te Manual Installation!!!**

The installation process will do various things that is explained just below.

![Installation diagram](https://raw.githubusercontent.com/Pixelbo/Minitel-raspi/main/Installation%20Diagram.png)
## Manual Installation

So you want to do it manually, ok no problem;

1. First of all we need to create the user Minitel:

```bash
useradd -m -p 'Minitel' -G sudo 'Minitel'
cd '/home/Minitel
```

2. Then we need to clone this repo:
  
  ```bash
git clone 'https://github.com/Pixelbo/Minitel-raspi'
cd 'Minitel-raspi'
```

3. The PyMinitel Library is essential to this project:
  ```bash
git clone 'https://github.com/paullouisageneau/PyMinitel'
cd 'PyMinitel'
python3 setup.py install
cd ..
rm -r PyMinitel
```

4. Finally we install pyserial and do various QoL things:

  ```bash
pip3 install pyserial
echo 'export LANG=fr_FR.iso88591'>> /home/Minitel/.bashrc
echo 'cd /home/Minitel/Minitel-raspi/Project/'>> /home/Minitel/.bashrc #comment this line if u don't want the project at startup
echo './Main.py' >> /home/Minitel/.bashrc
sudo tic "/home/Minitel/Minitel-raspi/Minitel_related/term.ti"
```

<a href="#fin-installation">Finishing Installation</a>

## Finishing Installation

Ok you're not entirely set for now, you need to maybe change the baudrate depending on your Minitel version.

For changing the baudrate, you need to edit two files:

<a href="/Minite_related/init.py#L8">init.py</a>, At line 8, there is the baudrate var; default is 4800 baud.

and <a href="/Minite_related/tty.py#L25">tty.py</a>, At line 25, there is the baudrate var; default is 4800 baud.

Here is the table for the baudrates:

|Minitel Version| Badurate |
|--|--|
| 1 | 1200 |
|1B|4800|
|2|9600|

# Usage

Ok everything about the Minitel is in the folder Minitel_relted:

If you want to Startup the proces for the Minitel; execute <a href="/Minitel_related/Startup.sh">Startup.sh</a>
If you want to Shutdown the proces for the Minitel; execute <a href="/Minitel_related/Shutdown.sh">Shutdown.sh</a>

If you want that it does it automaticly, you will need more wiring:

TODO

# Roadmap

 - [x] Minitel <=> communication
 - [ ] Proper key input with the special keyboard
 - [ ] Proper Setup.sh
 - Project:
 - [x] Whiptail with python
 - [x] Main Menu
 - [x] LMS control
 - [ ] adding translation
 - [ ] testing 
 - [ ] another API

# Contributing

You're free to contribute !
Just do some issues and some pull requests;
You can also fork this repo !

Beware of the licenses that you'll use!

# License

See <a href="LICENSE">License</a>

# Contact

E-mail: pixelbo21@gmail.com

# HELP!

Ok you need help;

there are the options:

 - Hardware help: 
	- https://chapelierfou.org/blog/a-minitel-as-a-linux-terminal.html
	- https://chapelierfou.org/blog/a-minitel-2.0.html
	
-Permission denied:
	

    sudo chmod -R 777 Minitel-raspi
If this don't work, see if your drive have the exec flag

- Not working:
  The tab "issues" at GitHub is very useful!
	
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTMzMTE2MTMwOF19
-->
