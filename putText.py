#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import jsonClass

arguments = cgi.FieldStorage()

blobUser.setHomeFolder()

user = blobUser(arguments["idTkn"].value)
text = arguments["text"].value

if user.isOk == True:
    user.write(text)
    print("done")
else:
    print("Error- Nicht angemeldet")



"""path = 'files.json'
data = jsonClass.open(path)
HomeFolder = data["HomeFolder"]

path = HomeFolder + "/user/" + userId + ".json"
userFile = jsonClass.open(path)
#New Post in userFile
jsonClass.save(path, userFile)

path = data["HomeFolder"] + "/index.json"
index = jsonClass.open(path)"""
