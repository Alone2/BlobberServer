#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import dataClass

def main():
    arguments = cgi.FieldStorage()
    if (not "idTkn" in arguments) or (not "text" in arguments):
        print("error - arguments missing")
        return
    
    user = blobUser(arguments["idTkn"].value)
    text = arguments["text"].value

    if user.isOk == False:
        print("error - Nicht angemeldet")
        return
    user.write(text)
    print("done")

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()
