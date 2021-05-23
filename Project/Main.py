from pylms.server import Server
from pylms.player import Player
from whiptail import *


def LMS_co():
  sc = Server(hostname="192.168.0.10", port=9090, username=" ", password=" ")
  sc.connect()
  sq = sc.get_player("00:0f:55:a8:d0:f9")
  return (sq.is_connected, sc, sq)

def LMS_Menu(Connected, Server, Player):
  choix_menuLMS = ("Pause/play", "Stop", "Next", "Previous", 
                   "Jouer une musique / Ajouter une musique a la playlist ","Ajouter un Album a la playlist","Regarder la playlist", "Clear la playlist",
                   "Chercher une musique", "Chercher un album", "Chercher un artiste", 
                   "Quitter")
  response = whip.menu("", choix_menuLMS).decode("UTF-8")
  
  if response == choix_menuLMS[0]: 
    if Connected:
      Player.toggle()
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
    
  if response == choix_menuLMS[1]:
    if Connected:
      Player.stop()
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[2]:
    if Connected:
      Player.next()
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[3]:
    if Connected:
      Player.previous()
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[4]:
    if Connected:
      result = whip.prompt("Mettez le nom de la musique, ca peut etre l'ID").decode("UTF-8")
      song_id = Server.search(result, mode="songs")[1][0]["url"]
      appendd = whip.confirm("Voulez-vous ajouter ce morceau a la playlist (oui) ou voulez-vous le jouer maintenant (non) ?")
      
      if appendd:
        Player.playlist_add(song_id)
      else:
        Player.playlist_play(song_id)
        
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[5]:
    if Connected:
      result = whip.prompt("Mettez le nom de l'album, ca peut etre l'ID").decode("UTF-8")
      album_id = Server.search(result, mode="albums")[1][0]
      Player.playlist_addalbum(None, album_id["artist"], album_id["album"])

        
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
      
  if response == choix_menuLMS[6]:
    if Connected:
      playlist = Player.playlist_get_info()
      playlist2 = []
      for album in range(len(playlist)):
        playlist2.append("%s from %s by %s" % (playlist[album]['title'], playlist[album]['album'], playlist[album]['artist']))
      try:
        result = whip.showlist("radiolist", "Voici la playist actuelle, il y a %i titres, cocher des cases ne sert a rien" % ( Player.playlist_track_count(),) ,playlist2 , "")
      except IndexError:
        whip.alert("Il y a rien dans la playlist, dommage...")
      except:
        pass

      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[7]:
    if Connected:
      result = whip.confirm("Voulez vous vraiment faire ca?")
      if result: Player.playlist_clear()
      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[8]:
    if Connected:
      result = whip.prompt("Mettez le titre de la musique").decode("UTF-8")
      song = Server.search(result, mode="songs")[1]
      playlist2 = []
      for i in range(len(song)):
        playlist2.append("%s from %s by %s" % (song[i]['title'], song[i]['album'], song[i]['artist']))
      try:
        result = whip.showlist("radiolist", "Resultats de recherche" ,playlist2 , "")
      except IndexError:
        whip.alert("Mauvais recherche, dommage...")
      except:
        pass

      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[9]:
    if Connected:
      result = whip.prompt("Mettez le titre de l'album").decode("UTF-8")
      album = Server.search(result, mode="albums")[1]
      playlist2 = []
      for i in range(len(album)):
        playlist2.append("%s by %s" % (album[i]['album'], album[i]['artist']))
      try:
        result = whip.showlist("radiolist", "Resultats de recherche" ,playlist2 , "")
      except IndexError:
        whip.alert("Mauvais recherche, dommage...")
      except:
        pass

      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
  if response == choix_menuLMS[10]:
    if Connected:
      result = whip.prompt("Mettez l'artist").decode("UTF-8")
      artist = Server.search(result, mode="artists")[1]
      playlist2 = []
      for i in range(len(artist)):
        playlist2.append("%s" % (artist[i]['artist']))
      try:
        result = whip.showlist("radiolist", "Resultats de recherche" ,playlist2 , "")
      except IndexError:
        whip.alert("Mauvais recherche, dommage...")
      except:
        pass

      LMS_Menu(Connected, Server, Player)
    else:
      whip.alert("Vous n'avez pas le Player de connecte!")
      LMS_Menu(Connected, Server, Player)
      
      
  if response == choix_menuLMS[-1]: Principal()
  
  
def Principal():
  choix_menuP = ("Ce connecter a la musique","TODO", "Quitter")
  response = whip.menu("", choix_menuP).decode("UTF-8")
  
  
  if response == choix_menuP[0]:
    co, ser, ply = LMS_co()
    if co:
      LMS_Menu(True, ser, ply)
    else:
      whip.alert("Le player n'est pas connecte, dommage...")
      LMS_Menu(False, ser, None)
      
  if response == choix_menuP[-1]:
    result = whip.confirm("Si vous etes Nele, appuyer sur non")
    if result: exit()
    else: Principal()
    
  
    
    
whip = Whiptail("Le Minitel des Hilkens", backtitle="B.Hilkens 2021", height=24, width= 80)
Principal()