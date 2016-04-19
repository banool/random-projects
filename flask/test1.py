#!/usr/bin/python

# Just a compatibility layer to make python2 more like python3
from __future__ import print_function
def input(question):
    return str(raw_input(question))
# This line, for example, works:
# print(input("bemes? "), end="")


from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return(input("endme "))
    return "Hello World!!!"

if __name__ == "__main__":
    app.debug = True
    app.run()
