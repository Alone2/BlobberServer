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

# Klasse des Nutzers
class blobUser:
    def __init__(self, token):
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
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), BlobberHomeData["clientId"])
            self.userId = idinfo['sub']
            
            # Path wird definiert
            self.path = BlobberHomeFolder + "/user/" + self.userId + ".json"
        
        except ValueError:
            return False
        #Debug:
        #except ValueError as e: print(e)
            

        # Wenn der User noch nicht im System ist, wird ihm ein File erstellt
        # -> Wenn der User sich manuell anmelden sollte -> Später durch Instanz ersetzen
        if not os.path.isfile(self.path):
            # Eine User-Id wird generiert
            userlistPath = BlobberHomeFolder + "/userlist.json"
            userId = self.__getUniqueBlobId(userlistPath, 10)
            # User-Id wird mit Path in Index gespeichert
            index = dataClass.open(userlistPath)
            index[userId] = {"path": self.path}
            dataClass.save(userlistPath, index)
            # Daten des Nutzers werden gespeichert
            jsonData = {}
            jsonData['userId'] = userId
            storedInfo = {"mail":idinfo["email"],"firstName":idinfo["given_name"],"lastName":idinfo["family_name"]}
            jsonData['info'] = storedInfo
            jsonData['text'] = {}
            jsonData['upvotetPosts'] = []
            dataClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 
        unxTime = time.time()

        # Idee: upvotes und comments(ids) werden auch in Index gespeichert
        # random Id wird generiert
        indexPath = BlobberHomeFolder + "/index.json"
        blobId = self.__getUniqueBlobId(indexPath, 10)
        # Id wird mit Path in Index gespeichert
        index = dataClass.open(indexPath)
        index[blobId] = {"path": self.path}
        dataClass.save(indexPath, index)
        # Blob wird gespeichert
        userData = {"time":zeitVar,"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
        self.writeData(["text",blobId], userData)
        #dataClass.save(self.path, userData)

    def writeData(self, ort, data):
        # Daten des gespricherten Posts werden abgerufen
        userData = dataClass.open(self.path)
        if len(ort) == 1:
            userData[ort[0]] = data
        elif len(ort) == 2:
            userData[ort[0]][ort[1]] = data
        elif len(ort) == 3:
            userData[ort[0]][ort[1]][ort[3]] = data
        else:
            # Error
            return
        # Die Daten werden gespeichert
        dataClass.save(self.path, userData)

    def __getUniqueBlobId(self, path, lenght):
        # Zufällige Id wird kreiert
        blobId = ""
        for i in range(lenght):
            blobId += random.choice("qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM1234567890")
        # Wenn die Id schon vergeben ist, wird eine neue kreiert
        index = dataClass.open(path)
        if blobId in index:
            blobId = self.__getUniqueBlobId(path, lenght)
        # Id wird ausgegeben
        return blobId

# Klasse um Sortierung zu bekommen
class sortingClass:
    HOT, TRENDING = "/sorting/hot.json","/sorting/trending.json"
    @classmethod
    def getBlobDataList(cls, sorting, von, bis):
        # X Blobs werden "genommen"
        path = BlobberHomeFolder + sorting #Bei New vielleicht anders. Bei New auch: clickedTime -> Zeit bei Aktuallisierung von New
        srt = dataClass.open(path)[von:bis]
        # Die Liste von Blobs wird kreiert
        blobList = []
        for i in srt:
            blobPost = blob(i)
            data = blobPost.data
            data["id"] = i
            blobList.append(data)
        # Liste wird ausgegeben
        return blobList

# Class für Blobbers(Posts)
class blob:
    def __init__(self, postId):
        self.postId = postId
        # Index wird abgerufen
        self.indexPath = BlobberHomeFolder + "/index.json"
        index = dataClass.open(self.indexPath)
        # wird geschaut ob der Blob überhaubt existiert -> wenn nicht -> isOk = False
        try:
            # Pfad wird abgerufen
            self.path = index[postId]["path"]
            # PostId wird gesucht
            blobPost = dataClass.open(self.path)["text"][postId]
            # upvotes und so werden in Klasse gespeichert
            self.data = blobPost
            self.upvotes = blobPost["upvotes"]
            self.commentsNumber = blobPost["commentsNumber"]
            self.text = blobPost["text"]
            self.isOk = True
        except:
            self.isOk = False
    
    def upvote(self, blobUserPath):
        # Daten des upvotenden Users werden abgerufen
        userData = dataClass.open(blobUserPath)
        # Wenn Post schon upgevoted
        if self.postId in userData["upvotetPosts"]:
            userData["upvotetPosts"].remove(self.postId)
            dataClass.save(blobUserPath, userData)
            # Blob Upvote number wird um eins zurückgesetzt
            blobPost = dataClass.open(self.path)
            blobPost["text"][self.postId]["upvotes"] -= 1
            dataClass.save(self.path, blobPost)
            return
        # BlobId wird zu upgevoteden Posts hinzugefügt
        userData["upvotetPosts"].append(self.postId)
        dataClass.save(blobUserPath, userData)
        # Blob Upvote number wird erhöht
        blobPost = dataClass.open(self.path)
        blobPost["text"][self.postId]["upvotes"] += 1
        dataClass.save(self.path, blobPost)
    def downvote(self):
        pass
    def comment(self):
        pass   

# Das Home Dateienverzeichnis wird definiert
BlobberHomeData = dataClass.open("files.json")
BlobberHomeFolder = BlobberHomeData["HomeFolder"]