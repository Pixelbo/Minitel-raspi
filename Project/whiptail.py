# whiptail.py - Use whiptail to display dialog boxes from shell scripts
# Copyright (C) 2013 Marwan Alsabbagh
# license: BSD, see LICENSE for more details.
#Yeah I modified it

from __future__ import print_function

import itertools
import shlex
import sys
from collections import namedtuple
from subprocess import Popen, PIPE

__version__ = '0.2'
PY3 = sys.version_info[0] == 3
string_types = str
Response = namedtuple('Response', 'returncode value')


def flatten(data):
    return list(itertools.chain.from_iterable(data))


class Whiptail(object):
    def __init__(self, title='', backtitle='', height=10, width=50,
                 auto_exit=True):
        self.title = title
        self.backtitle = backtitle
        self.height = height
        self.width = width
        self.auto_exit = auto_exit

    def run(self, control, msg, extra=(), exit_on=(5,)):
        cmd = [
            'whiptail', '--title', self.title, '--backtitle', self.backtitle, '--nocancel',
            '--' + control, msg, str(self.height), str(self.width)
        ]
        cmd += list(extra)

        self.p = Popen(cmd, stderr=PIPE, stdin=PIPE)
            
        out, err = self.p.communicate()
        if self.auto_exit and self.p.returncode in exit_on:
            print('User cancelled operation.')
            sys.exit(self.p.returncode)
        return Response(self.p.returncode, err)

    def prompt(self, msg, default='', password=False):
        control = 'passwordbox' if password else 'inputbox'
        return self.run(control, msg, [default]).value

    def confirm(self, msg, extras=None):
        extra = '--defaultno' if extras == None else ('--yes-button', extras[0], '--no-button',  extras[1])
        return self.run('yesno', msg, extra, [255]).returncode == 0

    def alert(self, msg):
        self.run('msgbox', msg)

    def view_file(self, path):
        self.run('textbox', path, ['--scrolltext'])

    def calc_height(self, msg):
        height_offset = 8 if msg else 7
        return [str(self.height - height_offset)]

    def menu(self, msg='', items=(), extras =(''),prefix=' - '):
        if isinstance(items[0], string_types):
            items = [(i, '') for i in items]
        else:
            items = [(k, prefix + v) for k, v in items]
        extra = self.calc_height(msg) + flatten(items) + list(extras)
        return self.run('menu', msg, extra).value

    def showlist(self, control, msg, items, prefix):
        if isinstance(items[0], string_types):
            items = [(i, '', 'OFF') for i in items]
        else:
            items = [(k, prefix + v, s) for k, v, s in items]
        extra = self.calc_height(msg) + flatten(items)
        return shlex.split(self.run(control, msg, extra).value)

    def radiolist(self, msg='', items=(), prefix=' - '):
        return self.showlist('radiolist', msg, items, prefix)

    def checklist(self, msg='', items=(), prefix=' - '):
        return self.showlist('checklist', msg, items, prefix)
