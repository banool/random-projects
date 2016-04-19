# Daniel Porteous 696965
# Made: 31/07/2014
"""
This script works if this script is here: /iTunes/iTunes Media/Music
and the music is organised as such: ./Artist/Album/Song.mp3 or .m4a

This is accomplished by importing from your phone with the program PhoneTrans.
"""

from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3

import os

song_num = 0
exten_list = []

select = int(raw_input("Do you want to do the whole function on the whole iTunes folder,\nor just tag all the songs in a folder? (1 or 2) "))

if select == 1:
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            full = os.path.join(root, name)
            print "path: " + full
            title = "".join(name.split(".")[0:-1])
            print "title: " + title
            try:
                artist = root.split("/")[-2]
                print "artist: " + artist
            except IndexError:
                print "Artist Key error, probs a file in the root"
            try:
                album = root.split("/")[-1]
                print "album: " + album
            except IndexError:
                print "Album Key error, probs a file in the root"
            exten = name.split(".")[-1]
            if exten not in exten_list:
                exten_list.append(exten)
            if exten == "m4a":
                song_num += 1
                audio = MP4(full)
                audio["\xa9alb"] = album  #album
                audio["\xa9nam"] = title  #title
                audio["\xa9ART"] = artist #artist
                audio.save()
            if exten == "mp3":
                song_num += 1
                mp3file = MP3(full, ID3=EasyID3)
                try:
                    mp3file.add_tags(ID3=EasyID3)
                except mutagen.id3.error:
                    print("has tags")
                mp3file["album"] = unicode(album, "utf-8")
                mp3file["title"] = unicode(title, "utf-8")
                mp3file["artist"] = unicode(artist, "utf-8")
                mp3file.save()
elif select == 2:
    album = raw_input("What is the album name? ")
    artist = raw_input("What is the artist name? ")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            full = os.path.join(root, name)
            print "path: " + full
            title = "".join(name.split(".")[0:-1])
            print "title: " + title
            exten = name.split(".")[-1]
            if exten not in exten_list:
                exten_list.append(exten)
            if exten == "m4a":
                song_num += 1
                audio = MP4(full)
                audio["\xa9alb"] = album  #album
                audio["\xa9nam"] = title  #title
                audio["\xa9ART"] = artist #artist
                audio.save()
            if exten == "mp3":
                song_num += 1
                mp3file = MP3(full, ID3=EasyID3)
                try:
                    mp3file.add_tags(ID3=EasyID3)
                except mutagen.id3.error:
                    print("has tags")
                mp3file["album"] = unicode(album, "utf-8")
                mp3file["title"] = unicode(title, "utf-8")
                mp3file["artist"] = unicode(artist, "utf-8")
                mp3file.save()
else:
    print "That wasn't a valid option."

print "You have %s songs" % song_num
print "There are these types of extensions in your library: \n%s" % str(exten_list)
print "done"


"""
How to change encoding to UTF-8 (or ascii if you want).
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

print sys.getdefaultencoding()
"""

"""
Example of how it works.
audio = MP4("./Spitting Feathers EP/A Rat's Nest (ratsnestphone).mp3")
audio["\xa9alb"] = "album"  #album
audio["\xa9nam"] = "title"  #title
audio["\xa9ART"] = "artist" #artist
audio.save()
"""