from ENTRY import ENTRY
class Memory:
    
    def __init__(self):
        #list to store all entries (and to rule them all)
        self.storage = []
        #IDnum to assign to next Entry
        self.nextEntryID = 0

    def isValidID(self, ID):
        for entry in self.storage:
            try:
                int(ID)
            except:
                print("That was not a valid ID")
                return
            if int(entry.getID()) == int(ID):
                return True
        return False

    def add(self, anEntry):
        self.storage.append(anEntry)

    def remove(self, entry):
        self.storage.remove(entry)

    def assignNewID(self):
        toAssign = self.nextEntryID
        self.nextEntryID +=1
        return toAssign
        
    def printSimple(self):
        nicknames = []
        for entry in self.storage:
            print('{}: {}'.format(entry.getID(), entry.getNickName()))
            
    def printDetail(self):
        for entry in self.storage:
            print()
            entry.printDetail()
            print()
            
    def printHits(hitList):
        print("Done searching")
        print("Hits:")
        for hit in hitList:
            hit.printDetail()
            print()

    def searchMatchOne(self, queries):
        hitList = []
        for entry in self.storage:
            added = False
            for query in queries:
                if ((query.lower() in entry.getTagList()) and (not added)):
                    hitList.append(entry)
                    added = True
        Memory.printHits(hitList)
            

    def searchMatchAll(self, queries):
        hitList = []
        for entry in self.storage:
            added = False
            match = [False]*len(queries)
            for counter in range(len(queries)):
                if (queries[counter].lower() in entry.getTagList()):
                    match[counter] = True
            if not (False in match):
                hitList.append(entry)
        Memory.printHits(hitList)

    def searchListValues(self, queries):
        hitList = []
        for entry in self.storage:
            added = False
            match = [False]*len(queries)
            for counter in range(len(queries)):
                if (queries[counter].lower() in entry.getTagList()):
                    match[counter] = True
            if not (False in match):
                hitList.append(entry)
        for each in hitList:
            each.printValue()

    def getByID(self, ID):
        for entry in self.storage:
            if entry.getID() == int(ID):
                return entry
        #Should print error if no entry is found with that ID
        print("Couldn't find that entry")

    def createEntry(self, name, value, tagList):
        newID = self.assignNewID()
        return ENTRY(newID, name, value, tagList)

    def addNewEntry(self, name, value, tagList):
        toAdd = self.createEntry(name, value, tagList)
        self.add(toAdd)
