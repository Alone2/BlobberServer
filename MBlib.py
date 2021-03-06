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
        """self.firstName = self.userFile["info"]["firstName"]
        self.lastName = self.userFile["info"]["lastName"]
        self.mail = self.userFile["info"]["mail"]"""
        self.username = self.userFile["info"]["username"]

    def __tokenReal(self, token):
        # Wird bei Google getestet ob der Acc. echt ist
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), BlobberHomeData["clientId"])
            self.userId = idinfo['sub']
            
            # Path wird definiert
            self.relativePath = "/user/" + self.userId + ".json"
            self.path = BlobberHomeFolder + self.relativePath
        
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
            index[userId] = {"path": self.relativePath}
            dataClass.save(userlistPath, index)
            # Daten des Nutzers werden gespeichert
            jsonData = {}
            #storedInfo = {"mail":idinfo["email"],"firstName":idinfo["given_name"],"lastName":idinfo["family_name"], "userId":userId,"username":"unnamed"}
            storedInfo = {"userId":userId,"username":"unnamed"}
            jsonData['info'] = storedInfo
            jsonData['text'] = {}
            jsonData['comments'] = {}
            jsonData['upvotedPosts'] = []
            jsonData['downvotedPosts'] = []
            dataClass.save(self.path, jsonData)

        return True

    def write(self, text):
        # Zeit angeben
        unxTime = time.time()
        # random Id wird generiert
        indexPath = BlobberHomeFolder + "/index.json"
        blobId = self.__getUniqueBlobId(indexPath, 10)
        # Id wird mit Path in Index gespeichert
        index = dataClass.open(indexPath)
        index[blobId] = {"path": self.relativePath, "comments":[]}
        dataClass.save(indexPath, index)
        # Blob wird gespeichert
        userData = {"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
        self.writeData(["text",blobId], userData)
        #dataClass.save(self.path, userData)

    def comment(self, postId, text):
        # Zeit angeben
        unxTime = time.time()
        # comment wird in commentIndex mit einer random Id gespeichert
        commentIndexPath = BlobberHomeFolder + "/commentIndex.json"
        commentId = self.__getUniqueBlobId(commentIndexPath, 10)
        commentIndex = dataClass.open(commentIndexPath)
        commentIndex[commentId] = {"path": self.relativePath}
        dataClass.save(commentIndexPath, commentIndex)
        # Id wird in Index gespeichert
        indexPath = BlobberHomeFolder + "/index.json"
        index = dataClass.open(indexPath)
        index[postId]["comments"].append(commentId)
        dataClass.save(indexPath, index)
        # Commentsnumber wird erhöht
        blobPost = dataClass.open(BlobberHomeFolder + index[postId]["path"])
        blobPost["text"][postId]["commentsNumber"] += 1
        dataClass.save(BlobberHomeFolder + index[postId]["path"], blobPost)
        # Blob wird gespeichert
        userData = {"unxTime":unxTime, "text":text, "upvotes":0, "commentsNumber":0}
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

    def save(self):
        # Daten werden geholt
        jsonFile = open(self.path, 'r+')
        myData = json.loads(jsonFile.read())
        #myData = dataClass.open(self.path)
        # Daten des Objekts werden aufgeschrieben
        """myData["info"]["firstName"] = self.firstName
        myData["info"]["lastName"] = self.lastName
        myData["info"]["mail"] = self.mail """
        myData["info"]["username"] = self.username
        #dataClass.save(self.path,myData)
        # Daten werden gespeichert
        dataJSON = json.dumps(myData, indent=2)
        # wird überschrieben
        jsonFile.seek(0)
        jsonFile.write(dataJSON)
        jsonFile.truncate()
        jsonFile.close()

    def getVotetPosts(self):
        # up und downgevotete Post werden so: {"up":[],"down":[]} ausgegeben
        userData = dataClass.open(self.path)
        voted = {}
        voted["up"] = userData["upvotedPosts"]
        voted["down"] = userData["downvotedPosts"]
        return voted
        
# Klasse um Sortierung zu bekommen
class sortingClass:
    HOT, TRENDING, NEW, USER = "/sorting/hot.json","/sorting/trending.json","/sorting/new.json", 87
    @classmethod
    def getBlobDataList(cls, sorting, von, bis, userId = "", votedPosts = {"up":[],"down":[]}):
        srt = []
        if sorting == cls.USER:
            # X Blobs werden "genommen"
            userPath = dataClass.open(BlobberHomeFolder + "/userlist.json")[userId]["path"]
            dat = dataClass.open(BlobberHomeFolder + userPath)["text"]  # ERROR! -> manche blobs sind unter "text" noch da, aber im Index gelöscht
            for x, y in dat.items():
                srt.append(str(x)) #Ist nicht normaler String, sondern {}
            # später ... nach time sortieren...
            srt = srt[von:bis]
        else:
            # X Blobs werden "genommen"
            path = BlobberHomeFolder + sorting
            srt = dataClass.open(path)[von:bis]
        return cls.createList(srt, blob, votedPosts)
    
    @classmethod
    def getListLenght(cls, sorting, userId = ""):
        srt = []
        if sorting == cls.USER:
            # X Blobs werden "genommen"
            userPath = dataClass.open(BlobberHomeFolder + "/userlist.json")[userId]["path"]
            dat = dataClass.open(BlobberHomeFolder + userPath)["text"]
            for x, y in dat.items():
                srt.append(str(x)) #Ist nicht normaler String, sondern {}
            return len(srt)
        else:
            # X Blobs werden "genommen"
            path = BlobberHomeFolder + sorting
            return len(dataClass.open(path))

    @classmethod
    def getCommentList(cls, sorting, von, bis, postId, votedPosts = {"up":[],"down":[]}):
        index = dataClass.open(BlobberHomeFolder + "/index.json")
        # CommentId's werden abgerufen
        comments = index[postId]["comments"]
        #Liste mit Kommentaren wird generiert
        return cls.createList(comments, comment, votedPosts)[von:bis]
        # Sorting noch nicht implementiert!

    # getCommentListLenght noch Ohne sorting!
    @classmethod
    def getCommentListLenght(cls, postId):
        index = dataClass.open(BlobberHomeFolder + "/index.json")
        # CommentId's werden abgerufen
        return len(index[postId]["comments"])
    
    @classmethod
    def createList(cls, le_list, commentOrBlob, votedPosts = {"up":[],"down":[]}):
        #Liste von Kommentaren / Blobs wird erstellt
        blobList = []
        for i in le_list:
            blobPost = commentOrBlob(i)
            # Wenn Blob nicht existiert: error
            if not blobPost.isOk:
                data = {}
                data["id"] = i
                data["text"] = "[error]"
                data["OP"] = "[removed]"
                data["OP_id"] = ""
                data["id"] = ""
                data["unxTime"] = time.time()
                blobList.append(data)
                continue
            data = blobPost.data
            data["id"] = i
            data["OP"] = blobPost.OP
            data["OP_id"] = blobPost.OP_id
            #wird geschaut ob der Nutzer den Blob schon upgevoted hat
            if i in votedPosts["up"]:
                data["isUpvoted"] = True
                data["isDownvoted"] = False
            elif i in votedPosts["down"]:
                data["isDownvoted"] = True
                data["isUpvoted"] = False
            else:
                data["isUpvoted"] = False
                data["isDownvoted"] = False
            #Post wird in List hinzgefügt
            blobList.append(data)
        return blobList

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
        except:
            self.isOk = False
        #Debug
        """except Exception as e:
            self.isOk = e"""

    def __getBlobPost(self, dataVar):
        # Index wird geöffnet
        index = dataClass.open(self.indexPath)
        # Pfad wird abgerufen
        self.path = BlobberHomeFolder + index[self.postId]["path"]
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