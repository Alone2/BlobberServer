#Anmelde Library
import json

def TokenReal(token):
    #test if Token real
    return True

def getUserId(token):
    if TokenReal(token) == True:
        pass
        #Get User ID
    return "error"

def openJson(path):
    jsonFile = open(path,'r')
    data = json.loads(jsonFile.read())
    jsonFile.close()
    return data

def saveJson(path, data):
    dataJSON = json.dumps(data, indent=2)
    jsonFile = open(path, 'w')
    jsonFile.write(dataJSON)
    jsonFile.close()

