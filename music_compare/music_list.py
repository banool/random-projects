#!/usr/local/bin/python3

"""
This script exists because iTunes does all kinds of nonsense with files when
they are added automatically into iTunes. As such, it is not feasible to
check which files exist on each end each time I want to copy music across
from the server. To get around this, a manual record of which files have
been copied across is maintained, which has gradually improved over time.
The automatically adding to iTunes has its advantages however. Even if single
files are dumped into the Automatically Add to iTunes folder, if you have the
option enabled iTunes will organise them by Artist -> Album. Very handy.

See the changelog on Github and below to know what has been added over time
to this script and why. Perhaps feature creep, but really many of these changes
have been beneficial to the maintenance of this code, not detrimental.

Note two main limitations of this script.
1. It doesn't handle non UTF-8 characters, such as if ke$ha was in the path.
2. .flac files are not handled uniquely, despite iTunes not accepting them.
   Perhaps in future I will add support to have them copied elsewhere for
   converting to .alac.
                             Update 07/05/15:
   .flac files are now moved into a separate folder so they can be
   converted and added manually.
   Note that the .flac file name from the remote location will be added
   to the record file. Whatever you do with the flac file from that point
   is irrelelvant. So don't be worried about deleting them after converting
   them to mp3 files and adding them to iTunes.

Version 2:
It turns out that iTunes butchers some of the file names as they come in:
09 - Momma - Kendrick Lamar.mp3 to 09 Momma.mp3
As such, a seperate record of music copied needs to be made.

However this doesn't actually crawl the local files, just the record file that
is appended to when new music is added. As such, it is important that when
this script is run, the operation is allowed to go to completion.

Additional note: As stated, the record file checks if files have already been
added based on the naming scheme of the remote system (in order to deal with
iTunes butchering the filenames of the local files). However, this obviously
means that if any butchering of the filenames (specifically the filenames,
the path can change) on the remote system will result in this script no
longer working yet again. Keep this in mind.

Update 06/06/16:
Script now handles a KeyboardInterrupt cleanly. Informs the user that nothing
was changed (this is how it functioned previously too).

Update 06/09/15:
After having to recreate the server from scratch, I struggled a little with
restoring things to how they were. Here's a quick guide:

On the server, make sure you've followed this guide for TimeMachine first:
http://dae.me/blog/1660/concisest-guide-to-setting-up-time-machine-server-on-ubuntu-server-12-04/

Once done, head to your config file for netatalk here:
sudo nano /etc/netatalk/AppleVolumes.default
And add this line:
/media/hddroot/music iTunes_Server options:tm volsizelimit:500000 allow:daniel

Make sure that daniel has user permissions on this folder por supuesto.
Should be good from here to use this script.

Update 07/11/15:
Recently a method was added to test for if the drive has been mounted by smb
instead of afp. As a further extension of that, I've now implemented a method
that will attempt to mount the drive itself via smb if it hasn't been manually
mounted by the user using afp or smb.

Credit: http://stackoverflow.com/questions/21590361/mount-windows-smb-shares-on-a-mac-using-python

Update 10/05/16:
Adds .wav files to the flac_files folder since iTunes can't handle their 
metadata properly either. The are probably other file formats which should also 
be handled separately. A more extensible approach might be to have two lists, 
one for supported and one for not.

Update 10/06/16:
Significant performance improvement implemented. In crawl(), each of the folders 
in the base startlocation are checked to see if they have changed since last we 
checked and only these are crawled. To support this, the time of last check in
UNIX epoch time is put at the top of the record.txt file. This change has 
resulted in an enormous decrease in time spent on disk reads (and minor 
computation). Also cleaned up the logic of crawl() calls a bit, but that code 
block is still very messy.

Update 02/07/16:
Big code clean up implemented. The super ugly and unmaintainable nested loop for
trying to mount the remote drive by the 3 main different methods (smb auto, smb 
manual, afp manual) was replaced with a higher order function which processed 
the three different methods separately (meaning that each method was pulled out
into its own function). This function is called mountAndCrawl() and it solves
a lot of the code duplication that was running rampant in the script beforehand.
The checks for which OS you were running on and their respective global
variables were removed since this script has only ever really worked on OS X /
macOS Darwin.

Update 26/07/16:
Noticed some undesirable behaviour. When the script found items but the user 
chose not to do anything with them, on the next execution of the script those 
items were ignored because of the updated timestamp. This could indeed be what 
the user wants, having decided that they don't want those items. However, it 
might not be. As such, in the case that no items were selected to be 
transferred, the script will ask if they want to update the timestamp. Perhaps 
this should be implemented for any time the timestamp is updated, but I think 
this is the most outstanding case to sort out. See NOTE1 below for the relevant 
code snippet.

Update 28/07/16:
Added a method which tries to mount the remote drive via SSH automatically. 
I was encouraged to do this after SMB didn't work following restoring the 
server. It turns out that I needed to do this for the account that I wanted to 
access the samba share as to give it a password: smbpasswd -a daniel
While not a big deal, it indeed highlights how SSH is just that much more 
reliable. Also moved my password from this source code into an environmental 
variable. A bit remiss now I know.

Update 13/10/16:
Upon running into the "rare case" (ctrl+F for it), I found that when using the 
automatic SMB mount function, and then cancelling before fully finishing 
execution, it wasn't properly unmounting the drive This lead me to look for a 
different way to handle the interruption, so now a global signal handler has
been implemented. This removes the need to check throughout the code, and should 
work well, except for maybe very early in the script when the mount location 
hasn't yet been defined. For context, this has become necessary because the 
automatic SSH mount is broken in macOS Sierra.

Update 28/10/16:
The script can now automatically convert flac and wav files using this library:
https://github.com/jiaaro/pydub
It will convert them to mp3, add them to the Automatically Add to iTunes folder
and delete the original flac files (locally, not remotely of course).
Considering that this adds another yes/no question, I've added a check at the
start to see if you just want to say yes to everything. The same effect could be 
reached by just piping yes into this script, but this is still nice.
"""

