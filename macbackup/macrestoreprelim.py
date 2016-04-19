# This is the automatically generated macrestore.py file.

files_to_restore = "./restorecommands.txt"

import os

print
print("This is the automatically generated macrestore.py file.")
print("----------------------------------------------------------------------------")

commands = []

f = open(files_to_restore, "r")
for line in f:
    commands.append(line)

print("These commands will be run:")
for command in commands:
    print(command)
    
if(raw_input("Proceed? ").lower()[0] != "y"):
    print("Ok, will not run.")
else:
    print("Running restore commands...")
    for command in commands:
        print(command)
        os.system(command)
    f.close()
    print("All done.")
    print