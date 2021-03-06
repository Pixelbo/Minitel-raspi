#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys
from minitel.Minitel import Minitel

port = sys.argv[1] if len(sys.argv) >= 2 else 'ttyUSB0'
baudrate = 4800

minitel = Minitel(peripherique = '/dev/'+port)
minitel.identifier()
minitel.definir_vitesse(baudrate)
minitel.definir_mode('MIXTE')
minitel.echo(False)
minitel.curseur(True)
minitel.efface()
