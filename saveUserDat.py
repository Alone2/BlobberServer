#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
from MBlib import blobUser

def main():
    arguments = cgi.FieldStorage()
    # Wenn die Argumente nicht da sind, wird eine Error-Message ausgegeben
    if (not "idTkn" in arguments) or (not "data" in arguments) or (not "dataValue" in arguments):
        print("error - arguments missing")
        return
    # Nutzer wird erstellt
    user = blobUser(arguments["idTkn"].value)
    # Es wird geschaut ob der User "echt" ist
    if user.isOk == False:
        print("error - nicht angemeldet")
        return

    newValue = arguments["dataValue"].value
    #Name wird neu gespeichert
    if arguments["data"].value == "name":
        user.username = newValue
    #wird gespiechert
    user.save()
    print("done")
    return

if __name__ == "__main__":
    # Beim Starten wird die Funktion main ausgeführt
    main()