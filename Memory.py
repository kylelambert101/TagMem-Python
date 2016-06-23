from ENTRY import ENTRY
class Memory:
    
    def __init__(self):
        #store entries in a dictionary
        self.storage = dict()
        #IDnum to assign to next Entry
        self.nextEntryID = 0

    def isValidID(self, ID):
        return self.storage.has_key(ID)

    def add(self, anEntry, newID):
        self.storage[''+newID] = anEntry

    def remove(self, entryID):
        del self.storage[entryID]

    def assignNewID(self):
        toAssign = self.nextEntryID
        self.nextEntryID +=1
        return toAssign
      
    def printSimple(self):
        for entry in self.storage.values():
            print('{}: {}'.format(entry.getID(), entry.getNickName()))
          
    def printDetail(self):
        for entry in self.storage.values():
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
        for entry in self.storage.values():
            added = False
            for query in queries:
                if ((query.lower() in entry.getTagList()) and (not added)):
                    hitList.append(entry)
                    added = True
        Memory.printHits(hitList)

    def searchMatchAll(self, queries):
        hitList = []
        for entry in self.storage.values():
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
        for entry in self.storage.values():
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
        return self.storage[''+ID]

    def createEntry(self, name, value, tagList):
        newID = self.assignNewID()
        return ENTRY(newID, name, value, tagList)

    def addNewEntry(self, name, value, tagList):
        toAdd = self.createEntry(name, value, tagList)
        self.add(toAdd, toAdd.getID())

    def associateTags(self, existing, new):
        #for each entry, if it has existing but not new, add new
        for entry in self.storage.values():
            if entry.hasTag(existing) and not entry.hasTag(new):
                entry.addTag(new)
                print("Updated Entry {}".format(entry.getID()))

