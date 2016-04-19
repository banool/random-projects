from time import strftime

targetFile = "2nd year subjects.txt"
outputFile = "subject.html"

additionalMessage = "These subjects either don't require prereqs, or are those which I have the prereqs for"

rootUrl = "https://handbook.unimelb.edu.au/view/2016/"

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
        output.append("<li><a href='" + rootUrl + item.split()[0] + "'>" + item + "</a></li>")

output.append("</ul></br>")
output.append("<p>Made on: %s" % strftime("%d/%m/%Y"))
output.append("</body>")
output.append("</html>")

with open(outputFile, "w") as f:
    for line in output:
        f.write(line + "\n")
