# Anmelde Library
import json
import os
import time
import random
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
        self.userFile = dataClass.open(self.path)
        self.firstName = self.userFile["info"]["firstName"]
        self.lastName = self.userFile["info"]["lastName"]
        self.mail = self.userFile["info"]["mail"]

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
            jsonData['text'] = {}
            dataClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 
        unxTime = time.time()

        # Text wird geschpeichert
        userFile = dataClass.open(self.path)
        # Idee: upvotes und comments(ids) werden auch in Index gespeichert
        # random Id wird generiert
        indexPath = self.homeFolder + "/index.json"
        blobId = self.__getUniqueBlobId(indexPath, 10)
        # Id wird mit Path in Index gespeichert
        index = dataClass.open(indexPath)
        """index.append({"id":blobId, "path":self.path})"""
        index[blobId] = {"path": self.path}
        dataClass.save(indexPath, index)
        # Blob wird gespeichert
        """userFile["text"].append({"id":blobId, "time":zeitVar,"unxTime":unxTime, "text":text})"""
        userFile["text"][blobId] = {"time":zeitVar,"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
        dataClass.save(self.path, userFile)

    def __getUniqueBlobId(self, indexPath, lenght):
        blobId = ""
        for i in range(lenght):
            blobId += random.choice("qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM1234567890")
        index = dataClass.open(indexPath)
        if blobId in index:
            blobId = self.__getUniqueBlobId(indexPath, lenght)
        return blobId

# Klasse um Sortierung zu bekommen
class sortingClass:
    @classmethod
    def getBlobJsonList(cls, sorting, von, bis):
        #20 Blobs werden "genommen"
        home = dataClass.getHomeData()["HomeFolder"]
        path = home + "/sorting/" + sorting + ".json" #Bei New vielleicht anders. Bei New auch: clickedTime -> Zeit bei Aktuallisierung von New
        srt = dataClass.open(path)[von:bis]
        # Die Liste von Blobs wird kreiert
        blobList = []
        for i in srt:
            blobPost = blob(i)
            blobList.append(blobPost.data)
        # Liste wird ausgegeben
        return blobList

#Class für Blobbers(Posts)
class blob:
    def __init__(self, postId):
        self.postId = postId
        # Index wird abgerufen
        home = dataClass.getHomeData()["HomeFolder"]
        self.indexPath = home + "/index.json"
        index = dataClass.open(self.indexPath)
        # Pfad wird abgerufen
        path = index[postId]["path"]
        # PostId wird gesucht
        blobPost = dataClass.open(path)["text"][postId]
        # upvotes und so werden in Klasse gespeichert
        self.data = blobPost
        self.upvotes = blobPost["upvotes"]
        self.commentsNumber = blobPost["commentsNumber"]
        self.text = blobPost["text"]
    
    def upvote(self, blobUser):
        pass
    def downvote(self):
        pass
    def comment(self):
        pass   
