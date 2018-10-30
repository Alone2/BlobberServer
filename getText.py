#!/usr/bin/env python
print("Content-type: text/html\n\n")
import cgi

arguments = cgi.FieldStorage()

if arguments["sorting"] == "new":
    pass
elif arguments["sorting"] == "trending":
    pass
