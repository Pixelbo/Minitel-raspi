import threading
import time
from pylms.server import Server
import text_utils

class LMS():
    def __init__(self, whip):

        self.hostname_ = "192.168.0.10"
        self.port_ = 9090
        self.mac_ = "00:0f:55:a8:d0:f9"

        self.update = False
        self.stop_threads = False
        self.whip = whip

        self.server = Server(hostname=self.hostname_, port=self.port_, username=" ", password=" ")
        self.server.connect()

        try:
            self.player = self.server.get_player(self.mac_)
        except Exception as e:
            print(e)
            self.whip.alert("Vous n'avez pas de player!")
            #Main()
            # return

        choix_menuLMS_no_center = ("Pause/play", "Stop", "Next", "Previous", "----------------",
                                   "Status page", "Regarder la playlist", "Clear la playlist", "Manageur de playlists",
                                   "----------------",
                                   "Ajouter un titre a la playlist", "Ajouter un album a la playlist",
                                   "Chercher un artiste", "----------------",
                                   "Quitter")

        self.choix_menuLMS = text_utils.center_list(choix_menuLMS_no_center)
        self.menu()

    def updater_status(self):
        prev = self.player.get_track_current_title()
        while True:
            if self.player.get_track_current_title() != prev:
                self.update = True
                self.whip.p.terminate()
                break
            if self.stop_threads:
                self.stop_threads = False
                break
            time.sleep(1)

    def menu(self, overdrive=None):
        if overdrive is not None:
            selection = overdrive
        else:
            selection = self.whip.menu("", self.choix_menuLMS).decode("UTF-8")

        if selection == self.choix_menuLMS[0]: self.toggle()  # TODO: better selection method
        if selection == self.choix_menuLMS[1]: self.stop()
        if selection == self.choix_menuLMS[2]: self.next()
        if selection == self.choix_menuLMS[3]: self.previous()
        if selection == self.choix_menuLMS[5]: self.status_page()  # todo
        if selection == self.choix_menuLMS[6]: self.lookpl()
        if selection == self.choix_menuLMS[7]: self.clearpl()
        if selection == self.choix_menuLMS[8]: self.playlist_manager()
        if selection == self.choix_menuLMS[10]: self.title_add()
        if selection == self.choix_menuLMS[11]: self.album_add()
        if selection == self.choix_menuLMS[12]: self.artist_lp()
        if selection == (self.choix_menuLMS[4] or
                         self.choix_menuLMS[9] or
                         self.choix_menuLMS[13]):
            self.menu()  # redraw because pass will take us back to previous menu
        if selection == self.choix_menuLMS[-1]: Main()

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
        self.player.prev()
        self.menu()

    def lookpl(self):
        playlist_not_treated = self.player.playlist_get_info()
        playlist_treated = []

        for i in range(len(playlist_not_treated)):
            playlist_treated.append(
                "%s from %s by %s" % (
                    playlist_not_treated[i]['title'], playlist_not_treated[i]['album'],
                    playlist_not_treated[i]['artist'])
            )

        try:
            result = self.whip.showlist("radiolist",
                                        "Voici la playist actuelle, il y a %i titres, cocher des cases ne sert a rien" % (
                                            self.player.playlist_track_count(),)
                                        , playlist_treated, "")

        except IndexError:
            self.whip.alert("Il y a rien dans la playlist, dommage...")

        except:
            pass

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
            song_list_treated.append(
                "%s from %s by %s" % (song_list[i]['title'], song_list[i]['album'], song_list[i]['artist']))

        try:
            result = self.whip.menu("Resultats de recherche", song_list_treated).decode("UTF-8")
            song = song_list[song_list_treated.index(result)]['url']
            appendd = self.whip.confirm("Voulez-vous jouer ce titre maintenant? ")
            if not appendd:
                self.player.playlist_add(song)
            else:
                self.player.playlist_play(song)

        except IndexError:
            self.whip.alert("Mauvaise recherche, dommage...")
        except:
            self.whip.alert("Erreur, dommage...")

        self.menu()

    def album_add(self):
        result = self.whip.prompt("Mettez le titre de l'album").decode("UTF-8")
        album_list = self.server.search(result, mode="albums")[1]
        album_list_treated = []

        for i in range(len(album_list)):
            album_list_treated.append(" %s by %s" % (album_list[i]['album'], album_list[i]['artist']))

        try:
            result = self.whip.menu("Resultats de recherche", album_list_treated).decode("UTF-8")
            album_ar = album_list[album_list_treated.index(result)]['artist']
            album = album_list[album_list_treated.index(result)]['album']
            self.player.playlist_addalbum(None, album_ar, album)

        except IndexError:
            self.whip.alert("Mauvais recherche, dommage...")
        except:
            self.whip.alert("Erreur, dommage...")

        self.menu()

    def artist_lp(self):
        result = self.whip.prompt("Mettez l'artist").decode("UTF-8")
        artists = self.server.search(result, mode="artists")[1]
        artists_treated = []
        for i in range(len(artists)):
            artists_treated.append("%s" % (artists[i]['artist']))

        try:
            self.whip.showlist("radiolist", "Resultats de recherche", artists_treated, "")
        except IndexError:
            self.whip.alert("Mauvais recherche, dommage...")
        #        except:
        #            self.whip.alert("Erreur, dommage...")

        self.menu()

    def status_page(self):
        # const:
        # TODO

        player_volume = self.player.get_volume()
        volume = ("Volume:" if player_volume != 0 else "Volume :") + str(player_volume) + "%"
        track_title = self.player.get_track_current_title()
        track_artist = self.player.get_track_artist()
        track_album = self.player.get_track_album()
        track_genre = self.player.get_track_genre()
        genre = ("Genre: " + track_genre) if track_genre != "No Genre" else ""

        playlist_not_treated = self.player.playlist_get_info()
        playlist_treated = []

        for i in range(1, 10):
            try:
                playlist_treated.append(
                    (playlist_not_treated[i]['title'], " by ", playlist_not_treated[i]['artist'])
                )
            except IndexError:
                playlist_treated.append(
                    (" ", " ", " ")
                )

        # the char need to be a pair
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

        next_tracks = (
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
            "|" + text_utils.center_text("Next Tracks", 40, True) + "|",
            "|" + text_utils.center_text(playlist_treated[0][0][:18] + playlist_treated[0][1] + playlist_treated[0][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[1][0][:18] + playlist_treated[1][1] + playlist_treated[1][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[2][0][:18] + playlist_treated[2][1] + playlist_treated[2][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[3][0][:18] + playlist_treated[3][1] + playlist_treated[3][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[4][0][:18] + playlist_treated[4][1] + playlist_treated[4][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[5][0][:18] + playlist_treated[5][1] + playlist_treated[5][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[6][0][:18] + playlist_treated[6][1] + playlist_treated[6][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[7][0][:18] + playlist_treated[7][1] + playlist_treated[7][2][:18], 40,
                              True) + "|",
            "|" + text_utils.center_text(playlist_treated[8][0][:18] + playlist_treated[8][1] + playlist_treated[8][2][:18], 40,
                              True) + "|",
            "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
        )

        final_message = (
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
            text_utils.center_text(" ", 76),
            text_utils.center_text(" ", 76),
            text_utils.center_text(" ", 76)
        )

        self.updater = threading.Thread(target=self.updater_status)

        if self.update:
            self.update = False

        self.updater.start()

        decision = self.whip.confirm("\n".join(final_message), extras=("Quit", "Quit"))

        if self.update:
            self.menu(overdrive=self.choix_menuLMS[5])
        else:
            self.stop_threads = True
            self.updater.join()
            if decision:
                self.menu()
            else:
                self.menu()  # TODO: album cover

    ##        if decision: self.menu()
    ##        else: self.status_page()

    def playlist_manager(self):
        try:

            playlists = self.server.request_with_results("playlists 0 50 tags:u")
            nb_playlists = playlists[0]
            playlists_name = [playlists[1][i + 1]['playlist'] for i in range(nb_playlists)]
            playlists_url = [playlists[1][i + 1]['url'] for i in range(nb_playlists)]
            playlists_id = [playlists[1][i + 1]['id'] for i in range(nb_playlists)]

            selection = self.whip.menu("Manageur de playlist", text_utils.center_list(playlists_name), extras=()).decode("UTF-8")

            pl_options = (
                "Jouer cete playlist", "Editer cette playlist", "Rename la playlist", "Supprimmer cette playlist",
                "Retour")

            choix = self.whip.menu("Manageur de playlist: " + selection, text_utils.center_list(pl_options), extras=()).decode(
                "UTF-8")

            if choix == pl_options[0]: self.server.request(
                self.mac_ + " playlist add " + playlists_url[playlists_name.index(selection)])
            if choix == pl_options[1]:
                pl_tracks = self.server.request_with_results("playlists tracks 0 50 playlist_id:" + playlists_id[
                    playlists_name.index(selection)] + " tags:galdu")
                nb_tracks = pl_tracks[0]
                pl_tracks_url = [pl_tracks[1][i + 1]['url'] for i in range(nb_tracks)]
                pl_tracks_info = []
                for i in range(nb_tracks):
                    pl_tracks_info.append(pl_tracks[1][i + 1]['title'] + " par " + pl_tracks[1][i + 1]['artist'])

                track_sel = self.whip.menu("Editeur de playlist: " + selection, pl_tracks_info, extras=()).decode(
                    "UTF-8")

                track_option = ("Jouer ce morceau", "Suprimer le morceau de liste", "Mettre le morceau au-dessus",
                                "Mettre le morceau en-dessous")
                edit_sel = self.whip.menu("Editeur de playlist: " + selection, center_list(track_option),
                                          extras=()).decode("UTF-8")

                if edit_sel == text_utils.center_list(track_option)[0]: self.player.playlist_play(
                    pl_tracks_url[pl_tracks_info.index(track_sel)])
                if edit_sel == text_utils.center_list(track_option)[1]: self.server.request(
                    "playlists edit cmd:delete playlist_id:{} index:{}".format(
                        playlists_id[playlists_name.index(selection)], pl_tracks_info.index(track_sel) + 1))
                if edit_sel == text_utils.center_list(track_option)[2]: self.server.request(
                    "playlists edit cmd:up playlist_id:{} index:{}".format(
                        playlists_id[playlists_name.index(selection)], pl_tracks_info.index(track_sel) + 1))
                if edit_sel == text_utils.center_list(track_option)[3]: self.server.request(
                    "playlists edit cmd:down playlist_id:{} index:{}".format(
                        playlists_id[playlists_name.index(selection)], pl_tracks_info.index(track_sel) + 1))

        except Exception as e:
            print(e)
            self.whip.alert("Erreur, dommage...")

        self.menu()