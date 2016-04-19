#!/usr/bin/python3

import os
from shutil import rmtree
from sys import exit

"""
Ok so how this works is when Google Drive decides that it's found a
duplicate, what it will do is get the original name of the item and
append a space and a (1) to it, like so:

Directory: Folder    and Folder (1)
File:      hello.txt and hello (1).txt

So we're essentially hunting these files and folders with a (1) on
the end of them and deleting them.

From my understanding, the original and usually complete version of
the file/folder will be the one without the (1) on the end of it.
If everything goes to shit with deleting it, remember that the files
should still be there in your Google Drive web app in the Trash folder.

Daniel Porteous
danielporteous1@gmail.com
07/07/15
"""

start = "."
end = "(1)"
len_neg = -len(end)


problems = []

for root, dirs, files in os.walk(start):
    current = []

    for dir in dirs:
        current.append(dir)
    for item in current:
        #print(item[:-4])
        if item[:len_neg-1] in current and item[len_neg:] == end:
            problems.append(os.path.join(root, item))

    current = []
    for file in files:
        current.append(file)
    no_exts = []
    for item in current:
        with_ext = item.split(".")
        if len(with_ext) > 1:
            no_exts.append("".join(with_ext[:-1]))

    for item in current:
        with_ext = item.split(".")
        if len(with_ext) > 1:
            no_ext = "".join(with_ext[:-1])

            if no_ext[:len_neg-1] in no_exts and no_ext[len_neg:] == end:
                problems.append(os.path.join(root, item))

if len(problems) == 0:
    print("No duplicates found, perhaps make sure that the ending specified is correct for your system?\nTerminating...")
    exit(0)

print("===== These are the duplicates =====")
for i in range (0, len(problems)):
    print(i, problems[i])
print("===== These are the duplicates END =====")

del_str = input("Enter the numbers above of any items you don't want deleted. Otherwise just press enter.\nSeparated by spaces! >>> ")
if len(del_str) == 0:
    pass
else:
    del_from_list = [int(x) for x in del_str.split(" ")]

    count = 0
    deleted = []
    for num in del_from_list:
        deleted.append(problems.pop(num - count))
        count += 1

    print("===== These are the duplicates =====")
    for i in range (0, len(problems)):
        print(i, problems[i])
    print("===== These are the duplicates END =====")

    print("===== These are the items that were removed from the deletion list =====")
    for item in deleted:
        print(item)
    print("===== These are the items that were removed from the deletion list END =====")


confirm = input("Would you finally like to delete these items (y or n)? ")[0].lower()
if confirm == "y":
    for item in problems:
        try:
            rmtree(item)
        except NotADirectoryError:
            os.remove(item)
        except Exception as e:
            print("Unexpected error:\n%s\nTerminating..." % (str(e)))
            exit(1)
else:
    print("Ok, terminating...")

print("Done!")
