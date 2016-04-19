#!/usr/bin/python3

"""
For whatever reason this only walks in the root directory.
When it recurses to lower directories it doesn't make or
execute the move command properly, like it's not joining
the root and the old name properly
"""

import os, time
from sys import exit
from sys import argv

ignore = []
ignore.append(argv[0])

output = []

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
        output.append([root, name, time.ctime(mtime)])

output.sort(key=lambda x: x[2])

for line in output:
    print(line)

commands = []

i = 0
dodge = 0
while i < len(output):
    item = output[i]
    name_split = item[1].split(".")
    old = item[1]
    if len(name_split) < 2:
        pass
    else:
        if old not in ignore:
            new = str(i+1-dodge) + "." + name_split[-1]
            command = "mv '%s' '%s'" % (os.path.join(root, old), os.path.join(root, new))
            commands.append(command)
        else:
            dodge += 1
        i += 1

print("These are the commands to be performed:")
for line in commands:
    print(line)
conf = input("Would you like to continue? (y or n) ")[0].lower()
if conf != "y":
    print("Ok, terminating...")
    exit(0)
else:
    for line in commands:
        os.system(line)

print("Done!")
