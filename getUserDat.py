#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser

def main():
    arguments = cgi.FieldStorage()  
    if (not "idTkn" in arguments) or (not "data" in arguments) :
        print("error - arguments missing")
        return  
    # Nutzer wird erstellt
    user = blobUser(arguments["idTkn"].value)
    # Es wird geschaut ob der User "echt" ist
    if user.isOk == False:
        print("error - nicht angemeldet")
        return

    # Nutzername wird abgefragt
    if arguments["data"].value == "name":
        data = json.dumps({"data":user.username})
        print(data)
    
    return

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()