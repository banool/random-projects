#!/usr/bin/python

from subprocess import call
from sys import exit

# Target should be a list of urls one on a line.
target = "target.txt"
cookies = "cookies.txt"
subjectName = "geom20013"
pauseLocation = "pause.txt"
commandsLocation = "commands.txt"

# Modify this to include any lectures that didn't
# take place. The format is [week, [lectureNumber]]/
# Example: (6, [1, 3]). Meaning lectures 1 and 3
# were missed on week 6.
excluded = [(3, [1, 2]), (7, [2])]

# Should match the number of lectures per week.
# This assumes that there will always be this many
# lectures per week.
numLecturesPerWeek = 2

def printErrors(errors):
    print("There were errors with the following commands:")
    print(errors)
    print("Most likely because the urls supplied in %s were invalid for these commands." % target)

def processCommands(commands):
    errors = []
    for i in range(0, len(commands)):
        command = commands[i]
        try:
            if call(command, shell=True) != 0:
                errors.append(i)
        except KeyboardInterrupt:
            # We pause progress. Write line of current command
            # and the list of commands. At the top of the program
            # if these files exist, we give them the option to
            # resume the download.
            print("Pausing at %d: %s" % (i, command))
            with open(pauseLocation, "w") as f:
                f.write(str(i))
            with open(commandsLocation, "w") as f:
                for i in commands:
                    f.write(i + "\n")
            printErrors(errors)
            exit()
    # If we get here, all downloads were successfully completed.
    print("Done!")
    if isfile(pauseLocation):
        call("rm %s" % pauseLocation, shell=True)
    if isfile(commandsLocation):
        call("rm %s" % commandsLocation, shell=True)
    printErrors(errors)

# Checking if there are downloads in progress.
from os.path import isfile
if isfile(pauseLocation) and isfile(commandsLocation):
    with open(pauseLocation, "r") as f:
        start = int(f.read()[0])
    with open(commandsLocation, "r") as f:
        commands = [x.strip() for x in f.readlines()][start:]
    
    # Making sure they want to resume instead of go from the start.
    conf = raw_input("Would you like to start where you left off at %d? " % start)
    if conf[0].lower() == "y":
        print("Starting from command number %d." % start)    
        processCommands(commands)
        exit()

# If not, we move forward to generating the commands.

# Read in the file of target downloads.
with open(target, "r") as f:
    targetDownloads = [x.strip() for x in f.readlines()]

# Getting weeks 1 through to 12.
weeks = range(1, 13)

# Building a generic list not removing exclusions.
outputNumbering = []
for week in weeks:
    # Getting the lecture numbers as per numLecturesPerWeek.
    lecs = range(1, numLecturesPerWeek + 1)
    outputNumbering.append( (week, lecs) )

finalOutputNumbering = []

# Removing exclusions.
excludedWeeks = [x[0] for x in excluded]
# Iterate through the current list.
for i in outputNumbering:
    lecs = i[1]
    # If a week is in the list of weeks with exclusions.
    if i[0] in excludedWeeks:
        # Produces new list of lectures
        excludedLecs = excluded[excludedWeeks.index(i[0])][1]
        lecs = [x for x in lecs if x not in excludedLecs]
        # If there are no lectures left, remove the whole week.
        if len(lecs) == 0:
            continue
    # Otherwise add the new week with its lectures to the final
    # list of lectures.
    finalOutputNumbering.append( (i[0], lecs) )

# Now we count the number of lectures we have numbering for and
# see if it matches the number of files to download.
numLecsNumbering = 0
for i in finalOutputNumbering:
    numLecsNumbering += len(i[1])

# We check if the number of downloads available matches
# the number of lectures we've calculated we should have.
if numLecsNumbering != len(targetDownloads):
    print("Inconsistent number of downloads vs. numbering")
    print("Confirm you have the right exclusions list")

# We produce the output names for each download.
outputNames = []
lecNumber = 1
for week in finalOutputNumbering:
    for lecture in week[1]:
        # Relies upon the end of the target being named like:
        # audio-vga.m4v?download or audio.mp3?download
        extension = targetDownloads[lecNumber-1][-13:-9]
        args = (subjectName, week[0], lecture, lecNumber, extension)
        name = "%s_week%02d_lecture%d_%02d%s" % args
        outputNames.append(name)
        lecNumber += 1

commands = []
# Now we know the length of available downloads is the same
# as our list of numbering.
for i in range(0, numLecsNumbering):
    args = (cookies, targetDownloads[i], outputNames[i])
    base = """wget -c --load-cookies=%s --keep-session-cookies "%s" -O "%s" """ % args
    commands.append(base)

for i in commands:
    print(i)

# Getting final confirmation and running. Happy downloading!
# Try to do this in a screen.
conf = raw_input("Does this look ok? ")
if conf[0].lower() == "y":
    processCommands(commands)
else:
    print("Ok, not running.")

