#In disem Programm wird der Content sortiert
import time
from MBlib import dataClass

def newTrending():
    # Wie newHot()
    pass
    
def newHot():
    #Liste mit Blobs wird geoffnet
    home = dataClass.getHomeData()["home"]
    indexPath = home + "/index.json"
    index = dataClass.open(indexPath)

    hot = []
    # Für jeden Blob wird der Text im For-Loop ausgeführt
    for i in index:
        # upvotes (downvotes abgezogen)
        upvotes = i["upvotes"]
        # commentsNumber ist die Anzahl Kommentare
        commentsNumber = i["commentsNumber"]
        # Wann der Blob veröffentlicht wurde
        datum = i["date"]
        
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
