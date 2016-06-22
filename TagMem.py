#TagMem Version 2
from Memory import Memory
from ENTRY import ENTRY
import pickle, webbrowser

memory = []

def prompt():
    print("---------------------------------------------")
    print("What would you like to do?")

def createEntry():
    global memory
    nickName = input("Nickname: ")
    value = input("Value: ")
    tagString = input("Enter tags in the following format: tag1 tag2 tag3...\nNote: No spaces allowed in a single tag\n-->")
    tagList = tagString.split(' ')
    for each in tagList:
        each = each.lower()
    idNum = memory.assignNewID()
    myEntry = ENTRY(idNum, nickName, value, tagList)
    return myEntry

def changeTags(entryID):
    addOrRemove = input("Please select the number of the action you would like to perform:\n1)Add Tag\n2)Remove Tag\n-->")
    if (addOrRemove == '1'):
        toAdd = input("What is the tag you would like to add?\n-->")
        memory.addTag(entryID, toAdd)
    elif(addOrRemove == '2'):
        toRemove = input("Which tag would you like to remove?\n-->")
        memory.removeTag(entryID, toRemove)

def changeEntry(entryID):
    if not (memory.isValidID(entryID)):
        print("Not a valid ID")
        return
    memory.getByID(entryID).printDetail()
    fieldType = input("Which attribute of the entry would you like to change?\n1)NickName\n2)Value\n3)Tag List\n-->")
    if (fieldType == '1'):
        newValue = input("What should the new value of this attribute be?")
        memory.getByID(entryID).setNickName(newValue)
    elif (fieldType == '2'):
        newValue = input("What should the new value of this attribute be?")
        memory.getByID(entryID).setValue(newValue)
    elif (fieldType == '3'):
        changeTags(entryID)
    else:
        print("Invalid field type")
        return

def loadMemory():
    global memory
    try:
        filename = "myMemory.dat"
        file = open(filename, "rb")
        memory = pickle.load(file)
        print("Memory file successfully loaded.")
        file.close()
    except:
        print("No Memory file exists.  A new one will be made.")
        memory = Memory()
        
def saveMemory():
    global memory
    filename = "myMemory.dat"
    file = open(filename, "wb")
    if file == None:
        print("There was an error creating the file")
        return
    pickle.dump(memory, file)
    file.close()
    print("Saved Memory to",filename)

def printHelp():
    print("The following are the available commands for the TagMem program:")
    print("add -- starts the add dialogue for adding a new entry to memory")
    print("edit ID -- opens edit dialogue for the specified entry")
    print("help -- prints this super helpful list")
    print("lookup TASK -- creates a new lookup entry which can be found under todolist and lookuplist")
    print("lookuplist -- lists all lookup entries")
    print("print detail -- prints detail view of full memory")
    print("quickprint -- prints ID and Nickname of all entries in memory")
    print("remove ENTRYID -- removes the entry with the given ID")
    print("save -- saves the current memory to myMemory.dat")
    print("search QUERY -- searches memory for given query (not case sensitive) and displays detail print of results")
    print("todo TASK -- creates a new todo entry with the value TASK")
    print("valuelist QUERY -- prints only values of search results for given query")
    print("view ID -- displays detail print of entry with given ID")

def removeProtocol(entryID):
    entry = memory.getByID(entryID)
    print("Are you sure you want to remove the following entry? (y/n)")
    entry.printDetail()
    sure = input("-->")
    if (sure == 'y'):
        memory.remove(entry)
        print("Entry removed")
    else:
        return

def valueList(query):
    queryList = query.split(' ')
    memory.searchListValues(queryList)

def makeToDo(item):
    value = item
    tags = item.split(' ')
    for each in tags:
        each = each.lower()
    tags.append('todo')
    tags.append('to')
    tags.append('do')
    nickName = "Todo: "+item
    idNum = memory.assignNewID()
    newEntry = ENTRY(idNum, nickName, value, tags)
    memory.add(newEntry)
    print("Todo Entry added")
    
