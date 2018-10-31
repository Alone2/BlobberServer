# Anmelde Library
import json
import os
import time
# install: pip install --upgrade google-api-python-client
#          pip install requests
from google.oauth2 import id_token
from google.auth.transport import requests

# Oeffnung der Json Files
class jsonClass:
    @classmethod
    def open(cls, path):
        jsonFile = open(path, 'r')
        data = json.loads(jsonFile.read())
        jsonFile.close()
        return data
    @classmethod
    def save(cls, path, data):
        dataJSON = json.dumps(data, indent=2)
        jsonFile = open(path, 'w')
        jsonFile.write(dataJSON)
        jsonFile.close()

# Klasse des Nutzers
class blobUser:
    def __init__(self, token):
        # Testen ob der Account echt ist. Wenn ja -> isOk = True
        if not self.__tokenReal(token):
            self.isOk = False
            return
        self.isOk = True
                
        # Werte vom json-file werden an blobUser übertragen
        userFile = jsonClass.open(self.path)
        self.firstName = userFile["info"]["firstName"]
        self.lastName = userFile["info"]["lastName"]
        self.mail = userFile["info"]["mail"]

    def __tokenReal(self, token):
        # Wird bei Google getestet ob der Acc. echt ist
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.homeData["clientId"])
            self.userId = idinfo['sub']
            
            # Path wird definiert
            self.path = self.homeFolder + "/user/" + self.userId + ".json"
        
        except ValueError:
            return False
        #Debug:
        #except ValueError as e: print(e)
            

        # Wenn der User noch nicht im System ist, wird ihm ein File erstellt
        # -> Wenn der User sich manuell anmelden sollte -> Später durch Instanz ersetzen
        if not os.path.isfile(self.path):
            jsonData = {}
            storedInfo = {"mail":idinfo["email"],"firstName":idinfo["given_name"],"lastName":idinfo["family_name"]}
            jsonData['info'] = storedInfo
            jsonData['text'] = []
            jsonClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 

        #Text wird geschpeichert
        userFile = jsonClass.open(self.path)
        userFile["text"].append({"time":zeitVar,"text":text})
        jsonClass.save(self.path, userFile)

    @classmethod
    def setHomeFolder(cls):
        #Der Ort der Dateien wird von files.json ausgelesen
        path = 'files.json'
        data = jsonClass.open(path)
        # Und als homeData gespeichert
        cls.homeData = data
        cls.homeFolder = data["HomeFolder"]
