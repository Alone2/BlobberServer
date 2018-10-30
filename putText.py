#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import blobUser
from MBlib import jsonClass

arguments = cgi.FieldStorage()

blobUser.setHomeFolder()

user = blobUser(arguments["idTkn"])
text = arguments["text"]

if user.isOk == False:
    print("error")
    exit
user.write(text)


"""path = 'files.json'
data = jsonClass.open(path)
HomeFolder = data["HomeFolder"]

path = HomeFolder + "/user/" + userId + ".json"
userFile = jsonClass.open(path)
#New Post in userFile
jsonClass.save(path, userFile)

path = data["HomeFolder"] + "/index.json"
index = jsonClass.open(path)"""
