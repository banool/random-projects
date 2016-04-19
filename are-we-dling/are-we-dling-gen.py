#!/usr/bin/python3

import fileinput
import time
from os.path import isfile

output_html_path = "/var/www/html/splash-level/are-we-dling.html"

switch_name = "./switch"

# If it reads 1 in the switch file, it will say that we're not
# downloading, even if we are.
switch = 0
if isfile(switch_name):
    with open(switch_name, "r") as f:
        if f.read()[0] == "1":
            switch = 1

# Reads from stdin if no file given.
total = 0.0
for line in fileinput.input():
    try:
        total += float(line[31:35])
    except:
        total = 0.0
        pass

template1 = ["<html>",
            "<head>",
            "<title>Downloading?</title>",
            "</head>",
            "<body>",
            "<h2 style='font-family:Helvetica'>'are we dling?' - rogey 2k15'</h2>"]

if total == 0 or switch == 1:
    template1.append("<h3 style='font-family:Helvetica'>no rogey, we aren't.</h3>")
else:
    template1.append("<h3 style='font-family:Helvetica'>Yes we are, at %skb/s</h3>" % total)

current_time = "Last checked at %s" % time.strftime("%I:%M:%p")

template2 = ["<p></p>",
             current_time,
             "</body>",
             "</html>"]

for line in template2:
    template1.append(line)

with open(output_html_path, "w") as f:
    f.writelines(template1)
