# Cleans all files ending with ~ as their extension
# Daniel Porteous 696965 12/08/14

import os

to_del = []
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        full = os.path.join(root, name)
        exten = name.split(".")[-1]
        if "~" in exten:
            to_del.append(full)

print "Are you sure you want to delete these?\n"
for i in to_del:
    print i
ok = raw_input("(Y)es or (N)o? ").lower()

if ok == "y":
    for i in to_del:
        os.remove(i)

print "Done!\n"
