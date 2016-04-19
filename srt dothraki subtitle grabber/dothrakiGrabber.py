import pysrt
from os import walk

"""
Selects the only srt file in the directory if none is given.
"""

f = []
for (dirpath, dirnames, filenames) in walk("."):
    f.extend(filenames)
    break

srts = []
for i in f:
    if i[-4:] == ".srt":
        srts.append(i)
        
def getInput():
    if len(srts) == 1:
        return srts[0]
    print "Options: "
    for i in range(1, len(srts)+1):
        print "[%s]. %s" % (i, srts[i-1])

    targetAnswer = raw_input("Which .srt file do you want to get Dothraki from? ")
    try:
        targetAnswer = int(targetAnswer)
    except:
        print "Invalid input. Please just select one of the numbers."
        getInput()

    if targetAnswer in range(0, len(srts)+1):
        return srts[targetAnswer - 1]
    else:
        print "That wasn't a valid option. Try again from the available numbers."
        getInput()

target = getInput()

subs = pysrt.open(r"%s" % target)
print "Opened " + target

outputSubs = []

end = len(subs) - 1

for num in range(0, end):
    if "[Speaks Dothraki]" in subs[num].text:
        print(subs[num].text)
        outputSubs.append(subs[num])

for i in outputSubs:
    print i

#outputName = "".join(target.split(".")[:-1]) + ".mkv"
#print outputName

titleRaw = target.split(".")[4:-1]
i = 0
title = ""
while titleRaw[i] != "720p":
    title += " " + titleRaw[i]
    i += 1
    
outputName = "Game of Thrones " + target.split(".")[3] + " - " + title + ".srt"
print outputName

subs = pysrt.SubRipFile(outputSubs)
subs.save(outputName)