import os
from subprocess import call
from sys import exit
import platform
from time import ctime, time
import signal # So we can catch ctrl + C globally
from pydub import AudioSegment
from pydub.utils import mediainfo

mp3Bitrate = "320k"

print()
yesToAllConf = input("Say yes to everything? ")[0].lower()
yesToAll = False
if yesToAllConf == "y":
    yesToAll = True
print()

def unmount():
    umountCommand = "umount %s && rm -R %s" % (mountLocation, mountLocation)
    os.system(umountCommand)
    print("Unmounted the remote drive.")

def keyboard_interrupt(signal, frame):
    print()
    unmount()
    print("Keyboard interrupt received. Nothing was changed.\nTerminating...")
    exit(0)

# Telling the program to run the keyboard_interrupt() function upon 
# receiving ctrl+C (SIGINT).
signal.signal(signal.SIGINT, keyboard_interrupt)

system = platform.system()

ext_fname = "extensions.txt"
instructions_fname = "instructions.sh"
#timezoneOffset = 10 * 60 * 60 # Dirty timezone hack for GMT +10. 
# Update: Not actually necessary.
timezoneOffset = 0

# TODO this shouldn't be necessary, crawl is starting one dir too high up.
excludedDirs = ["Album Artwork", "AppleDouble", "DS_Store", ".AppleDouble", 
    ".DS_Store"]

if system != "Darwin":
    print("OS must be OSX, terminating...")
    exit()

base_local = "/Users/daniel/Music/iTunes"
base_remote = "/Volumes/iTunes_Server"
base_remote_smb = "/Volumes/Music"
start_local = base_local + "/iTunes Media"
auto_add_location = "/Users/daniel/Music/iTunes/iTunes Media/Automatically Add to iTunes/"
record_location = "/Users/daniel/Music/iTunes/record.txt"
flac_ending = "/flac_files/"





def get_extensions(fname, decode_y):
    output = []
    output2 = []
    with open(fname, "rb") as f:
        output = f.readlines()
    for i in output:
        if decode_y:
            output2.append(i.decode("utf-8").rstrip('\n'))
        else:
            output2.append(i.decode("utf-8").rstrip('\n'))
    return output2

