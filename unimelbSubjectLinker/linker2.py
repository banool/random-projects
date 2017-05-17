from time import strftime

import re

# Updated for the new 2017 handbook.

targetFile = "winter subjects.txt"
outputFile = "subjects.html"

additionalMessage = "These subjects either don't require prereqs, or are those which I have the prereqs for"

rootUrl = "https://handbook.unimelb.edu.au/subjects/"

with open(targetFile, "r") as f:
    contents = f.readlines()

output = []
output.append("<html>")
output.append("<head>")
output.append("<title>%s</title>" % targetFile.split(".")[0])
output.append("</head>")
output.append("<body>")
output.append("<h1>%s</h1>" % targetFile.split(".")[0])
output.append(additionalMessage)
output.append("<ul>")

for item in contents:
    if item[0] != "#":
        m = re.match(r'.+(\(.+?\))', item)
        if not m:
            raise ValueError('Blah, something went wrong with the regex!')
        subjectCode = m.group(1)[1:-1]
        output.append("<li><a href='" + rootUrl + subjectCode + "'>" + item + "</a></li>")

output.append("</ul></br>")
output.append("<p>Made on: %s" % strftime("%d/%m/%Y"))
output.append("</body>")
output.append("</html>")

with open(outputFile, "w") as f:
    for line in output:
        f.write(line + "\n")
