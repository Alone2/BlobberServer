#In disem Programm wird der Content sortiert
import time
from MBlib import dataClass

def newTrending():
    # Wie newHot()
    pass
    
def newHot():
    #Liste mit Blobs wird geoffnet
    home = dataClass.getHomeData()["HomeFolder"]
    indexPath = home + "/index.json"
    index = dataClass.open(indexPath)

    hot = []
    # Für jeden Blob wird der Text im For-Loop ausgeführt
    for i in index:
        postPath = i["path"]
        userFile = dataClass.open(postPath)
        pstIfo = {}
        for postInfo in userFile["text"]:
            if postInfo["id"] == i["id"]:
                pstIfo = postInfo
                break
        # upvotes (downvotes abgezogen)
        upvotes = pstIfo["upvotes"]
        # commentsNumber ist die Anzahl Kommentare
        commentsNumber = pstIfo["commentsNumber"]
        # Wann der Blob veröffentlicht wurde als liste: Wie https://docs.python.org/3/library/time.html#time.struct_time
        datum = pstIfo["time"]
        # Wann der Blob veröffeltlicht wurde seit dem 1. Januar 1970
        unxDatum = pstIfo["unxTime"]
        # Hier kommt ein Algorithmus
        
        # Blobs die es in Hot eingeordnet werden sollen, werden in die Liste hot gespeichert
        hot.append(i["id"])

    # Hot wird als Datei gespeichert
    hotPath = home + "/sorting/hot.json"
    dataClass.save(hotPath, hot)
  

if __name__ == "__main__":
    while True:
        newTrending()
        newHot()
        time.sleep(3600)