def crawl(start, exts, excludedDirs, lastCheckTime):
    output = []

    if os.path.isdir(start):
        pass
    else:
        return -1

    print("Crawling remote...")
    changed = []

    # Recurse through each dir and check if they were made after the
    # last time we checked the record (UNIX epoch time).
    for i in os.listdir(start):
        if int(os.path.getmtime(start+"/"+i)) > lastCheckTime and i not in excludedDirs:
            changed.append(i)

    if (len(changed)) > 0:
        print("Folders changed since last music pull:")
        for folder in changed:
            print("  " + folder)

    # Call os.walk on each of the folders that has changed since last time.
    try:
        for folder in changed:
            for root, dirs, files in os.walk(start+"/"+folder, topdown=True):
                # Excluding certain directories from crawling. 
                # Update 18/05/16: Not sure this does anything.
                dirs[:] = [d for d in dirs if d not in excludedDirs]
                for file in files:
                    if file.split(".")[-1] in exts:
                        output.append( (file, root+"/"+file) )
    except Exception as e:
        print("Unexpected error: %s" % str(e))
        return -1
    return output

# Returns paths of files to add from remote folder to local.
def comp(list1, list2):
    print("Comparing against current local music:")
    output = []
    output_names = []
    for val in list1:
        if val[0] not in list2:
            if ".AppleDouble" not in val[1] and "DS_Store" not in val[1]:
                output.append(val[1])
                output_names.append(val[0])
    return (output, output_names)

# Getting list of local files from record.txt
# Uses get_extensions. If no record.txt, it copies all the files over.
record_output = []
if(os.path.isfile(record_location)):
    local = get_extensions(record_location, False)
    print("Local record file found with %s items" % str(len(local)))
    # We get the time the record was last written (UNIX epoch time).
    lastCheckTime = int(local[0])
else:
    # If no local record just make local list empty.
    # We will make a new record when we do write at the end.
    print("No local record file, copying all music over.")
    local = []
    # Folders made before epoch will be problematic here/
    lastCheckTime = 0

# Re-add previous record lines with new (current) UNIX epoch timestamp.
record_output.append(str(int(time()) + timezoneOffset) + "\n")
for i in local[1:]:
    record_output.append("%s\n" % i)

music_exts = get_extensions(ext_fname, True)





# Variables for attempting to mount the drive automatically.
mountLocation = "/Users/daniel/Desktop/tempmount"
username = "delugeuser"
password = os.environ["SMBPWORD"]
remoteServerName = "server"
remoteDirName = "Music"
remoteServerSSH = "192.168.1.2"
remoteDirSSH = "/media/hddroot/music"

def mountAutomaticallySSH():
    """ 
    Tries to mount vis SSH automatically.
    Should only ask for password if key based auth fails.
    """
    start_remote = mountLocation + "/iTunes Media/Music"

    print("Trying to mount automatically via SSH.")
    if not os.path.exists(mountLocation):
        os.makedirs(mountLocation)

    args = (username, remoteServerSSH, remoteDirSSH, mountLocation)
    mountCommand = "sshfs -p 25566 %s@%s:%s %s" % args
    
    status = call(mountCommand, shell=True)
    if status != 0:
        return -1

    print("Mounted via SSH automatically to " + mountLocation)

    return crawl(start_remote, music_exts, excludedDirs, lastCheckTime)

# Moved this down one in the chain. Will try using ssh first now.
def mountAutomaticallySMB():
    """
    Tries to mount the remote drive via SMB itself before crawling it.
    """
    start_remote = mountLocation + "/iTunes Media/Music"

    print("Trying to mount automatically via SMB.")
    # Note, this snippet doesn't work if the path is given with ~ in it. 
    # Have to use either an absolute or directory relative path.
    if not os.path.exists(mountLocation):
        os.makedirs(mountLocation)

    args = (username, password, remoteServerName, remoteDirName, mountLocation)
    mountCommand = "mount_smbfs //%s:%s@%s/%s %s" % args

    status = call(mountCommand, shell=True)
    if status != 0:
        return -1

    print("Mounted via SMB automatically to " + mountLocation)

    return crawl(start_remote, music_exts, excludedDirs, lastCheckTime)

