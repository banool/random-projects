# Takes an input file that has a list of folders to check.
# It then takes the names of the folders inside it (without recursing down).
# This file is then saved to google drive.

import sys
import os
import datetime
import shutil

now = datetime.datetime.now()

def openfile(filename, mode):
    try:
        f = open(filename, mode)
        print("Opened %s in %s mode" % (filename, mode))
        return f
    except IOError:
        f = open(filename, "w")
        f.write("File made %s" % str(now))
        if(mode in "wra"):
            print("Made %s and opened in %s mode" % (filename, mode))
        else:
            print("Invalid mode. Exiting")
            sys.exit()
        f.close()
        f = open(filename, mode)
        return f
    except:
        print("Could not open %s." % filename)
        sys.exit()

f = openfile("input.txt", "r")

inp = f.readlines()
f.close()

f = openfile("output.txt", "w")

f.write("Input folders:\n")
for i in inp:
    f.write("  %s" % i)

f.write("\n\n\n")

for i in inp:
    i.rstrip('\n')
    f.write("%s\n********************************************\n" % i.rstrip('\n'))
    for item in os.listdir(i.rstrip('\n')):
        f.write("%s\%s\n" % (i.rstrip('\n'), item))
    f.write("\n")

f.close()

# Copying the file into google drive
shutil.copyfile("output.txt", "C:\Users\dan\Google Drive\Tech Stuff\medialist.txt")
print("Copied output.txt to Google Drive as medialist.txt")
print("\nDone!")