def todoList():
    valueList('todo')

def addWish(newWish):
    value = newWish
    tags = newWish.split(' ')
    for each in tags:
        each = each.lower()
    tags.append('wishlist')
    tags.append('wish')
    tags.append('list')
    nickName = "WishList: "+newWish
    idNum = memory.assignNewID()
    newEntry = ENTRY(idNum, nickName, value, tags)
    memory.add(newEntry)
    print("Wishlist Entry added")

def wishList():
    valueList('wishlist')

def openURL(searchID):
    if not memory.isValidID(searchID):
        print("That wasn't a valid ID")
        return
    url = memory.getByID(searchID).getValue()
    webbrowser.open(url)

def addLookup(newThing):
    value = newThing
    tags = newThing.split(' ')
    for each in tags:
        each = each.lower()
    tags.append('lookup')
    tags.append('look')
    tags.append('up')
    tags.append('todo')
    tags.append('to')
    tags.append('do')
    nickName = "Lookup: "+newThing
    idNum = memory.assignNewID()
    newEntry = ENTRY(idNum, nickName, value, tags)
    memory.add(newEntry)
    print("Lookup Entry added")

def lookupList():
    valueList('lookup')

def genericAdd(toAdd):
    value = toAdd
    nickName = toAdd
    tags = toAdd.split(' ')
    idNum = memory.assignNewID()
    newEntry = ENTRY(idNum, nickName, value, tags)
    memory.add(newEntry)
    print("New Entry Added")

def parseCommand(userInput):
    userInput = userInput.lower()
    if userInput.startswith('search '):
        queries = userInput[7:].split(' ')
        for query in queries:
            print("Query: '{}'".format(query))
        memory.searchMatchAll(queries)
    elif userInput.startswith('view '):
        IDtoSearch = userInput[5:]
        if memory.isValidID(IDtoSearch):
            memory.getByID(IDtoSearch).printDetail()
        else:
            print("Not a valid ID")
    elif userInput.startswith('edit '):
        croppedInput = userInput[5:]
        ID = 0
        try:
            ID = int(croppedInput)
        except:
            print("There was a problem with your command")
            return
        changeEntry(ID)
    elif userInput == 'help':
        printHelp()
    elif userInput == 'save':
        saveMemory()
    elif userInput == 'quickprint':
        memory.printSimple()
    elif userInput == 'print detail':
        memory.printDetail()
    elif userInput  == 'add':
        memory.add(createEntry())
        saveMemory()
    elif userInput.startswith('add '):
        genericAdd(userInput[4:])
    elif userInput.startswith('remove '):
        IDtoRemove = userInput[7:]
        if memory.isValidID(IDtoRemove):
            removeProtocol(IDtoRemove)
    elif userInput.startswith('valuelist '):
        valueList(userInput[10:])
    elif userInput.startswith('todo '):
        makeToDo(userInput[5:])
        saveMemory()
    elif userInput == 'todolist':
        todoList()
    elif userInput.startswith('wish '):
        addWish(userInput[5:])
        saveMemory()
    elif userInput == 'wishlist':
        wishList()
    elif userInput.startswith("url "):
        openURL(userInput[4:])
    elif userInput.startswith('lookup '):
        addLookup(userInput[7:])
        saveMemory()
    elif userInput == 'lookuplist':
        lookupList()
    else:
        print("I didn't recognize that command")
    
def main():
    global memory
    loadMemory()
    print("Welcome to your memory!")
    while True:
        prompt()
        userChoice = input("-->")
        if userChoice.lower() == 'exit':
            shouldSave = input("Do you want to save before exiting? (y/n)")
            if (shouldSave == 'y'):
                saveMemory()
            else:
                print("Alright, whatevs.")
            print("TTYL!")
            return
        parseCommand(userChoice)
        print('\n\n')
       
main()
