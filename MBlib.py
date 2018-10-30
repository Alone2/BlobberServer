# Anmelde Library
import json
#install: pip install --upgrade google-api-python-client
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
        if not self.__tokenReal(token):
            self.isOk = False
            return
        self.isOk = False
        path = self.homeFolder + "/user/" + self.userId + ".json"
        userFile = jsonClass.open(path)
        self.name = userFile["info"]["name"]

    def __tokenReal(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.homeFiles["clientId"])
            self.userId = idinfo['sub']
            self.mail = idinfo['email']
        except:
            return False
        return True

    def write(self, text):
        pass

    @classmethod
    def setHomeFolder(cls):
        path = 'files.json'
        data = jsonClass.open(path)
        cls.homeFiles = data
        cls.homeFolder = data["HomeFolder"]
