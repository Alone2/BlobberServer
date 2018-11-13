#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import sortingClass

def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error message ausgegeben
    if (not "sorting" in arguments) or (not "von" in arguments) or (not "bis" in arguments):
        print("error - arguments missing")
        return
    #wird geschaut ob es ein Kommentar ist
    if "comment" in arguments:
        blobs = sortingClass.getCommentList("", int(arguments["von"].value), int(arguments["bis"].value), arguments["comment"].value)
        print(blobs)
        return
    # Die blobs werden gesucht und schliesslich ausgegeben
    sorting = sortingClass()
    if arguments["sorting"].value == "hot":
        sorting = sortingClass.HOT
    elif arguments["sorting"].value == "trending":
        sorting = sortingClass.TRENDING
    elif arguments["sorting"].value == "new":
        sorting = sortingClass.NEW
    else:
        print("error - kein korrektes Sorting eingegeben")
    blobs = sortingClass.getBlobDataList(sorting, int(arguments["von"].value), int(arguments["bis"].value))
    print(blobs)

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()

