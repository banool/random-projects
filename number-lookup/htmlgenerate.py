"""
Opens up the template html file and fills in anything where there is
something like #this#. Returns the resulting html in a line by line list.
"""

templatename = "template.html"

"""
This function takes the results from the query function
as well as the initial term inputted.
"""

#need to check the length of the results to be greater than 0 before starting.
#also need to check if it is greater than one (So to repeat the results row).

output = []

def htmlgen(result, joined_term):
    print result[0][1][2]
    # This syntax automatically closes it the file after it is read into content
    with open(templatename, 'rb') as templatefile:
        content = templatefile.readlines()
    
    for line in content:
        if("<!-- queryterm -->" in line):
            line = line.replace("<!-- queryterm -->", joined_term)
            output.append(line)
        if("<!-- name -->" in line):
            line = line.replace("<!-- name -->", result[0][1][2])
            output.append(line)
        else:
            output.append(line)
            
    return output
    
    
