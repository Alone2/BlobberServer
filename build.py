from MBlib import dataClass

# Der Orndnerpfad und die Google Client Id werden abgefrage
homeFolder = input("Wo sollten die Daten gespeichert werden?: ")
googleClient = input("Google Client Id: ")

# Das Ganze wird in files.json gespeichert
fileData = {"HomeFolder":homeFolder, "clientId":googleClient}
dataClass.save("files.json", fileData)

# index.json wird erstellt
emptyDict = {}
dataClass.save(homeFolder + "/index.json", emptyDict)

# hot und Trending werden erstellt
emptyList = []
dataClass.save(homeFolder + "/sorting/hot.json", emptyList)
dataClass.save(homeFolder + "/sorting/trending.json", emptyList)