import re
from datetime import date
from os import walk, makedirs
from os.path import exists, isfile
from shutil import move
import os # to be removed
 

"""
with the greatest case of there being a folder with the movie inside it
as well as a bunch of other files
rename the folder and the movie file to be the same, then create a folder by
this name in the Movies folder and copy in the movie file
(there may be a sample file, in this case only rename and move the biggest file)
as such all superfluous shit will be left behind).
maybe also copy in any images (for artwork).
 

 

 

need a way to check inside the folder to decide if it is a tv show or a movie.
 

maybe just check the files and then ditch the old folders, instead making
new folders based off the name of the series.
if the shows inside have different naming schemes, maybe give the option to
choose which name you want to go for.
 

this will require a scanning phase and then a doing phase, though that was
always expected
 

 

 

does os walk go in to a folder first as deep as possible then recurses out?
maybe record the second up folder in a variable

prioritise file name and then the folder that it is in
"""
 

testname1 = "the.shawshank.redemption.1980.aXXo.720p.ac3.swag.mp4"
testname2 = "the Legend of koRRa S01e03.the.swaggening.mkv"
testname3 = "the.shawshank.redemption.1980.aXXo"
 

result1 = re.split("\W+", testname1)
result2 = re.split("\W+", testname2)
 

video_ext_list = ["mp4", "mkv", "avi", "wmv", "flv"]
music_ext_list = ["mp3", "flac", "aac", "wav"]
filter_list = ["axxo", "yify", "x264", "judas", "ac3"]
ignore_list = ["sample"]
 

# Checks if this one filename is that of a TV show.
# Returns (point at which the season was, and the season + ep)
# in the format: sXXeXX
# or -1 and 0.
def interpret_seasonep(split_name):
    for i in range(len(split_name)):
        section = split_name[i]
        # This just checks for the format sXXeXX
        if(len(section) == 6 and section[0] == "s" and section[3] == "e"):
            try:
                season = int(section[1:3])
                episode = int(section[4:6])
                # Catching the rare circumstance that the season or episode
                # is longer than 2 digits.
                if (season > 99) or (episode > 99):
                    return (-1, 0)
                return (i, (season, episode))
            except:
                pass
    # Only returns False once it has checked every bit of the filename
    # for the previously stated seasonXXepisodeXX type format
    return (-1, 0)
 
# "s%02de%02d" % (season, episode)
 

def get_year(query):
    """ this is all very slow and usually unsuccessful
    from requests import get
    key = "XLPAPH-RG33L3866E"
    call = "http://api.wolframalpha.com/v2/query?input="+query+"&appid="+key
    data = get(call)
    status_code = int(data.status_code)
    if status_code == 200:
        print data.text
        #if(is there a year there?):
            # return the year that is there
    """
    return str(date.today().year)

def comp(list1, list2):
    strength = 0
    for val1 in list1:
        for val2 in list2:
            if (val1.lower() in val2.lower()) or (val2.lower() in val1.lower()):
                strength += 1
    return strength
    

