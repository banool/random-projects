#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Python script that adds jobs to deluge based on which folder they are put in.
# Put this job in the deluge_user crontab. Mine is set up like this:
# * * * * * cd /srv/torrents && python sorter.py > sorter.log

# Note that all the file checks it does don't access anywhere on the second
# HDD where the media is stored until a torrent is actually added.
# This restricts all read/write operations to the one OS HDD, saving
# unecessary spin time for the media HDD which can hopefully spin down
# from time to time (whereas the OS HDD is essentially always active anyway).

from os import walk, listdir, system
from os.path import join
from sys import exit
from time import strftime

# The way I have sometimes relatively and other times absolutely defined
# the base and makes this script by no means portable.
root = "/srv/torrents/"
start = "."
media_type_list = ["Music", "TV Shows", "Movies"]
ending = "torrent"
dest_base = "/home/deluge_user/"
mod_base = "successfully_added/"
time_stamp = strftime("%d/%m/%Y | %H:%M:%S")

# Test so that the rest of the script won't run if there are no .torrent files
all_empty = True
for folder in media_type_list:
    if listdir("./" + folder):
        all_empty = False
        break

if all_empty:
    print time_stamp
    print "\r\nCollection folders empty. Terminating..."
    exit()

for (dirpath, dirnames, filenames) in walk(start):
    for i in filenames:
        path = join(dirpath, i)
        media_type = path.split("/")[-2]
        # This line is making sure that the file is in only one of the
        # three folders lsited in media_type_list and that they are
        # indeed .torrent files.
        if media_type in media_type_list and path.split("/")[-1].split(".")[-1] == ending:
            # Note the use of the windows line ending \r\n
            if media_type == "Movies":
                dest = dest_base + "movies/"
            elif media_type == "TV Shows":
                dest = dest_base + "tvshows/"
            else:
                dest = dest_base + "music/"
            full_path = root + path[2:]
            mod_path = root + mod_base + path.split("/")[-1]
            command = """deluge-console "add -p '%s' '%s'" && mv '%s' '%s'""" % (dest, full_path, full_path, mod_path)
            print "\r\n%s\r\nPath:    %s\r\nType:    %s\r\nCommand: %s\r\n\r\n" % (time_stamp, path, media_type, command)
            system(command)

print "Done!"

# Obviously this script is pretty dirty and quick, but it does the job
# and shouldn't break as long as its environment isn't tampered with.