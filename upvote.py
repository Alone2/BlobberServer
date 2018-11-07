#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import blob


def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error message ausgegeben
    if (not "idTkn" in arguments) or (not "postId" in arguments):
        print("error - arguments missing")
        return
    # BlobUser wird aus idTkn generiert
    user = blobUser(arguments["idTkn"].value)
    # Es wird geschaut ob der User "echt" ist
    if user.isOk == False:
        print("error - nicht angemeldet")
        return
    # Der Post wird abgefragt
    blobToUpvote = blob(arguments["postId"].value)
    # Wenn der Blob nicht existiert, wird eine Error-Message ausgegeben
    if blobToUpvote.isOk == False:
        print("error - ungültige blob-id")
        return
    # Der Blob wird upgevotet
    blobToUpvote.upvote(user.path)
    print("done")

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()
