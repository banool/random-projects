#!/usr/bin/python
# -*- coding: UTF-8 -*-

from os import walk
from os import remove
from os.path import exists
from shutil import rmtree


start = "."
ending = " 2"

file_del = []
dir_del = []

def scan(ending):
    for (dirpath, dirnames, filenames) in walk(start):
        for i in filenames:
            i_list = i.split(".")
            i_out = "".join(i_list[:-1])
            if i_out == "":
                i_out = i
            if i_out[-len(ending):] == ending and i_out[:-(len(ending))] in ["".join(x.split(".")[:-1]) for x in filenames]:
                """
                If it has the dupe ending and the base part of the name exists also without the (1). #Making sure its actually a dupe.
                Note that this list comprehension remakes the list of files in the filenames without the extensions.
                """
                file_del.append(dirpath + "/" + i)
            #print dirpath + "/" + i_out
        for j in dirnames:
            #print len(dirnames)
            if j[-len(ending):] == ending and j[:-(len(ending)+1)] in dirnames:
                dir_del.append(dirpath + "/" + j)

"""
Note: We delete files first. This is because if we delete the directory first,
if there happened to be a dupe file inside the dupe directory it won't be able
to find the file when it goes to delete it because the directory has already
been deleted. This isn't the most efficient approach but it is the least error
inducing method so we're using it.
"""

scan(ending)

print "\nFiles:"
for i in file_del:
    if exists(i):
        print i
    else:
        file_del.remove(i)

print "\nFolders:"
for j in dir_del:
    if exists(j):
        print j
    else:
        dir_del.remove(j)
print '\n'

conf = str(raw_input("Are you sure you want to delete these (y or n)? ")).lower()
if conf == 'y':
    for i in file_del:
        try:
            remove(i)
            print "*FILE* Success"
        except:
            print "*FILE* Something went wrong."
    for j in dir_del:
        try:
            rmtree(j)
            print "*DIR* Success"
        except:
            print "*DIR* Something went wrong."
else:
    print "All g"

raw_input("Press enter to quit...")


"""

from os.path import isfile
import itertools

def level_delete(root, ending):
    #print "watup"
    dirpath = []
    dirnames = []
    filenames = []

    f = []
    d = []
    
    for (dirpath, dirnames, filenames) in walk(root):
        for i in filenames:
            i_list = i.split(".")
            i_out = "".join(i_list[:-1])
            if i_out == "":
                i_out = i
            if i_out[-3:] == ending and i_out[:-4] in ["".join(x.split(".")[:-1]) for x in filenames]:
                #If it has the dup ending and the base part of the name exists also without the (1). #Making sure its actually a dupe.
                f.append(root + "\\" + i)
        if len(dirnames) == 0:
            #print "ay"
            pass
        else:
            for j in dirnames:
                #print len(dirnames)
                if j[-3:] == ending and j[:-4] in dirnames:
                    d.append(root + "\\" + j)
                else:
                    new_root = root + "\\" + j
                    #print new_root
                    level_delete(new_root, ending) #This little thing makes it recursive and it will check all lower folders.
    if f:
        file_del.append(f)
    if d:
        dir_del.append(d)


level_delete(start, ending)

file_del = list(itertools.chain.from_iterable(file_del))
dir_del = list(itertools.chain.from_iterable(dir_del))
# ^^This puts it into 1 list, no lists within lists^^

#print "file_del: " + str(file_del)
#print "dir_del: " + str(dir_del)

print "DIR_DEL"
for i in dir_del:
    if exists(i):
        print i
    else:
        dir_del.remove(i)
print "FILE_DEL"
for j in file_del:
    if exists(j):
        print j
    else:
        file_del.remove(j)

conf = raw_input("Are you sure you want to delete these? ")
if conf.lower() == "y" or "yes":
    for i in dir_del:
        try:
            rmtree(i)
            print "*DIR* Success"
        except:
            print "*DIR* Something went wrong."
    for j in file_del:
        try:
            print "*FILE* Success"
            remove(j)
        except:
            print "*FILE* Something went wrong."
else:
    print "All g."


Something is going wrong with the recursion, it appears to be going down the
first path it can find with a (1) duplicate in it, then putting that file at
the end of each root on the way back out. Then it just stops, without checking
the other folders after it. It's like it is recursing back up the directory tree,
instead of along the base root.

ANS: This was due to a fundamental misunderstanding of how os.walk() worked.
os.walk() actaully goes all the way down to the deepest point of each directory,
it doesn't just scan the top level of the directory. This means you DON'T need
to call it for each directory, it does this itself essentially.
"""
