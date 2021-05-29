#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from whiptail import Whiptail

x = Whiptail("Le Minitel des Hilkens", backtitle="B.Hilkens 2021", height=24, width= 80)

def center_textstr(input_str, max_chars=None, both_side=False): #Outputs a list with *space required to have the text centered
  if max_chars==None: max_chars= int(len(max(input_str, key=len))/2)
  if both_side: return " "*(int(max_chars/2)-int(len(input_str)/2)) + input_str + " "*(int(max_chars/2)-int(len(input_str)/2))
  else: return " "*(int(max_chars/2)-int(len(input_str)/2)) + input_str

max_h = 18
max_w = 76

gauge_box = (
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
"|---------------------------------------------------------|",
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+"
)

real_gauge=(
center_textstr(gauge_box[0], max_chars=max_w),
center_textstr('Time_now' + gauge_box[1]+ 'time_max', max_chars=max_w),
center_textstr(gauge_box[2], max_chars=max_w)
)
#the char need to be a pair
Now = (
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
"|" + center_textstr("Title song", 30, True) + "|",
"|" + center_textstr("From", 30, True) + "|",
"|" + center_textstr("Albumt", 30, True) + "|",
"|" + center_textstr("By", 30, True) + "|",
"|" + center_textstr("Artist", 30, True) + "|",
"|" + center_textstr("", 30, True) + "|",
"|" + "Genre: " + "Yessss" + center_textstr("", (30-len("Genre: " + "Yessss"))*2, False ) + "|",
"|" + center_textstr("", 30, True) + "|",
"|" + "Volume: " + "9" + center_textstr("", (30-len("Volume: " + "9"))*2, False ) + "|",
"|" + center_textstr("", 30, True) + "|",
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+"
)

Next = (
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"|" + center_textstr("Song random"[:15] + " by " + "random artist"[:14], 40, True) + "|",
"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+",
)

Monitor = (
center_textstr(" ", max_w),
Now[0] + " "*2 + Next[0],
Now[1] + " "*2 + Next[1],
Now[2] + " "*2 + Next[2],
Now[3] + " "*2 + Next[3],
Now[4] + " "*2 + Next[4],
Now[5] + " "*2 + Next[5],
Now[6] + " "*2 + Next[6],
Now[7] + " "*2 + Next[7],
Now[8] + " "*2 + Next[8],
Now[9] + " "*2 + Next[9],
Now[10] + " "*2 + Next[10],
Now[11] + " "*2 + Next[11],
center_textstr(" ", max_w),
real_gauge[0],
real_gauge[1],
real_gauge[2],
center_textstr(" ", max_w)
)

x.confirm("\n".join(Monitor), default='no')