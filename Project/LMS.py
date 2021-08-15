import threading
import time

import text_utils
from pylms.server import Server


class LMS:
    def __init__(self, whip, host, port, mac):

        self.hostname_ = host
        self.port_ = port
        self.mac_ = mac

        self.update = False  # Var to check if there is an update
        self.stop_threads = False  # self-explaining

        self.whip = whip  # We keep the same whiptail object through the code

        try:  # trying to connect to the server
          self.server = Server(hostname=self.hostname_, port=self.port_, username=" ", password=" ")
          self.server.connect()
        except Exception as e:  # if no server then alert an error and return back to main menu
            self.whip.alert("Vous n'avez pas de server! \n Erreur: " + str(e))
            return

        try:  # trying to connect to the player
            self.player = self.server.get_player(self.mac_)
        except Exception as e:  # if no player then alert an error and return back to main menu
            self.whip.alert("Vous n'avez pas de player! \n Erreur: " + str(e))
            # Main()
            return

        self.menu()
        return  # Todo: need to be check in test

    def updater_status(self):  # Simple 2nd thread to check if the track had changed
        prev = self.player.get_track_current_title()
        while True:
            if self.player.get_track_current_title() != prev:  # if it's changed
                self.update = True  # well, there is an update
                self.whip.p.terminate()  # terminate the status_page whiptail to redraw
                break
            if self.stop_threads:  # if the stop_thread var is up then stop with break
                self.stop_threads = False
                break
            time.sleep(1)

    def menu(self, overdrive=None):
        # Choice for the menu (not centered)
        choix_menuLMS_no_center = ("Pause/play", "Stop", "Next", "Previous",
                                   "----------------",
                                   "Status page", "Regarder la playlist", "Clear la playlist", "Manageur de playlists",
                                   "----------------",
                                   "Ajouter un titre a la playlist", "Ajouter un album a la playlist",
                                   "Chercher un artiste",
                                   "----------------",
                                   "Quitter")

        choix_menuLMS = text_utils.center_list(choix_menuLMS_no_center)  # Center the menu

        selection = self.whip.menu("", choix_menuLMS).decode("UTF-8")

        if selection == choix_menuLMS[0]: self.toggle()  # TODO: better selection method
        if selection == choix_menuLMS[1]: self.stop()
        if selection == choix_menuLMS[2]: self.next()
        if selection == choix_menuLMS[3]: self.previous()
        if selection == choix_menuLMS[5]: self.status_page()  # todo
        if selection == choix_menuLMS[6]: self.lookpl()
        if selection == choix_menuLMS[7]: self.clearpl()
        if selection == choix_menuLMS[8]: self.playlist_manager()
        if selection == choix_menuLMS[10]: self.title_add()
        if selection == choix_menuLMS[11]: self.album_add()
        if selection == choix_menuLMS[12]: self.artist_lp()
        if selection == (choix_menuLMS[4] or
                         choix_menuLMS[9] or
                         choix_menuLMS[13]):
            self.menu()  # redraw because retur will take us back to previous menu
        if selection == choix_menuLMS[-1]: return  # go to __Init__ then to Main()

        self.menu()  # Loop-back

    def toggle(self):  # like, it's litteraly the name
        self.player.toggle()
        return

    def stop(self):  # again
        self.player.stop()
        return

    def next(self):  # and again
        self.player.next()
        return

    def previous(self):  # and again
        self.player.prev()
        return

    def lookpl(self):  # We want to look at our current playlist
        playlist_not_treated = self.player.playlist_get_info()  # not_treated because not parsed for showing to screen
        playlist_treated = []  # init

        for i in range(len(playlist_not_treated)):
            playlist_treated.append("{} from {} by {}".format(
                playlist_not_treated[i]['title'],
                playlist_not_treated[i]['album'],
                playlist_not_treated[i]['artist'])
            )

        try:
            self.whip.showlist("radiolist",
                               "Voici la playist actuelle, il y a {} titres, cocher des cases ne sert a rien".format(
                                   self.player.playlist_track_count())  # track_count shown in the title
                               , playlist_treated,  # list to show
                               "")  # no parameters

        except IndexError:
            self.whip.alert("Il y a rien dans la playlist, dommage...")
        except Exception as e:
            self.whip.alert("Erreur, dommage! \n Erreur: " + str(e))

        return

    def clearpl(self):  # Clear the playlist
        result = self.whip.confirm("Voulez vous vraiment faire ca?")  # Return bool
        if result: self.player.playlist_clear()
        return

    def title_add(self):  # We want to add a title
        result = self.whip.prompt("Mettez le titre").decode("UTF-8")  # Prompt for a title and decode it
        song_list = self.server.search(result, mode="songs")[1]  # Search function within the LMS lib
        song_list_treated = []  # Same as lookpl()

        for i in range(len(song_list)):
            song_list_treated.append(
                "%s from %s by %s" % (song_list[i]['title'], song_list[i]['album'], song_list[i]['artist']))

        try:
            result = self.whip.menu("Resultats de recherche", song_list_treated).decode(
                "UTF-8")  # Prints the result and get the name
            song = song_list[song_list_treated.index(result)]['url']  # get the url of the song with the index function
            appendd = self.whip.confirm(
                "Voulez-vous jouer ce titre maintenant? ")  # Do we want to append the title to te playlist or play it now?
            if not appendd:
                self.player.playlist_add(song)
            else:
                self.player.playlist_play(song)

        except IndexError:
            self.whip.alert("Mauvaise recherche, dommage...")
        except Exception as e:
            self.whip.alert("Vous n'avez pas de player! \n Erreur: " + str(e))

        return

    def album_add(self):  # We want to add a full album; It's a litteral copy of the previous function
        result = self.whip.prompt("Mettez le titre de l'album").decode("UTF-8")
        album_list = self.server.search(result, mode="albums")[1]
        album_list_treated = []

        for i in range(len(album_list)):
            album_list_treated.append(" {} by {}".format(album_list[i]['album'], album_list[i]['artist']))

        try:
            result = self.whip.menu("Resultats de recherche", album_list_treated).decode("UTF-8")
            album_ar = album_list[album_list_treated.index(result)]['artist']
            album = album_list[album_list_treated.index(result)]['album']
            self.player.playlist_addalbum(None, album_ar, album)

        except IndexError:
            self.whip.alert("Mauvais recherche, dommage...")
        except Exception as e:
            self.whip.alert("Vous n'avez pas de player! \n Erreur: " + str(e))

        return

    def artist_lp(self):  # We want to look up a artist in db
        result = self.whip.prompt("Mettez l'artist").decode("UTF-8")  # Prompt for the artist to lookup
        artists = self.server.search(result, mode="artists")[1]  # search but with te artist param
        artists_treated = []  # same as before
        for i in range(len(artists)):
            artists_treated.append("%s" % (artists[i]['artist']))

        try:  # show it
            self.whip.showlist("radiolist", "Resultats de recherche", artists_treated, "")
        except IndexError:
            self.whip.alert("Mauvais recherche, dommage...")
        except Exception as e:
            self.whip.alert("Vous n'avez pas de player! \n Erreur: " + str(e))

        return

    def status_page(self):  # OMG it's complicated; it's a status page to see what is playling right now

        # Get various ingo and parse it
        player_volume = self.player.get_volume()
        volume = ("Volume:" if player_volume != 0 else "Volume :") + str(player_volume) + "%"
        track_title = self.player.get_track_current_title()
        track_artist = self.player.get_track_artist()
        track_album = self.player.get_track_album()
        track_genre = self.player.get_track_genre()
        genre = ("Genre: " + track_genre) if track_genre != "No Genre" else ""

        if not track_title:  # if there is nothing thn don't bother to draw everything
            self.whip.alert("Il y a pas de musique en cours!")
            return

        # Get the playlist like the fnction that does that
        playlist_not_treated = self.player.playlist_get_info()
        playlist_treated = []

        for i in range(1, 10):
            try:
                playlist_treated.append(
                    (playlist_not_treated[i]['title'], " by ", playlist_not_treated[i]['artist'])
                )
            except IndexError:  # if there is nothing then it's just blank
                playlist_treated.append(
                    (" ", " ", " ")
                )

        # window to see current track
        music_now = (
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
            "|" + text_utils.center_text(track_title[:28], 30, True) + "|",
            "|" + text_utils.center_text("From", 30, True) + "|",
            "|" + text_utils.center_text(track_album[:28], 30, True) + "|",
            "|" + text_utils.center_text("By", 30, True) + "|",
            "|" + text_utils.center_text(track_artist[:28], 30, True) + "|",
            "|" + text_utils.center_text("", 30, True) + "|",
            "|" + genre + text_utils.center_text("", (30 - len(genre)) * 2, False) + "|",  # Left align
            "|" + text_utils.center_text("", 30, True) + "|",
            "|" + volume + text_utils.center_text("", (30 - len(volume)) * 2, False) + "|",  # Left align
            "|" + text_utils.center_text("", 30, True) + "|",
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+"
        )

        next_tracks = (  # Window to see next tracks
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
            "|" + text_utils.center_text("Next Tracks", 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[0][0][:18] + playlist_treated[0][1] + playlist_treated[0][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[1][0][:18] + playlist_treated[1][1] + playlist_treated[1][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[2][0][:18] + playlist_treated[2][1] + playlist_treated[2][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[3][0][:18] + playlist_treated[3][1] + playlist_treated[3][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[4][0][:18] + playlist_treated[4][1] + playlist_treated[4][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[5][0][:18] + playlist_treated[5][1] + playlist_treated[5][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[6][0][:18] + playlist_treated[6][1] + playlist_treated[6][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[7][0][:18] + playlist_treated[7][1] + playlist_treated[7][2][:18], 40, True) + "|",
            "|" + text_utils.center_text(
                playlist_treated[8][0][:18] + playlist_treated[8][1] + playlist_treated[8][2][:18], 40, True) + "|",
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
        )

        final_message = (  # Avengers, Assemble!
            text_utils.center_text(" ", 76),
            music_now[0] + " " * 2 + next_tracks[0],
            music_now[1] + " " * 2 + next_tracks[1],
            music_now[2] + " " * 2 + next_tracks[2],
            music_now[3] + " " * 2 + next_tracks[3],
            music_now[4] + " " * 2 + next_tracks[4],
            music_now[5] + " " * 2 + next_tracks[5],
            music_now[6] + " " * 2 + next_tracks[6],
            music_now[7] + " " * 2 + next_tracks[7],
            music_now[8] + " " * 2 + next_tracks[8],
            music_now[9] + " " * 2 + next_tracks[9],
            music_now[10] + " " * 2 + next_tracks[10],
            music_now[11] + " " * 2 + next_tracks[11],
            text_utils.center_text(" ", 76),
            text_utils.center_text(" ", 76),
            text_utils.center_text(" ", 76),  # Black, can be other info
            text_utils.center_text(" ", 76),
            text_utils.center_text(" ", 76)
        )

        self.updater = threading.Thread(target=self.updater_status)  # init the thread

        if self.update:  # un-check the update var
            self.update = False

        self.updater.start()  # start the updater

        decision = self.whip.confirm("\n".join(final_message), extras=("Quit", "Quit"))  # Join the message with \n
        # When we terminate the whip process, the code below gets executed
        if self.update:  # if there is an update redraw
            self.status_page()
        else:  # else, it's an user input then stop threads
            self.stop_threads = True
            self.updater.join()
            if decision:  # Can have more things here
                return
            else:
                return

    def playlist_manager(
            self):  # OMG it's like the inception of whiptails; tests to do
        try:
            playlists = self.server.request_with_results("playlists 0 50 tags:u") # fetch
            nb_playlists = playlists[0] #parse info
            playlists_name = [playlists[1][i + 1]['playlist'] for i in range(nb_playlists)]
            playlists_name_ctr = text_utils.center_list(playlists_name)
            playlists_url = [playlists[1][i + 1]['url'] for i in range(nb_playlists)]
            playlists_id = [playlists[1][i + 1]['id'] for i in range(nb_playlists)]

            selection = self.whip.menu("Manageur de playlist", playlists_name_ctr, extras=()).decode("UTF-8")

            pl_options = (
                "Jouer cete playlist",
                "Editer cette playlist",
                "Rename la playlist",
                "Supprimmer cette playlist",
                "Retour")

            pl_options_ctr = text_utils.center_list(pl_options)

            choix = self.whip.menu("Manageur de playlist: " + selection, pl_options_ctr, extras=()).decode(
                "UTF-8")

            if choix == pl_options_ctr[0]: # add playist to playlist
                self.server.request(self.mac_ + " playlist add " + playlists_url[playlists_name_ctr.index(selection)])

            if choix == pl_options_ctr[1]: # edit-playlist
                # Get tracks and other infos
                pl_tracks = self.server.request_with_results("playlists tracks 0 50 playlist_id:" + playlists_id[playlists_name_ctr.index(selection)] + " tags:galdu")
                nb_tracks = pl_tracks[0]
                pl_tracks_url = [pl_tracks[1][i + 1]['url'] for i in range(nb_tracks)]
                pl_tracks_info = []

                for i in range(nb_tracks): #For the menu
                    pl_tracks_info.append(pl_tracks[1][i + 1]['title'] + " par " + pl_tracks[1][i + 1]['artist'])

                track_sel = self.whip.menu("Editeur de playlist: " + selection, text_utils.center_list(pl_tracks_info), extras=()).decode("UTF-8")
                # TODO: fix it!
                #Option to dowith the tracks
                track_option = (
                    "Jouer ce morceau",
                    "Suprimer le morceau de liste",
                    "Mettre le morceau au-dessus",
                    "Mettre le morceau en-dessous")

                track_option = text_utils.center_list(track_option) #center_it

                edit_sel = self.whip.menu("Editeur de playlist: " + selection, track_option,
                                          extras=()).decode("UTF-8")

                if edit_sel == track_option[0]:
                    self.player.playlist_play( pl_tracks_url[pl_tracks_info.index(track_sel)])

                if edit_sel == track_option[1]:
                    self.server.request("playlists edit cmd:delete playlist_id:{} index:{}".format(playlists_id[playlists_name_ctr.index(selection)], pl_tracks_info.index(track_sel) + 1))

                if edit_sel == track_option[2]:
                    self.server.request("playlists edit cmd:up playlist_id:{} index:{}".format(playlists_id[playlists_name_ctr.index(selection)], pl_tracks_info.index(track_sel) + 1))

                if edit_sel == track_option[3]:
                    self.server.request("playlists edit cmd:down playlist_id:{} index:{}".format(playlists_id[playlists_name_ctr.index(selection)], pl_tracks_info.index(track_sel) + 1))

            if choix == pl_options_ctr[2]:
                rename = self.whip.prompt("Quel nouveau nom voulez vous mettre à votre playlst?")

                decision = self.whip.confirm("Voulez-vous vraiment remplacer le nom de la playlist: \n {} \n par \n {} ?".format(rename,playlists_name_ctr.index(selection)))

                if decision:
                    self.server.request("playlists rename playlist_id:{} newname:{}".format(
                        playlists_id[playlists_name_ctr.index(selection)], rename))

            if choix == pl_options_ctr[2]:
                decision = self.whip.confirm(
                    "Voulez-vous vraiment supprimer la playlist {} ?".format(playlists_name_ctr.index(selection)))

                if decision:
                    self.server.request("playlists delete playlist_id:{}".format(
                        playlists_id[playlists_name_ctr.index(selection)]))

        except Exception as e:
            self.whip.alert("Erreur, dommage... \n Erreur: " + str(e))

        return
