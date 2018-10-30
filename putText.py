#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
import MBlib

arguments = cgi.FieldStorage()

userId = MBlib.getUserId(arguments["usrId"])


path = 'files.json'
data = MBlib.openJson(path)
HomeFolder = data["HomeFolder"]

path = HomeFolder + "/user/" + userId + ".json"
userFile = MBlib.openJson(path)
#New Post in userFile
MBlib.saveJson(path, userFile)

path = data["HomeFolder"] + "/index.json"
index = MBlib.openJson(path)

arguments = cgi.FieldStorage()