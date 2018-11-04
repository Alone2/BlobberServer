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
    # Die blobs werden gesucht und schliesslich ausgegeben
    blobs = sortingClass.getBlobJsonList(arguments["sorting"].value, int(arguments["von"].value), int(arguments["bis"].value))
    print(blobs)

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()

