#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import blob


def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error message ausgegeben
    if (not "idTkn" in arguments) or (not "postId" in arguments) or (not "vote" in arguments):
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
    # Wird geschaut ob der Post up oder downgevotet werden sollte
    if arguments["vote"].value == "up":
        # Der Blob wird upgevotet
        blobToUpvote.vote(user.path, True)
        print("done")
        return
    elif arguments["vote"].value == "down":
        # Der Blob wird downgevoted
        blobToUpvote.vote(user.path, False)
        print("done")
        return  
    else:
        print("error - argument vote ist nicht gültig")

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()
