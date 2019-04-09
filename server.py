#In disem Programm wird der Content sortier
#pip install schedule
import time
import schedule
from MBlib import dataClass

def newTrending():
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" Trending wird neu generiert")
    # Wie newHot()
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" Trending wurde generiert")
    pass

def newNew():
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" New wird neu generiert")
    # Idee New ist Rückwärts: neuste Posts als letztes -> einfacher um abzurufen -> Um Mitternacht wird das ganze resettet
    # Zeit wird ausgegeben

    #Liste mit Blobs wird geoffnet
    home = dataClass.open("files.json")["HomeFolder"]
    indexPath = home + "/index.json"
    index = dataClass.open(indexPath)
    #New wird geöffnet
    newPath = home + "/sorting/new.json"
    new = dataClass.open(newPath)
    # Für jeden Blob wird der Text im For-Loop ausgeführt
    for postId in index:
        if not postId in new:
            new.append(postId)
    # Wird gespeichert
    dataClass.save(newPath, new)
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" New wurde generiert")
    
def newHot():
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" Hot wird neu generiert")
    #Liste mit Blobs wird geoffnet
    home = dataClass.open("files.json")["HomeFolder"]
    indexPath = home + "/index.json"
    index = dataClass.open(indexPath)

    hot = []
    # Für jeden Blob wird der Text im For-Loop ausgeführt
    for postId, postData in index.items():
        userFile = dataClass.open(home + postData["path"])
        pstIfo = userFile["text"][postId]

        # upvotes (downvotes abgezogen)
        upvotes = pstIfo["upvotes"]
        # commentsNumber ist die Anzahl Kommentare
        commentsNumber = pstIfo["commentsNumber"]
        # Wann der Blob veröffeltlicht wurde seit dem 1. Januar 1970
        unxDatum = pstIfo["unxTime"]
        # Hier kommt ein Algorithmus
        
        # Blobs die es in Hot eingeordnet werden sollen, werden in die Liste hot gespeichert
        hot.append(postId)

    # Hot wird als Datei gespeichert
    hotPath = home + "/sorting/hot.json"
    dataClass.save(hotPath, hot)
    # Zeit wird ausgegeben
    print(time.strftime("[%H:%M:%S]", time.localtime())+" Hot wurde generiert")

if __name__ == "__main__":
    print("Blobber-Server V0.1.2 wird gestartet...")
    # Scheudle Tasks werden definiert
    schedule.every().hour.do(newTrending)
    schedule.every().hour.do(newHot)
    schedule.every(30).seconds.do(newNew)
    print("Blobber-Server wurde gestartet")
    while True:
        # Scheudle Tasks werden am Leben gehalten/ ausgeführt
        schedule.run_pending()
        time.sleep(1)
        
