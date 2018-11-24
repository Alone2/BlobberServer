#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import sortingClass
from MBlib import blob
from MBlib import blobUser

def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error message ausgegeben
    if (not "sorting" in arguments) or (not "von" in arguments) or (not "bis" in arguments):
        print("error - arguments missing")
        return
    #wird geschaut ob es ein Kommentar ist
    if "comment" in arguments:
        if blob(arguments["comment"].value).isOk != True:
            print("error - invalid blob")
            return
        blobs = sortingClass.getCommentList("", int(arguments["von"].value), int(arguments["bis"].value), arguments["comment"].value)
        print(json.dumps(blobs))
        return
    # Die blobs werden gesucht und schliesslich ausgegeben
    sorting = sortingClass()
    if arguments["sorting"].value == "hot":
        sorting = sortingClass.HOT
    elif arguments["sorting"].value == "trending":
        sorting = sortingClass.TRENDING
    elif arguments["sorting"].value == "new":
        sorting = sortingClass.NEW
    elif arguments["sorting"].value == "user":
        sorting = sortingClass.USER
        if not "userId" in arguments:
            print("error - keine userId angegeben")
            return
        userId = arguments["userId"]
        blobs = sortingClass.getBlobDataList(sorting, int(arguments["von"].value), int(arguments["bis"].value), userId.value)
        print(json.dumps(blobs))
        return
    else:
        print("error - kein korrektes Sorting eingegeben")
        return
    #Wenn der Nutzer eingeloggt ist, wird auch zerückgegeben, ob er schon upgevotet hat
    if "idTkn" in arguments:
            # BloberUser wird erstellt
            idTkn = arguments["idTkn"].value
            blobUsr = blobUser(idTkn)
            if blobUsr.isOk != True:
                print("error - anmeldung schiefgelaufen")
                return
            blobs = sortingClass.getBlobDataList(sorting, int(arguments["von"].value), int(arguments["bis"].value), "", blobUsr.getVotetPosts())
            print(json.dumps(blobs))
    blobs = sortingClass.getBlobDataList(sorting, int(arguments["von"].value), int(arguments["bis"].value))
    print(json.dumps(blobs))

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()

