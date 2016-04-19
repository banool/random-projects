from os import walk
from os import remove
from shutil import rmtree
import itertools

start = "C:\Users\daniel\Google Drive"
ending = "(1)"

file_del = []
dir_del = []

def level_delete(root, ending):
    #print "watup"
    dirpath = []
    dirnames = []
    filenames = []

    f = []
    d = []
    
    for (dirpath, dirnames, filenames) in walk(root):
        for i in filenames:
            i_list = i.split(".")
            i_out = "".join(i_list[:-1])
            if i_out == "":
                i_out = i
            if i_out[-3:] == ending and i_out[:-4] in ["".join(x.split(".")[:-1]) for x in filenames]:
                #If it has the dup ending and the base part of the name exists also without the (1). #Making sure its actually a dupe.
                f.append(root + "\\" + i)
        if len(dirnames) == 0:
            #print "ay"
            pass
        else:
            for j in dirnames:
                #print len(dirnames)
                if j[-3:] == ending and j[:-4] in dirnames:
                    d.append(root + "\\" + j)
                else:
                    new_root = root + "\\" + j
                    #print new_root
                    level_delete(new_root, ending) #This little thing makes it recursive and it will check all lower folders.

        
        """
        # This here is just checking that the (1) file/folder is actually a duplicate.

        # This little block makes a list of all the files without extensions.
        file_temp = []
        for i in filenames:
            i_list = i.split(".")
            i_out = "".join(i_list[:-1])
            if i_out == "":
                i_out = i
            file_temp.append(dirpath + i_out)
        print file_temp
        for i in f:
            i_list = i.split(".")
            i_out = "".join(i_list[:-1])
            if i_out == "":
                i_out = i
            if i[:-4] in file_temp:
                pass
            else:
                f.remove(i)   
        
        for j in d:
            print j[:-4]
            if j[:-4] in dirnames:
                pass
            else:
                d.remove(j)
        """
    if f:
        file_del.append(f)
    if d:
        dir_del.append(d)


level_delete(start, ending)
    
file_del = list(itertools.chain.from_iterable(file_del))
dir_del = list(itertools.chain.from_iterable(dir_del))
# ^^This puts it into 1 list, no lists within lists^^

#print "file_del: " + str(file_del)
#print "dir_del: " + str(dir_del)

print "DIR_DEL"
for i in dir_del:
    print i
print "FILE_DEL"
for j in file_del:
    print j

conf = raw_input("Are you happy to delete these? ")
if conf.lower() == "y" or "yes":
    for i in dir_del:
        try:
            rmtree(i)
            print "Dir: Success"
        except:
            print "Dir: Something went wrong."
    for j in file_del:
        try:
            print "File: Success"
            remove(j)
        except:
            print "File: Something went wrong."
else:
    print "All g"

