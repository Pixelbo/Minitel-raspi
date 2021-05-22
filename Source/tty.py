#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

"""
Minitel 1B terminal converter
Copyright (C) 2016 Paul-Louis Ageneau
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os, subprocess, ctypes

port = sys.argv[1] if len(sys.argv) >= 2 else 'ttyUSB0'
user = sys.argv[2] if len(sys.argv) >= 3 else 'pi'
minitel = '/dev/'+port
term = 'm1b-x80'
lang = 'fr_FR.iso88591'
baudrate = 4800

# Character output conversion table
conv = {}

for i in range(0xC0, 0xC6):
    conv[i] = b'A'
for i in range(0xC8, 0xCC):
    conv[i] = b'E'
for i in range(0xCC, 0xD0):
    conv[i] = b'I'
for i in range(0xD2, 0xD7):
    conv[i] = b'O'
for i in range(0xD9, 0xDD):
    conv[i] = b'U'
for i in range(0xE0, 0xE6):
    conv[i] = b'a'
for i in range(0xE8, 0xEC):
    conv[i] = b'e'
for i in range(0xEC, 0xF0):
    conv[i] = b'i'
for i in range(0xF2, 0xF7):
    conv[i] = b'o'
for i in range(0xF9, 0xFD):
    conv[i] = b'u'

conv[0xC6] = b'AE'
conv[0xC7] = b'C'
conv[0xD0] = b'D'
conv[0xD1] = b'N'
conv[0xD7] = b'*'
conv[0xD8] = b'O'
conv[0xDD] = b'Y'
conv[0xDE] = b'TH'
conv[0xDF] = b'ss'
conv[0xE6] = b'ae'
conv[0xE7] = b'c'
conv[0xF0] = b'd'
conv[0xF1] = b'n'
conv[0xF7] = b'/'
conv[0xF8] = b'o'
conv[0xFD] = b'y'
conv[0xFE] = b'th'
conv[0xFF] = b'y'

conv[0xA0] = b' '  # non-breakable space
conv[0xA2] = b'c'  # cent sign
conv[0xA3] = b'L'  # pound sterling sign
conv[0xA5] = b'Y'  # yen sign
conv[0xAB] = b'"'  # opening guillemet
conv[0xBB] = b'"'  # closing guillemet
conv[0xAC] = b'-'  # negation sign
conv[0xB2] = b'^2' # square sign
conv[0xB3] = b'^3' # cube sign
conv[0xB9] = b'^1'

# Windows-1252 specific
conv[0x80] = b'E'  # euro sign
conv[0x8C] = b'OE'
conv[0x9C] = b'oe'

# ISO-8859-15 specific
conv[0xA4] = b'E'  # euro sign
conv[0xA6] = b'S'
conv[0xA8] = b's'
conv[0xB4] = b'Z'
conv[0xB8] = b'z'
conv[0xBC] = b'OE'
conv[0xBD] = b'oe'
conv[0xBE] = b'Y'

# Special characters
conv[0xE0] = b'\x0E\x40\x0F' # small a grave
conv[0xE8] = b'\x0E\x7D\x0F' # small e grave
conv[0xE9] = b'\x0E\x7B\x0F' # small e acute
conv[0xF9] = b'\x0E\x7C\x0F' # small u grave
conv[0xE7] = b'\x0E\x5C\x0F' # small c cedilla
conv[0xB0] = b'\x0E\x5B\x0F' # degree sign
conv[0xBA] = b'\x0E\x5B\x0F' # ordinal indicator
conv[0xA3] = b'\x0E\x23\x0F' # pound sterling sign
conv[0xA7] = b'\x0E\x5D\x0F' # section sign

# Special keys (0x13) conversion table
buttons = {}
buttons[0x41] = b'\x0D' # ENVOI
buttons[0x42] = b'\x1B' # RETOUR
buttons[0x43] = b'\x1BOS' # REPETITION
buttons[0x44] = b'\x1BOm' # GUIDE
buttons[0x45] = b'\x18' # ANNULATION
buttons[0x46] = b'\x1BOP' # SOMMAIRE
buttons[0x47] = b'\x08' # CORRECTION
buttons[0x48] = b'\x0D' # SUITE

# Open a TTY for the user shell
master, slave = os.openpty()
ttyname = os.ttyname(slave)
os.chmod(ttyname, 0o666)
print(ttyname)

# Configure the TTY to the Minitel
os.system('stty -F "{}" {} istrip cs7 parenb -parodd brkint \
ignpar icrnl -ixon ixany -opost cread hupcl isig cbreak min 1 \
-echo echoe echok'.format(minitel, baudrate))

# Run a shell for the specified user
libc = ctypes.CDLL('libc.so.6')
p = subprocess.Popen(['bash', '-c', 'export TERM=\'{}\'; export LANG=\'{}\'; while true; do clear; cd \'{}\'; runuser -l \'{}\'; sleep 1; done'.format(term, lang, '/home/'+user, user)], stdin=slave, stdout=slave, stderr=slave, bufsize=0, preexec_fn=libc.setsid)

pid = os.fork()
if pid:
    w = os.fdopen(master, 'wb', 0)
    r = open(minitel, 'rb', 0)
    while 1:
        c = r.read(1)
        #print(c)
        if len(c) == 0:
            break
        if ord(c) == 0x03 or ord(c) == 0x18: # divert ctrl-C and ctrl-X and send SIGINT
            try:
                fgid = int(subprocess.check_output(['ps', 'h', '-t', ttyname, '-o', 'tpgid']).decode(sys.stdout.encoding).split('\n')[0])
                subprocess.call(['kill', '-INT', '-'+str(fgid)])
            except Exception as e:
                print(e)
            continue
        elif ord(c) == 0x13: # Special buttons in mixed mode
            c = r.read(1)
            if not ord(c) in buttons:
                continue
            c = buttons[ord(c)]
        w.write(c)
        w.flush()
else:
    r = os.fdopen(master,  'rb', 0)
    w = open(minitel, 'wb', 0)
    while 1:
        c = r.read(1)
        if len(c) == 0:
            break
        if ord(c) in conv:
            c = conv[ord(c)]
        elif ord(c) >= 0xA0:
            c = b' ' # placeholder
        elif ord(c) >= 0x80:
            continue
        w.write(c)
        w.flush()
