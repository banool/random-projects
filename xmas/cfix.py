"""
Daniel Porteous 696965
12/09/14

This program is meant to clean up C code in the ansi style of formatting.
"""

slash = '/'
asterik = "*"

fname = raw_input("\nLike this: ./example.c\nEnter a filename: ");
if(fname):
    pass
else:
    fname = "./example.c"

with open(fname) as f:
    content = f.readlines()

f.close()


# Primary operation. Changing    // something  ->  /* something */
print "\n"
for i in range(len(content)):
    if slash in content[i]:
        cont_len = len(content[i])
        for j in range(cont_len - 1):
            if(content[i][j] == slash and content[i][j+1] == slash):
                print "Line %d reads:\n%s" % (i, content[i])
                new_str = ""
                for k in range(cont_len):
                    if k == j+1:
                        new_str = new_str + asterik
                    else:
                        new_str = new_str + content[i][k]
                new_str = new_str.rstrip('\n') + ' */\n'
                
                content[i] = new_str
                print "Line %d now reads:\n%s" % (i, content[i])

# Writing the new file contents back to the file.
f = open(fname, "w")
for line in content:
    f.write("%s" % line)

f.close()
print "All done!"