"""
Abstraction yo.
We have the query in one pyfile and the html generation
in another, all of which is aggregated in this pyfile.
"""

chrome_location = """ "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" """
outputname = "output.html"

from os import system
from fetch2 import query
from htmlgenerate import htmlgen

term = str(raw_input("Enter query: "))

results = query(term)
output = htmlgen(results, term)

with open(outputname, "wb") as f:
    f.writelines(output)

# Finally, attempts to open the html file that was generated.
# Need to find a way to get the current directory and append it to the start of outputname
# system(chrome_location + outputname)
