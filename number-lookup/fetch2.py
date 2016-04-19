import csv
from operator import itemgetter

csvname = "daniel_location_numbers.csv"
classname = "classes.txt"

"""
Format of the classes dictionary:
class and a list full of tags. classes = {"level5": ["cardio", "heart", "etc."], etc}
"""

"""
Make an object called person or something.
"""

classes = {}

with open(classname, 'rb') as classfile:
    content = classfile.readlines()

for line in content:
    line = ''.join(line.split()) # Removing all spaces
    marker = 0
    try:
        while(line[marker] != ':'):
            marker += 1
    except IndexError:
        print "Index Error.\nThere is probably no colon on one of the lines in the classes.txt file.\nThe class based lookup will not work."
    classkey = line[0: marker]
    tags = line[marker+1:].split(',')
    if(len(tags) and tags[0]):
        classes[classkey] = tags


# Has the 'exact' option to check for string in string or string = string.
def comp(list1, list2, exact):
    strength = 0
    if(exact == True):
        for val1 in list1:
            for val2 in list2:
                if val1.lower() == val2.lower():
                    strength += 1
    else:
        for val in list1:
            if val.lower() in list2:
                strength += 1
    return strength


def query(inp):
    inp = inp.lower().split()
    results = {}
    
    # Opening the file
    csvfile = open(csvname, 'rb')
    csvobj = csv.DictReader(csvfile)
    
    # Doing the first round of checks.
    # This looks for the query in either the location or the name. 
    for row in csvobj:
        if(row["Number"]):
            strength_loca = comp(inp, row["Location"].lower(), False)
            strength_name = comp(inp, row["Name"].lower(), False)
            if(strength_loca > strength_name):
                results[row["Number"]] = [strength_loca, row["Location"], row["Name"]]
            elif(strength_loca < strength_name):
                results[row["Number"]] = [strength_loca, row["Location"], row["Name"]]
            # Making sure that if they're equal, it's not because they'e both 0
            elif(strength_loca > 0):
                results[row["Number"]] = [strength_loca, row["Location"], row["Name"]]

    empty = True
    if(len(results) > 0):
        empty = False
        # Sorting by keys: sorted(d.items(), reverse=True)
        results_test = sorted(results.items(), key=itemgetter(1), reverse=True)
        # If there are results with strength of 2 or higher, don't check tags.
        if(results_test[0][1][0] > 1):
            print results_test[0][1]
            print "High strength, returning..."
            return results_test
    
    """
    Searches through the tags for each class. If there is a match in the
    tags, append the class and its strength to the results, like before.

    Altered so that it also checks tag at the start here, but it starts with
    one less. This way the tags are prioritised last.
    """    
    results = sorted(results.items(), reverse=True)
    
    for i in range(0, len(classes)):
        strength = comp(inp, classes[classes.keys()[i]], True)
        if(empty == False):
            strength -= 1
        if(strength > 0):
            results.append(classes.keys()[i])
    
    csvfile.close()
    return results

"""
From here you can process this data.
You can tell when you get to the data retrieved from the tags because it
is only a single string, whereas the first sets of data returned from the
names/locations is a tuple.
"""

"""
Maybe make it so that the strength is the key, then have all their info
in a list in the value. <-- Done.

Didn't work because you can only have one key, changed to using the phone
number/extension as the key.
"""

