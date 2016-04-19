"""
Upon a reformat or whatever, this python script will copy all those
small files you may have forgotten to backup into one place.
It does this copying by calling the system cp function.

Note that python can't follow ~, so the code replaces that with
/Users/[username]/
As such the correct username for the system needs to be in username.

It also creates a restore file which puts each of the backed-up files 
to back where they were originally found from.
"""

import os 
import os.path

files_to_copy = "./copyfiles.txt"
username = "daniel"
    
print
print("MacBackup is copies easily forgotten files into ./backup/")
print("It also makes a python script that will copy them back to where they were found.")
print("----------------------------------------------------------------------------")

f = open(files_to_copy, "r")

commands = []
reverse = []

for line in f:
    name_t = line[0]
    name = line[2:]
    if(name[0] == "~"):
        name = "/Users/" + username + "/" + name[2:]
    endname = (name.split("/"))[-1]
    if(name_t == "f"):
        # File
        if(os.path.exists(name)):
            commands.append('cp "%s" "./backup/%s"' % (name , endname))
            reverse.append('cp "./%s" "%s"' % (endname , name))
        else:
            print('The file "%s" cannot be found.' % name.rstrip('\n'))
    elif(name_t == "d"):
        # Directory/Folder
        if(os.path.exists(name)):
            commands.append('cp -r "%s" "./backup/%s"' % (name , endname))
            reverse.append('cp -r "./%s" "%s"' % (endname , name))
        else:
            print('The directory "%s" cannot be found.' % name.rstrip('\n'))


print("These commands will be run:")
for command in commands:
    print(command)
print("--------")

if(raw_input("Proceed? ").lower()[0] != "y"):
    print("Ok, will not run.")
else:
    print("Making backup folder...")
    os.system("mkdir backup")
    print
    print("Running commands:")
    for command in commands:
        print(command)
        os.system(command)
    print
    print("Closing %s..." % files_to_copy)
    f.close()
    
    print
    print("Writing ./backup/restorecommands.txt")
    os.system("touch ./backup/restorecommands.txt")
    f = open("./backup/restorecommands.txt", "w")
    for command in reverse:
        f.write(command + '\n')
    print("Closing ./backup/restorecommands.txt")
    f.close()
    
    print
    print("Writing ./backup/macrestore.py")
    os.system("cp ./macrestoreprelim.py ./backup/macrestore.py")
    print("Closing ./backup/macrestore.py")
    
    print
    print("Zipping up the backup...")
    os.system("zip -r -X backup.zip ./backup > /dev/null")
    print
    
    
    print("All done.")
    print
    