def mountManuallySMB():
    """ 
    Tries to crawl a remote drive which was already manually mounted via SMB.
    """
    start_remote = base_remote_smb + "/iTunes Media/Music"

    print("Trying to access the remote drive via manual SMB mount.")

    ret = crawl(start_remote, music_exts, excludedDirs, lastCheckTime)
    if ret == -1:
        print("rare case")
        # Deals with the rare case that the remote dir was already mounted by this script
        # but was then aborted (and is hence not under /Volumes) but also not unmounted.
        # This shouldn't ever really trigger.
        start_remote = mountLocation
        return crawl(start_remote, music_exts, excludedDirs, lastCheckTime)
    else:
        return ret

def mountManuallyAFP():
    """
    Tries to crawl a remote drive which was already manually mounted via SMB.
    """
    start_remote = base_remote + "/iTunes Media/Music"

    print("Trying to access the remote drive via manual AFP mount.")

    return crawl(start_remote, music_exts, excludedDirs, lastCheckTime)





# This takes a bunch of functions and tries them one by one until the remote 
# drive is mounted successfully.
def mountAndCrawl(*funcs):
    result = 0
    i = 0
    # The functions will return a list on success, or a number indicating what
    # went wrong in the event of an error / interruption.
    while type(result) is int:
        result = funcs[i]()
        if type(result) is int:
            print("Failure, trying next mounting method...")

        i += 1
        if i == len(funcs):
            break

    # This only triggers after trying all functions unsuccessfully.
    if type(result) is int:
        return -1

    # Should be a list in the event of success.
    print("Success!")
    return result


mountingFunctions = [mountAutomaticallySSH, mountAutomaticallySMB, mountManuallySMB, mountManuallyAFP]
remote = mountAndCrawl(*mountingFunctions)
# Checking that the remote drive was successfully mounted and crawled.
if remote == -1:
    print("None of the methods were successful in mounting and crawling the remote drive.")
    print("Exiting...")
    exit()


# Isolating the two lists returned from comp. The first are the full paths.
# The second, extracted further below, is just the file names.
comp_output = comp(remote,local)
diff = comp_output[0]

"""
Added on 07/05/15. Dealing with .flac and .wav files
Checks the differences and adds them to a folder in
the iTunes Media folder: iTunes Media/flac_files.
These can then be converted to mp3 or maybe aiff.
"""
diff_flac = []
diff_flac_clean = []
# This relies on the indices of the two arrays returned
# by comp alligning perfectly (which they should).
counter = 0
end = len(diff)
while counter < end:
    if diff[counter][-4:] == "flac" or diff[counter][-3:] == "wav":
        diff_flac.append(diff.pop(counter))
        diff_flac_clean.append(comp_output[1].pop(counter))
        end -= 1
    else:
        counter += 1
        """
        Note: We only incrememnt the counter when we don't pop. Because pop 
        returns the item at the given index AND deletes it, if we increase the 
        counter after popping we will skip a value. When we DO pop we decrease 
        the required end counter, since the list is now one item smaller.
        """

if len(diff) == 0 and len(diff_flac) == 0:
    print("There were no differences, exiting.")
    # Writing record as it was before but with new timestamp.
    with open(record_location, "w") as f:
        f.writelines(record_output)
    unmount()
    exit()

confirm1 = "n"
if(len(diff) > 0):
    for i in comp_output[1]:
        print(i)
    print("\n")
    print("%s non_flac files were found in the remote server, but not locally." % str(len(diff)))
    if yesToAll:
        confirm1 = "y"
    else:
        confirm1 = input("Would you like to add them? ")[0].lower()
        if confirm1 != "y":
            print("Ok, not adding non_flac files. Moving on to check .flac files...")

# We create an .sh file to do the copying so the shell can do it.
# Probably more reliable than letting python do it.
print("Creating %s file..." % instructions_fname)

instructions = []
for i in diff:
    instructions.append("""cp "%s" "%s"\n""" % (i, auto_add_location))

