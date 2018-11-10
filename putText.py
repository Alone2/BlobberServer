#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import dataClass

def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error-Message ausgegeben
    if (not "idTkn" in arguments) or (not "text" in arguments) or (not "comment" in arguments):
        print("error - arguments missing")
        return
    # Wenn der Blob mehr als 300 Zeichen hat, wird eine Error-Message ausgegeben
    if len(arguments["text"].value) >= 300:
        print("error - blob too long(more than 300 characters)")
        return
    # BlobUser wird aus idTkn generiert
    user = blobUser(arguments["idTkn"].value)
    text = arguments["text"].value
    # Es wird geschaut ob der User "echt" ist
    if user.isOk == False:
        print("error - nicht angemeldet")
        return
    # Wird geschaut ob es en Kommentar ist
    if arguments["comment"].value == "true":
        if not "postId" in arguments:
            print("error - arguments missing")
            return
        user.comment(text, arguments["postId"].value)
        return
    else:
        # Blob wird gespeichert
        user.write(text)
        print("done")

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()
