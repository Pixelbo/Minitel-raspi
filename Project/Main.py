#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from pylms.server import Server
from pylms.player import Player
from whiptail import *


class LMS():
    def __init__(self, whip):
        self.server = Server(hostname="192.168.0.10", port=9090, username=" ", password=" ")
        self.server.connect()
        self.player = self.server.get_player("00:0f:55:a8:d0:f9")
        self.connected = self.player.is_connected

        self.whip = whip

        if self.connected:
            self.choix_menuLMS = ("Pause/play", "Stop", "Next", "Previous",
                       "Regarder la playlist", "Clear la playlist",
                       "Chercher un titre et l'ajouter a la playlist", "Chercher un album et l'ajouter a la playlist", "Chercher un artiste",
                       "Quitter")
            self.menu()
        else:
            self.whip.alert("Vous n'avez pas de player!")
            Main.menu()
            #return

    def menu(self):
        selction = self.whip.menu("", self.choix_menuLMS).decode("UTF-8")

        if selction == self.choix_menuLMS[0]: self.toggle()
        if selction == self.choix_menuLMS[1]: self.stop()
        if selction == self.choix_menuLMS[2]: self.next()
        if selction == self.choix_menuLMS[3]: self.previous()
        if selction == self.choix_menuLMS[4]: self.lookpl()
        if selction == self.choix_menuLMS[5]: self.clearpl()
        if selction == self.choix_menuLMS[6]: self.title_add()
        if selction == self.choix_menuLMS[7]: self.album_add()
        if selction == self.choix_menuLMS[8]: self.artist_lp()
        if selction == self.choix_menuLMS[-1]: Main.menu()

    def toggle(self):
        self.player.toggle()
        self.menu()

    def stop(self):
        self.player.stop()
        self.menu()

    def next(self):
        self.player.next()
        self.menu()

    def previous(self):
        self.player.previous()
        self.menu()

    def lookpl(self):
        playlist_not_treated = Player.playlist_get_info()
        playlist_treated = []

        for i in range(len(playlist)):
            playlist_treated.append(
                "%s from %s by %s" % (playlist_not_treated[i]['title'], playlist_not_treated[i]['album'], playlist_not_treated[i]['artist'])
                )

        try:
            result = self.whip.showlist("radiolist",
                                        "Voici la playist actuelle, il y a %i titres, cocher des cases ne sert a rien" % (self.player.playlist_track_count(),)
                                        ,playlist_treated , "")
            self.menu()
        except IndexError:
            self.whip.alert("Il y a rien dans la playlist, dommage...")
            self.menu()
        except:
            self.menu()

    def clearpl(self):
        result = self.whip.confirm("Voulez vous vraiment faire ca?")
        if result: self.player.playlist_clear()
        self.menu()

    def title_add(self):
        result = self.whip.prompt("Mettez le titre").decode("UTF-8")
        song_list = self.server.search(result, mode="songs")[1]
        song_list_treated = []

        for i in range(len(song_list)):
            song_list_treated.append("%s from %s by %s" % (song_list[i]['title'], song_list[i]['album'], song_list[i]['artist']))

        try:
            result = self.whip.menu("radiolist", "Resultats de recherche" ,playlist2 , "").decode("UTF-8")
            song = self.server.search(result, mode="songs")[1][0]['url']
            appendd = self.whip.confirm("Voulez-vous ajouter ce morceau a la playlist (oui) ou voulez-vous le jouer maintenant (non) ?")
            if appendd: self.player.playlist_add(song)
            else: self.player.playlist_play(song)

            self.menu()
        except IndexError:
            whip.alert("Mauvais recherche, dommage...")
            self.menu()
        except:
            self.menu()

    def album_add(self):
        result = self.whip.prompt("Mettez le titre de l'album").decode("UTF-8")
        song_list = self.server.search(result, mode="albums")[1]
        song_list_treated = []

        for i in range(len(song_list)):
            song_list_treated.append(" %s by %s" % (song_list[i]['album'], song_list[i]['artist']))

        try:
            result = self.whip.menu("radiolist", "Resultats de recherche" ,playlist2 , "").decode("UTF-8")
            song = self.server.search(result, mode="albums")[1][0]['url']
            appendd = self.whip.confirm("Voulez-vous ajouter cet album a la playlist (oui) ou voulez-vous le jouer maintenant (non) ?")
            if appendd: self.player.playlist_addalbum(song)
            else: self.player.playlist_addalbum(song)

            self.menu()
        except IndexError:
            whip.alert("Mauvais recherche, dommage...")
            self.menu()
        except:
            self.menu()

    def artist_lp(self):
        result = self.whip.prompt("Mettez l'artist").decode("UTF-8")
        artists = self.server.search(result, mode="artists")[1]
        artists_treated = []
        for i in range(len(artists)):
            artists_treated.append("%s" % (artists[i]['artist']))

        try:
            result = elf.whip.showlist("radiolist", "Resultats de recherche" ,artists_treated , "")
            self.menu()
        except IndexError:
            self.whip.alert("Mauvais recherche, dommage...")
            self.menu()
        except:
            self.menu()



class Main():
    def __init__(self):
        self.whip = Whiptail("Le Minitel des Hilkens", backtitle="B.Hilkens 2021", height=24, width= 80)

        self.choix_menuMain = ("Music","other...", "Quitter")

    def menu(self):
        selction = self.whip.menu("", choix_menuP).decode("UTF-8")

        if selection == self.choix_menuMain[0]: self.start_LMS()
        if selection == self.choix_menuMain[-1]: exit()

    def start_LMS(self):
        LMS(self.whip)

        self.menu()





Main()