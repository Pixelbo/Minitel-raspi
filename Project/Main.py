#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from whiptail import Whiptail
import utils
import LMS

# MEMO writable char: max_h = 18
#                     max_w = 76

class Main():
    def __init__(self):

        self.whip = Whiptail("Le Minitel des Hilkens", backtitle="B.Hilkens 2021", height=24, width=80)

        choix_menuMain_no_center = ("Music", "other...", "Quitter")

        self.choix_menuMain = utils.center_list(choix_menuMain_no_center)

        self.menu()

    def menu(self):
        selection = self.whip.menu("", self.choix_menuMain).decode("UTF-8")

        if selection == self.choix_menuMain[0]: self.start_LMS()
        if selection == self.choix_menuMain[-1]: exit()

    def start_LMS(self):
        LMS.LMS(self.whip)

        self.menu()


Main()
