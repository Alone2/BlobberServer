# Anmelde Library
import json
import os
import time
# install: pip install --upgrade google-api-python-client
#          pip install requests
from google.oauth2 import id_token
from google.auth.transport import requests

# Oeffnung der Json Files
class dataClass:
    @staticmethod
    def open(path):
        jsonFile = open(path, 'r')
        data = json.loads(jsonFile.read())
        jsonFile.close()
        return data

    @staticmethod
    def save(path, data):
        dataJSON = json.dumps(data, indent=2)
        jsonFile = open(path, 'w')
        jsonFile.write(dataJSON)
        jsonFile.close()

    @classmethod
    def getHomeData(cls):
        #Der Ort der Dateien wird von files.json ausgelesen und ausgegeben
        path = 'files.json'
        data = cls.open(path)
        return data

# Klasse des Nutzers
class blobUser:
    def __init__(self, token):
        #Home angeben
        self.homeData = dataClass.getHomeData()
        self.homeFolder = dataClass.getHomeData()["HomeFolder"]
        # Testen ob der Account echt ist. Wenn ja -> isOk = True
        if not self.__tokenReal(token):
            self.isOk = False
            return
        self.isOk = True
        
        # Werte vom json-file werden an blobUser übertragen
        userFile = dataClass.open(self.path)
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
            dataClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 

        # Text wird geschpeichert
        userFile = dataClass.open(self.path)
        # upvotes, id, id von comment soll gesprichert werden (Id zufällig gewählt->Test ob
        # es sie schon gibt -> index)
        userFile["text"].append({"time":zeitVar,"text":text})
        dataClass.save(self.path, userFile)

# Klasse um Sortierung zu bekommen
class sorting:
    @classmethod
    def getBlobList(cls, sorting, von, bis):
        #20 Blobs werden "genommen"
        home = dataClass.getHomeData()["home"]
        path = home + "/sorting/" + sorting + ".json" #Bei New vielleicht anders. Bei New auch: clickedTime -> Zeit bei Aktuallisierung von New
        srt = dataClass.open(path)[von:bis]
        # Die Liste von Blobs wird kreiert
        blobList = []
        for i in srt:
            blobPost = blob(i)
            blobList.append(blobPost)
        # Liste wird ausgegeben
        return blobList

#Class für Blobbers(Posts)
class blob:
    def __init__(self, postId):
        #Index wird abgerufen
        home = dataClass.getHomeData()["home"]
        indexPath = home + "/index.json"
        index = dataClass.open(indexPath)
        #PostId wird gesucht
        blobPost = index[postId]
        #upvotes und so werden in Klasse gespeichert
        self.upvotes = blobPost["upvotes"]
        self.commentsNumber = blobPost["commentsNumber"]
    
    def upvote(self):
        pass
    def downvote(self):
        pass
    def comment(self):
        pass   