# Can return 4 cases: TVShow, Movie, Music and Unknown
# Returns this in a tuple with the correct naming scheme.
# return type with name of show, season, episode, extras and file extension
# year for movies
def name_format(path):
    isfolder = False
    # Not running on things like "sample.avi"
    if(comp([path], ignore_list) == 0):
        return "ignored: " + path
    
    fname = path.split("\\")[-1].lower()
    oneup = path.split("\\")[-2].lower()
    # Because not all of them will have a two up folder.
    try:
        twoup = path.split("\\")[-3].lower()
    except:
        pass
    split_name = re.split("\W+", fname)
    
    # Filtering out stuff like x264 (but only on strings that are 3
    # or more characters long, so we don't cut out things like "2".
    split_name = [x.lower() for x in split_name if comp([x], 
                  filter_list) == False or len(x)<3]
    ext = split_name[-1]
    # Checking if the file is a video
    if(ext in video_ext_list):
        # Checking if the video is a TV show
        tvresults = interpret_seasonep(split_name)
        # inrepret_seasonep returns -1 if it couldn't make it seasonep format.
        if(tvresults[0] >= 0):
            name = " ".join(split_name[0:tvresults[0]]).title()
            season = tvresults[1][0]
            episode = tvresults[1][1]
            results = name + " - " + seasonep
            extra = " ".join(split_name[tvresults[0]+1:-1]).title()
            if extra:
                results = results + " - " + extra
            if isfolder == False:
                results = results + "." + split_name[-1]
            return ("TVShow", [name, season, episode, extras, ext])
        #CHECK IF THERE IS A SEASON 1 FOLDER IN IT FOR EXAMPLE.
        #but do not check for files
        elif "season" in oneup:
            split_oneup = re.split("\W+", oneup)
            i = 0
            for i in range(len(split_oneup)):
                if("season" in split_oneup[i]):
                    break
            print split_oneup[i+1]
            return "Season: " + path
        # If not a TV show then it must be a movie
        else:
            year_point = -1
            # Checking for a year already in the right format
            for i in range(len(split_name)):
                section = split_name[i]
                # Checking if there is a year in the title
                if(len(section) == 4):
                    try:
                        int(section)
                        year = section
                        year_point = i
                    except: 
                        pass
            name = " ".join(split_name[0:year_point]).title()
            # Attempting to get the year that the movie was made in
            if year_point == -1:
                year = get_year(name)
            results = name + " (" + year + ")."
            if isfolder == False:
                results = results + split_name[-1]
            return ("Movie", results)
    # Checking if it is then music
    elif(ext in music_ext_list):
        # metadata is used mainly for this, don't sweat it.
        return "music: " + path
    else:
        return "else: " + path
        #return "unknown. maybe dont move these ones but just log them"
           
 

# Can either make a folder or move something.
# move syntax is ("move", [old, new]
# make syntax is ("make", #folder path#)
"""
actions = [("make", "Movies"), ("make", "TV Shows"), ("make", "Music")]
print "Actions to be performed:"
for i in range(len(actions)):
    if actions[i][0] == "make":
        print i + "Make"
 

def do_actions(actions):
    for action in actions:
        if action[0] == "make":
            if not os.path.exists(action[1]):
                os.makedirs(action[1])
            else:
                print "The folder " + action[1] + "already exists."
        elif action[0] == "move":
            if (isfile(action[1][0]) == True and isfile(action[1][1]) == False):
                move(action[1][0], action[1][1])
            else:
                print "The file " + action[1][0] + " cannot be found or " + action[1][1] + "already exists."
        else:
            "Unsupported action " + action[0] + ".\nOnly tanks 'make' or 'move'"
 

response = raw_input("Type (Y)es if you are happy to execute this actions, or (N)o if you want to change something: ")[0].lower()
if response == "y":
    do_actions(actions)
else:
    response = raw_input("Enter a number or list of numbers corresponding to the actions to remove\nright here: ")
 
"""

import os
swag = 0
"""
def scan(root):
    dir_list = os.listdir(root)
    for item_top in dir_list:
        content1_list = os.listdir(os.path.join(root, item_top))
        print item_top + ": "
        print content1_list

scan("samplefolder")
"""

start = "samplefolder"
for root, dirs, files in os.walk(start, topdown=True):
    if swag > 25:
        break
    swag += 1
    for name in files:
        print name_format(os.path.join(root, name))
        #print root
        #print(os.path.join(root, name))
    #for name in dirs:
    #    print(os.path.join(root, name))
    #print root
    
    #for name in files:
     #   print name_format(os.path.join(root, name))
    #for directory in dirs:
     #   print directory
    #if "season" in dirs:
        
# send the file into name_format to see if a seasonep can be interpretted.
# if not come back here and check the path

"""
print "root prints out directories only from what you specified"
print "dirs prints out sub-directories from root"
print "files prints out all files from root and directories"
print "*" * 20
from os.path import join, getsize
for root, dirs, files in os.walk('.'):
    if "season" in dirs.lower():
        print dir
    print root, "consumes",
    print sum([getsize(join(root, name)) for name in files]),
    print "bytes in", len(files), "non-directory files"
"""