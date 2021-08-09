#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import configparser

import LMS
import text_utils
from whiptail import Whiptail


# MEMO writable char: max_h = 18
#                     max_w = 76
#This is when there is a whiptail windows

class Main:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("options.ini")

        self.whip = Whiptail(self.config['WHIPTAIL']['title'], backtitle=self.config['WHIPTAIL']['corner_title'],
                             height=24, width=80)

        choix_menuMain_no_center = ("Music", "other...", "Quitter")

        self.choix_menuMain = text_utils.center_list(choix_menuMain_no_center)

        self.menu()

    def menu(self):
        selection = self.whip.menu("", self.choix_menuMain).decode("UTF-8")

        if selection == self.choix_menuMain[0]: self.start_LMS()
        if selection == self.choix_menuMain[-1]: exit()

    def start_LMS(self):
        host = str(self.config['LMS']['hostname'])
        port = int(self.config['LMS']['port'])
        mac = self.config['LMS']['mac']

        LMS.LMS(self.whip, host, port, mac)

        self.menu()


Main()
