#!/usr/local/bin/python3

"""
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
"""

import os
from sys import exit
import platform

system = platform.system()
print(system)

ext_fname = "extensions.txt"
instructions_fname = "instructions.sh"

# TODO this shouldn't be necessary, crawl is starting one dir too high up.
excludedDirs = ["Album Artwork"]

# Windows 7 using cygwin
if system == "CYGWIN_NT-6.1-WOW":
    print("Running inside Cygwin on Windows")
    start_local = r"C:\Users\daniel\Music\iTunes\iTunes Media"
    start_remote = r"\\SERVER\Music Top\iTunesMedia"
    auto_add_location = r"C:Users\daniel\Music\iTunes\iTunes Media\Automatically Add to iTunes"
    record_location = r"C:\Users\daniel\Music\iTunes\record.txt"
    flac_ending = "\\flac_files\\"
    print("Systems except Darwin don't work well currently, and have been disabled.\nExiting.")
    exit()
# Mac OSX 10.10
elif system == "Darwin":
    print("Running on the Mac.")
    base_local = "/Users/daniel/Music/iTunes"
    base_remote = "/Volumes/iTunes_Server"
    base_remote_smb = "/Volumes/Music"
    start_local = base_local + "/iTunes Media"
    # auto_add_location = "/Users/daniel/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized/"
    auto_add_location = "/Users/daniel/Music/iTunes/iTunes Media/Automatically Add to iTunes/"
    record_location = "/Users/daniel/Music/iTunes/record.txt"
    flac_ending = "/flac_files/"
# Windows in the cmd
elif system == "Windows":
    print("CANNY RUN ON WINDOWS.")
    start_local = "C:\\Users\\daniel\\Music\\iTunes\\iTunes Media"
    start_remote = "\\\\SERVER\\Music Top\\iTunesMedia"
    auto_add_location = "C:Users\\daniel\\Music\\iTunes\\iTunes Media\Automatically Add to iTunes"
    record_location = "C:\\Users\\daniel\\Music\\iTunes\\record.txt"
    flac_ending = "\\flac_files\\"
    print("Systems except Darwin don't work well currently, and have been disabled.\nExiting.")
    exit()
else:
    print("OS unrecognised, terminating...")
    exit()

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

def crawl(start, exts, excludedDirs):
    output = []

    if os.path.isdir(start):
        pass
    else:
        return -1

    try:
        print("Crawling remote...")
        for root, dirs, files in os.walk(start, topdown=True):
            # Excluding certain directories from crawling.
            dirs[:] = [d for d in dirs if d not in excludedDirs]
            for file in files:
                if file.split(".")[-1] in exts:
                    output.append( (file, root+"/"+file) )
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("Unexpected error: %s" % str(e))
        return -1
    return output

# Returns paths of files to add from remote folder to local.
def comp(list1, list2):
    print("Comparing against current local music.")
    output = []
    output_names = []
    #list2_names = [x[0] for x in list2]
    #print(list2)
    for val in list1:
        if val[0] not in list2:
            output.append(val[1])
            output_names.append(val[0])
    return (output, output_names)

# Getting list of local files from record.txt
# Uses get_extensions. If no record.txt, it copies all the files over.
record_output = []
if(os.path.isfile(record_location)):
    local = get_extensions(record_location, False)
    print("Local record file found with %s items" % str(len(local)))
    for i in local:
        record_output.append("%s\n" % i)
else:
    print("No local record file, copying all music over.")
    local = []
    os.system("""touch "%s" """ % record_location)

music_exts = get_extensions(ext_fname, True)


# Attempting to find the drive having been connected manually.
start_remote = base_remote + "/iTunes Media"
remote = crawl(start_remote, music_exts, excludedDirs)
if remote == -1:
    print("Couldn't find the remote dir via afp, trying smb.")
    start_remote = base_remote_smb + "/iTunes Media"
    remote = crawl(start_remote, music_exts, excludedDirs)
    if remote == -1:
        print("Couldn't find remote directory via afp or smb.\nMake sure you have used the browse option in the 'Connect to server' menu.\nAlternatively, mount the music dir via samba.\n")
        print("Attempting to mount the dir via smb automatically...\n")
    else:
        print("Found dir using smb.")
elif remote == 0:
    print("Keyboard interrupt received. Nothing was changed.\nTerminating...")
    exit(0)

# Attempting to connect the drive automatically
mountLocation = "/Users/daniel/Desktop/tempMount"
username = "daniel"
password = "stratakis5991"
remoteServerName = "SERVER"
remoteDirName = "Music"

