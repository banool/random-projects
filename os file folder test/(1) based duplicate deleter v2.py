from os import walk
from os import remove
from shutil import rmtree
import itertools

start = "C:\Users\daniel\Google Drive\School TGS"
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
            if i_out[-3:] == ending:
                f.append(root + "\\" + i)
        if len(dirnames) == 0:
            #print "ay"
            pass
        else:
            for j in dirnames:
                #print len(dirnames)
                if j[-3:] == ending:
                    d.append(root + "\\" + j)
                else:
                    new_root = root + "\\" + j
                    #print new_root
                    level_delete(new_root, ending)

    if f:
        file_del.append(f)
    if d:
        dir_del.append(d)

def main():
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

main()
