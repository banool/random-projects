import re
from datetime import date
from os import walk, makedirs
from os.path import exists, isfile, join
from shutil import move, copy
 

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

start = "samplefolder"

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


"""
Can return 4 cases: TVShow, Movie, Music and Unknown.
TVShow: [name of the show, season, episode, extra information, extension]
Movie: [name of the movie, year it was made, extension]
Music:
Unknown: Returns a string saying that it didn't work for this file.
"""
def name_format(path):
    # Not running on things like "sample.avi"    
    name = path.split("\\")[-1].lower()
    if(comp([name], ignore_list) > 0):
        return "ignored: " + path
    
    oneup = path.split("\\")[-2].lower()
    # Because not all of them will have a two up folder.
    twoup = False
    try:
        twoup = path.split("\\")[-3].lower()
    except:
        pass
    split_name = re.split("\W+", name)
    
    # Filtering out stuff like x264 (but only on strings that are 3
    # or more characters long, so we don't cut out things like "2".
    split_name = [x.lower() for x in split_name if comp([x], 
                  filter_list) == False or len(x)<3]
    ext = split_name[-1]
    # Checking if the file is a video
    if(ext in video_ext_list):
        # Checking if the video is a TV show
        tvresults = interpret_seasonep(split_name)
        # interpret_seasonep returns -1 if it couldn't make it seasonep format.
        if(tvresults[0] >= 0):
            name = " ".join(split_name[0:tvresults[0]]).title()
            season = tvresults[1][0]
            episode = tvresults[1][1]
            extra = " ".join(split_name[tvresults[0]+1:-1]).title()
            return ("TVShow", [name, season, episode, extra, ext])

        # Checking if the season info is held in an above folder.
        elif "season" in oneup:
            split_oneup = re.split("\W+", oneup)
            bemes = 0
            for i in range(len(split_oneup)):
                if("season" in split_oneup[i]):
                    break
            try:
                season = int(split_oneup[i+1])
                bemes = i
            except:
                print "Folder name ending with season wtf?"
                return "Unknown"
            
            if(twoup and twoup != start):
                # E.g. Adventure time/season 2/episode 3
                # Also makes sure that the twoup isn't just the root folder.
                name = twoup.title()
            elif(len(split_oneup) > 2 and "season" in split_oneup):
                # E.g. Adventure time season 2/episode 3
                name = " ".join(split_name[0:i]).title()
            else:                   
                # E.g. Adventure time season 3 episode 2
                # Though this should be picked up by the first if statement.
                name = " ".join(split_name[0:bemes+1]).title()
            for i in range(len(split_name)):
                if("episode" in split_name[i] or "ep" == split_name[i]):
                    break
            try:
                episode = int(split_name[i+1])
            except:
                return "Unknown"
            extra = " ".join(split_name[i+2:-1]).title()
            return ("TVShow", [name, season, episode, extra, ext])
        elif "season" in name and "episode" in name:
            bemes = 0
            for i in range(len(split_name)):
                if("season" in split_name[i]):
                    break
                    bemes = i
            for j in range(len(split_name)):
                if("episode" in split_name[j]):
                    break            
            try:
                season = int(split_name[i+1])
                episode = int(split_name[j+1])
            except:
                print "File name ending with season/episode wtf?"
                return "Unknown"

            if(oneup != start):
                name = oneup.title()
            else:
                name = " ".join(split_name[0:bemes+1]).title()
            extra = " ".join(split_name[j+2:-1])
            return ("TVShow", [name, season, episode, extra, ext])
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
            return ("Movie", [name, year, ext])
    # Checking if it is then music
    elif(ext in music_ext_list):
        # metadata is used mainly for this, don't sweat it.
        return ("Music" + path)
    else:
        return "Other: " + path
        #return "unknown. maybe dont move these ones but just log them"

actions = [("make", join(start, "Movies")), ("make", join(start,"TV Shows")), ("make", join(start,"Music"))]

# First actual call to anything starts here
print "Processing..."

for root, dirs, files in walk(start, topdown=True):
    for name in files:
        path = join(root, name)
        res = name_format(path)
        if res[0] == "TVShow":
            show_path = join(start, "TV Shows", res[1][0])
            show_action = ("make", show_path)
            if show_action not in actions:
                actions.append(show_action)
            
            name = res[1][0]
            seasonep = "s%02de%02d" % (res[1][1], res[1][2])
            extra = ""
            if res[1][3]:
                extra = " - " + res[1][3]
            ext = res[1][-1]
            
            new_name = "%s - %s%s.%s" % (name, seasonep, extra, ext)
            season = "Season " + str(res[1][1])
            season_path = join(show_path, season)
            season_action = ("make", season_path)
            if season_action not in actions:
                actions.append(season_action)
            new_path = join(season_path, new_name)
            actions.append(("move", [path, new_path]))
        elif res[0] == "Movie":
            name = res[1][0]
            year = res[1][1]
            ext = res[1][2]
            new_name = "%s (%s)" % (name, year)
            folder_path = join(start, "Movies", new_name)
            folder_action = ("make", folder_path)
            if folder_action not in actions:
                actions.append(folder_action)
            new_name = new_name + "." + ext
            new_path = join(folder_path, new_name)
            actions.append(("move", [path, new_path]))
        
# Can either make a folder or move something.
# move syntax is ("move", [old, new]
# make syntax is ("make", #folder path#)
def print_actions():
    print "\nActions to be performed:\n****************************************"
    for i in range(len(actions)):
        if actions[i][0] == "make":
            print str(i) + " Make: " + actions[i][1]
        elif actions[i][0] == "move":
            print str(i) + " Move: %s --> %s" % (actions[i][1][0], actions[i][1][1])
        else:
            print actions[i][1] + " is not a valid option."
            actions.pop(i)


def do_actions(actions):
    for action in actions:
        if action[0] == "make":
            if not exists(action[1]):
                makedirs(action[1])
            else:
                print "The folder:    %s already exists." % (str(action[1]).ljust(50))
        else:
            old = action[1][0]
            new = action[1][1]
            old_good = isfile(old)
            new_good = isfile(new)
            if (old_good == True and new_good == False):
                copy(old, new)
            elif(new_good == True):
                print new + " already exists."
            else:
                "The file " + old + " cannot be found."

print_actions()

def getresponse():
    response = raw_input("\nType (Y)es if you are happy to execute these actions,\nor (N)o if you want to change something: ")[0].lower()
    if response == "y":
        do_actions(actions)
        pass
    elif response == "n":
        to_remove = raw_input("\nEnter a number or list of numbers (separated by spaces) corresponding\nto the actions to remove: ")
        to_remove = sorted(to_remove.split(), reverse=True)
        for item in to_remove:
            try:
                item = int(item)
                actions.pop(item)
            except:
                print "Only numbers separated by spaces please."
                getresponse()
                break
        print_actions()
        getresponse()
    else:
        print "Please enter y or n"
        getresponse()

getresponse()


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