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
        self.username = self.userFile["info"]["username"]

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
            storedInfo = {"mail":idinfo["email"],"firstName":idinfo["given_name"],"lastName":idinfo["family_name"], "userId":userId,"username":"unnamed"}
            jsonData['info'] = storedInfo
            jsonData['text'] = {}
            jsonData['comments'] = {}
            jsonData['upvotedPosts'] = []
            jsonData['downvotedPosts'] = []
            dataClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 
        unxTime = time.time()
        # random Id wird generiert
        indexPath = BlobberHomeFolder + "/index.json"
        blobId = self.__getUniqueBlobId(indexPath, 10)
        # Id wird mit Path in Index gespeichert
        index = dataClass.open(indexPath)
        index[blobId] = {"path": self.path, "comments":[]}
        dataClass.save(indexPath, index)
        # Blob wird gespeichert
        userData = {"time":zeitVar,"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
        self.writeData(["text",blobId], userData)
        #dataClass.save(self.path, userData)

    def comment(self, postId, text):
        # Zeit angeben
        zeit = time.localtime()
        zeitVar = list(zeit[0:7]) 
        unxTime = time.time()
        # comment wird in commentIndex mit einer random Id gespeichert
        commentIndexPath = BlobberHomeFolder + "/commentIndex.json"
        commentId = self.__getUniqueBlobId(commentIndexPath, 10)
        commentIndex = dataClass.open(commentIndexPath)
        commentIndex[commentId] = {"path": self.path}
        dataClass.save(commentIndexPath, commentIndex)
        # Id wird in Index gespeichert
        indexPath = BlobberHomeFolder + "/index.json"
        index = dataClass.open(indexPath)
        index[postId]["comments"].append(commentId)
        dataClass.save(indexPath, index)
        # Commentsnumber wird erhöht
        blobPost = dataClass.open(index[postId]["path"])
        blobPost["text"][postId]["commentsNumber"] += 1
        dataClass.save(index[postId]["path"], blobPost)
        # Blob wird gespeichert
        userData = {"time":zeitVar,"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
        self.writeData(["comments",commentId], userData)

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
    HOT, TRENDING, NEW = "/sorting/hot.json","/sorting/trending.json","/sorting/new.json"
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
            data["OP"] = blobPost.OP
            data["OP_id"] = blobPost.OP_id
            blobList.append(data)
        # Liste wird ausgegeben
        return blobList
    
    @classmethod
    def getCommentList(cls, sorting, von, bis, postId):
        index = dataClass.open(BlobberHomeFolder + "/index.json")
        # CommentId's werdenn abgerufen
        comments = index[postId]["comments"]
        #Liste mit Kommentaren wird generiert
        commentsList = []
        for com in comments:
            commentPost = comment(com)
            data = commentPost.data
            data["id"] = com
            data["OP"] = commentPost.OP
            data["OP_id"] = commentPost.OP_id
            commentsList.append(data)
        return commentsList
        # Sorting noch nicht implementiert!

# Class für Blobbers(Posts)
class blob:
    def __init__(self, postId, dataVar = "text", indexPath = "/index.json"):
        self.postId = postId
        # Index wird abgerufen
        self.indexPath = BlobberHomeFolder + indexPath
        # wird geschaut ob der Blob überhaubt existiert -> wenn nicht -> isOk = False
        try:
            blobPost, blobPostText = self.__getBlobPost(dataVar)
            # upvotes und so werden in Klasse gespeichert
            self.OP = blobPost["info"]["username"]
            self.OP_id = blobPost["info"]["userId"]
            self.data = blobPostText
            self.upvotes = blobPostText["upvotes"]
            self.commentsNumber = blobPostText["commentsNumber"]
            self.text = blobPostText["text"]
            self.isOk = True
        except Exception as e:
            self.isOk = e

    def __getBlobPost(self, dataVar):
        # Index wird geöffnet
        index = dataClass.open(self.indexPath)
        # Pfad wird abgerufen
        self.path = index[self.postId]["path"]
        # PostId wird ausgegeben
        blobPost =  dataClass.open(self.path)
        blobPostText = blobPost[dataVar][self.postId]
        return blobPost,blobPostText

    def vote(self, blobUserPath, upvote):
        # Wird geschaut ob upgevoted oder downgevoted werden muss
        post = ["upvotedPosts", "downvotedPosts"]
        addition = 1
        if upvote == False:
            post = post[::-1]
            addition = -1
        
        # Daten des upvotenden Users werden abgerufen
        userData = dataClass.open(blobUserPath)

        # Wenn Post schon upgevoted/downgevoted vor downvote/upvote
        if self.postId in userData[post[1]]:
            # Zahl wird zu +/-2, da upvote/downvote rückgängig gemacht werden muss
            addition *= 2
            userData[post[1]].remove(self.postId)
        
        # Wenn Post schon upgevoted/downgevoted
        if self.postId in userData[post[0]]:
            # BlobId wird zu upgevoteden Posts hinzugefügt
            userData[post[0]].remove(self.postId)
            dataClass.save(blobUserPath, userData)
            # Blob Upvote number wird um addition geändert
            blobPost = dataClass.open(self.path)
            blobPost["text"][self.postId]["upvotes"] -= addition
            dataClass.save(self.path, blobPost)
            return
        # BlobId wird zu upgevoteden Posts hinzugefügt
        userData[post[0]].append(self.postId)
        dataClass.save(blobUserPath, userData)
        # Blob Upvote number wird erhöht
        blobPost = dataClass.open(self.path)
        blobPost["text"][self.postId]["upvotes"] += addition
        dataClass.save(self.path, blobPost)
  

# Klasse für Kommentare
class comment(blob):
    def __init__(self, commentId):
        super().__init__(commentId, "comments", "/commentIndex.json")
    #Hier kommt dann noch vote und so

# Das Home Dateienverzeichnis wird definiert
BlobberHomeData = dataClass.open("files.json")
BlobberHomeFolder = BlobberHomeData["HomeFolder"]