#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import dataClass

arguments = cgi.FieldStorage()

user = blobUser(arguments["idTkn"].value)
text = arguments["text"].value

if user.isOk == True:
    user.write(text)
    print("done")
else:
    print("Error- Nicht angemeldet")



"""path = 'files.json'
data = dataClass.open(path)
HomeFolder = data["HomeFolder"]

path = HomeFolder + "/user/" + userId + ".json"
userFile = dataClass.open(path)
#New Post in userFile
dataClass.save(path, userFile)

path = data["HomeFolder"] + "/index.json"
index = dataClass.open(path)"""
