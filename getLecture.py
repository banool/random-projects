#!/usr/bin/python3

"""
Place this in the root of your uni20xx folder.
This script decides upon the name for the next lecture for a given subject and downloads it.
"""

import os
import sys
import re
from urllib.request import urlretrieve

# The final int is for the number of lectures per week.
subjects = [("COMP30020", "Declarative Programming", 2), ("COMP30019", "Graphics and Interactions", 2), ("COMP30018", "Knowledge Technologies", 2)]

lectureFolder = "lectures"

dirs = os.listdir()

def getSubjectFolder():
	# Getting which subject the lecture belongs to.
	question = "Which subject does this lecture belong to?"
	for i in range(len(subjects)):
		print("[{}] {} - {}".format(i, subjects[i][0], subjects[i][1]))
	num = int(input("Enter a number: "))

	# Finding the appropriate folder.
	subject = subjects[num]

	# Using the subject code to find the appropriate folder.
	for i in dirs:
		if subject[0].lower() in i:
			subjectFolder = i
			break
	
	try:
		return (subject, subjectFolder)
	except NameError:
		print("There is a name mismatch between the subjects list and the folder names.")
		sys.exit(-1)

def getNextLectureName(subjectTuple, subjectFolder):

	lectureNameRegex = r"[a-zA-Z]{4}[0-9]{5}_week[0-9]{2}_lecture[0-9]_[0-9]{2}.m4v"

	lectures = []

	for i in os.listdir(os.path.join(subjectFolder, lectureFolder)):
		found = re.search(lectureNameRegex, i)
		if found:
			lectures.append(i)

	# Getting info for the first lecture. Should really just be 1 1 1.
	first = lectures[0].split("_")
	latestWeek = int(first[1][5:])
	latestLecture = int(first[2][7])
	latestLectureOverall = int(first[3][0:2])

	print("\nThese are the previous lectures:")
	for i in lectures:
		print(i)
		sp = i.split("_")
		week = int(sp[1][5:])
		lecture = int(sp[2][7])
		lectureOverall = int(sp[3][0:2])
		# Only update latestLecture if we're on the same week.
		if week == latestWeek:
			latestLecture = max(lecture, latestLecture)
		# Otherwise reset to 1.
		else:
			latestWeek = max(week, latestWeek)
			latestLecture = 1
		latestLectureOverall = max(lectureOverall, latestLectureOverall)

	# Checking if we roll over into a new week.
	if latestLecture == subjectTuple[2]:
		latestWeek += 1
		latestLecture = 1
	else:
		latestLecture += 1

	latestLectureOverall += 1

	return "{}_week{}_lecture{}_{}.m4v".format(subjectTuple[0].lower(), str(latestWeek).zfill(2), latestLecture, str(latestLectureOverall).zfill(2))

subjectTuple, subjectFolder = getSubjectFolder()
newName = getNextLectureName(subjectTuple, subjectFolder)
print("\nThis is the name for the new lecture:")
print(newName)

conf = input("\nIs this acceptable? ")[0].lower()
if conf != "y":
	print("Ok, exiting.")
	sys.exit(0)

print()

while True:
	targetURL = input("Please enter the url for the lecture\nhere: ")
	if targetURL[:4] != "http":
		print("Try again. ", end='')
		continue
	else:
		break

# Progress bar code from here:
# https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

dlDest = os.path.join(subjectFolder, lectureFolder, newName)
print("Downloading the lecture to '%s'" % dlDest)

urlretrieve(targetURL, dlDest, reporthook)

print("\nDone!")