print("Mounting //%s/%s via smb to %s" % (remoteServerName, remoteDirName, mountLocation))

# Note, this snippet doesn't work if the path is given with ~ in it. Have to
# user either an absolute or directory relative path.
if not os.path.exists(mountLocation):
    os.makedirs(mountLocation)
mountCommand = "mount_smbfs //%s:%s@%s/%s %s" % (username, password, remoteServerName, remoteDirName, mountLocation)

def unmount():
    umountCommand = "umount %s && rm -R %s" % (mountLocation, mountLocation)
    os.system(umountCommand)
    print("Unmounted the remote drive.")

os.system(mountCommand)
print("Mounted via smb automatically to " + mountLocation)

start_remote = mountLocation
remote = crawl(start_remote, music_exts, excludedDirs)


# Isolating the two lists returned from comp. The first are the full paths.
# The second, extracted further below, is just the file names.
comp_output = comp(remote,local)
diff = comp_output[0]

"""
Added on 07/05/15. Dealing with .flac files
Checks the differences and adds them to a folder in
the iTunes Media folder: iTunes Media/flac_files.
These can then be converted to mp3.
"""
diff_flac = []
diff_flac_clean = []
# This relies on the indices of the two arrays returned
# by comp alligning perfectly (which they should).
counter = 0
end = len(diff)
while counter < end:
    if diff[counter][-4:] == "flac":
        diff_flac.append(diff.pop(counter))
        diff_flac_clean.append(comp_output[1].pop(counter))
        end -= 1
    else:
        counter += 1
"""
Note: We only incrememnt the counter when we don't pop. Because pop returs
the item at the given index AND deletes it, if we increase the counter after
popping we will skip a value. When we DO pop we decrease the required end
counter, since the list is now one item smaller.
"""

if len(diff) == 0 and len(diff_flac) == 0:
    print("There were no differences, exiting.")
    unmount()
    exit()

confirm1 = "n"
if(len(diff) > 0):
    for i in comp_output[1]:
        print(i)
    print("\n")
    print("%s non_flac files were found in the remote server, but not locally." % str(len(diff)))
    confirm1 = input("Would you like to add them? ")[0].lower()
    if confirm1 != "y":
        print("Ok, not adding non_flac files. Moving on to check .flac files...")

# We create an .sh file to do the copying so the shell can do it.
# Faster than letting python do it.
print("Creating %s file..." % instructions_fname)

instructions = []
for i in diff:
    instructions.append("""cp "%s" "%s"\n""" % (i, auto_add_location))

"""
Checking if we want to move the .flac files to a seperate folder or just have them ignored.
"""
confirm2 = "n"
if len(diff_flac) > 0:
    for i in diff_flac_clean:
        print(i)
    print("\n")
    confirm2 = input("There were %s .flac files found.\nWould you like to add them to %s? " % ((str(len(diff_flac)), start_local+flac_ending)))[0].lower()
    if confirm2 != "y":
        print("Ok, ignoring .flac files.")
    else:
        print("Adding commands to copy the .flac files to %s to %s" % (start_local+flac_ending, instructions_fname))
        os.system("mkdir '%s'" % start_local+flac_ending)
        for i in diff_flac:
            instructions.append("""cp "%s" "%s"\n""" % (i, start_local+flac_ending))
else:
    print("No .flac files found, continuing...")

if confirm1 != "y" and confirm2 != "y":
    print("Neither non-flac nor flac options were accepted. Exiting.")
    unmount()
    exit()

with open(instructions_fname, "w") as f:
    f.writelines(instructions)

print("Would you like to execute %s now? Options:" % instructions_fname)
print("y - Yes, run %s and copy the files over"  % instructions_fname)
print("n - No, don't run %s and do nothing" % instructions_fname)
print("r - Don't run %s, but add the files to record.txt" % (instructions_fname))
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

os.system("cp '%s' ./" % record_location)
os.system("rm '%s'" % instructions_fname)

"""
# Copying the library file .xml to the remote location
local_lib = base_local + "/" + "iTunes Music Library.xml"
remote_lib = base_remote + "/" + "iTunes Music Library.xml"
os.system("cp '%s' '%s'" % (local_lib, remote_lib))
# Doing it for the .itl file. Not sure this is necessary tho.
local_lib = base_local + "/" + "iTunes Library.itl"
remote_lib = base_remote + "/" + "iTunes Library.itl"
os.system("cp '%s' '%s'" % (local_lib, remote_lib))
"""

unmount()

print("Done!")
