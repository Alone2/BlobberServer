#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi
import json
from MBlib import sortingClass

arguments = cgi.FieldStorage()

blobs = sortingClass.getBlobJsonList(arguments["sorting"].value, int(arguments["von"].value), int(arguments["bis"].value))
#print(json.dumps(blobs, indent=2))
print(blobs)