"""
Checking if we want to copy the .flac files to a seperate folder or just have 
them ignored.
"""
confirm2 = "n"
if len(diff_flac) > 0:
    for i in diff_flac_clean:
        print(i)
    print("\n")
    if yesToAll:
        confirm2 = "y"
    else:
        confirm2 = input("There were %s .flac or .wav files found.\nWould you like to add them to %s? " % ((str(len(diff_flac)), base_local + flac_ending)))[0].lower()
    if confirm2 != "y":
        print("Ok, ignoring .flac and .wav files.")
    else:
        print("Adding commands to copy the .flac and .wav files to %s to %s" % (base_local + flac_ending, instructions_fname))
        os.system("mkdir -p '%s'" % base_local + flac_ending)
        for i in diff_flac:
            instructions.append("""cp "%s" "%s"\n""" % (i, base_local + flac_ending))
else:
    print("No .flac or .wav files found, continuing...")

if confirm1 != "y" and confirm2 != "y":
    print("Neither non-flac nor flac/wav options were accepted. Exiting.")
    """
    Writing record as it was before but with new timestamp.
    
    NOTE1, interesting trade off here.
    If you write the timestamp here, it lets the script know that you've 
    checked up to this point. This is good if nothing was found as it will 
    scan for folders in a smaller time window next time. However if something
    was found but then not added, the next time the script is run it will
    not pick up those items, meaning the user has to manually change the 
    timestamp to an earlier time.
    
    As such, in this situation the script will now ask the user if they want 
    to update the timestamp.
    """
    timestampConf = "xxx"
    if yesToAll:
        timestampConf == "y"
    else:
        while timestampConf != "y" and timestampConf != "n":
            timestampConf = input("Would you like to update the timestamp in the record file? ")[0].lower()

    if timestampConf == "y":
        with open(record_location, "w") as f:
            f.writelines(record_output)
    
    unmount()
    exit()

with open(instructions_fname, "w") as f:
    f.writelines(instructions)

print("Would you like to execute %s now? Options:" % instructions_fname)
print("y - Yes, run %s and copy the files over"  % instructions_fname)
print("n - No, don't run %s and do nothing" % instructions_fname)
print("r - Don't run %s, but add the files to record.txt" % (instructions_fname))
if yesToAll:
    confirm = "y"
else:
    confirm = input("Select an option >> ")[0].lower()

# Exit and do nothing
if confirm == "n":
    print("Ok, exiting.")
    unmount()
    exit()

if confirm == "y":
    print("Executing %s" % instructions_fname)
    os.system("chmod +x %s" % instructions_fname)
    os.system("./%s" % instructions_fname)

# If you select r, it just continues from here, writing the record file.
print("Writing record.txt file.")

if confirm1 == "y":
    for item in comp_output[1]:
        record_output.append("%s\n" % item)
if confirm2 == "y":
    for item in diff_flac_clean:
        record_output.append("%s\n" % item)
with open(record_location, "w") as f:
    f.writelines(record_output)


# Copy the record.txt file here as well just incase we lose it.
os.system("cp '%s' ./" % record_location)
os.system("rm '%s'" % instructions_fname)

unmount()

# Converting flac / wav files to mp3.
confirm3 = "n"
if confirm2 == "y":
    if yesToAll:
        confirm3 = "y"
    else:
        confirm3 = input("Would you like to convert flac / wav files to mp3 and add them automatically? ")[0].lower()

#def getMetadata()

if confirm3 == "y":
    print("Converting flac / wav files to mp3")
    path = base_local + flac_ending
    files = []
    for i in os.listdir(path):
        ext = i.split(".")[-1]
        if ext == "flac":
            files.append((i, "flac"))
        if ext == "wav":
            files.append((i, "wav"))

    newExt = "mp3"

    for i in files:
        print("Converting " + i[0])
        audio = AudioSegment.from_file(path + i[0], i[1])
        metadata = mediainfo(path + i[0]).get("TAG", None)
        # Deals with weird case where there is title and TITLE, in which title is wrong.
        metadata["title"] = metadata["TITLE"]
        newName = i[0][:-(len(i[1])+1)] + "." + newExt
        newPath = auto_add_location + newName
        tempPath = newName
        audio.export(tempPath, format=newExt, bitrate=mp3Bitrate, tags=metadata)
        os.system(""" mv "{}" "{}" """.format(tempPath, newPath))
        os.system(""" rm "{}" """.format(path + i[0]))

print("Done!")
