#!/usr/bin/env python

from pylms.server import Server
from pylms.player import Player


sc = Server(hostname="192.168.0.10", port=9090, username=" ", password=" ")
sc.connect()

print("Logged in: %s" % sc.logged_in)
print("Version: %s" % sc.get_version())

sq = sc.get_player("00:0f:55:a8:d0:f9")

print("Numbers of players: %d | players: %s " % (sc.get_player_count(), sc.get_players()))
print("Name: %s | Mode: %s | Time: %s | Connected: %s | WiFi: %s" % (sq.get_name(), sq.get_mode(), sq.get_time_elapsed(), sq.is_connected, sq.get_wifi_signal_strength()))



print(sq.get_track_current_title())
print(sq.get_time_elapsed())
print(sq.get_time_remaining())

print(sq.get_track_title())
print(sq.get_track_album())
print(sq.get_track_artist())
print(sq.get_track_duration())
print(sq.get_track_genre())

playlist_not_treated = sq.playlist_get_info()
playlist_treated = []

for i in range(9):
    playlist_treated.append(
        (playlist_not_treated[i]['title'], playlist_not_treated[i]['artist'])
        )
        
print(playlist_treated)