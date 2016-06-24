#TagMem Version 5.1
from Memory import Memory
from ENTRY import ENTRY
import pickle, webbrowser

memory = []
associatedList = [('job', 'career'), ('career', 'job'), ('url', 'webpage')]

def createEntryDialogue():
    global memory
    name = input("Name: ")
    value = input("Value: ")
    tagString = input("Enter tags in the following format: tag1 tag2 tag3...\n-->")
    tagList = tagString.lower().split(' ')
    memory.addNewEntry(name, value, tagList)
    saveMemory()

def updateEntry(entryID):
    if not (memory.isValidID(entryID)):
        print("Not a valid ID")
        return
    while True:
        print("What about the following entry would you like to change?")
        print("Type 'done' when done.")
        toUpdate = memory.getByID(entryID)
        toUpdate.printDetail()
        editChoice = input('\n-->')
        if editChoice.lower().startswith('new name '):
            toUpdate.setname(editChoice[9:])
        elif editChoice.lower().startswith('new value '):
            toUpdate.setValue(editChoice[10:])
        elif editChoice.lower().startswith('add tag '):
            toUpdate.addTag(editChoice[8:])
        elif editChoice.lower().startswith('remove tag '):
            toUpdate.removeTag(editChoice[11:])
        elif editChoice.lower() == 'done':
            print("Returning to main menu")
            return
        else:
            print("That didn't make sense to me.")
        saveMemory()
        print("Entry updated")

def loadMemory():
    global memory
    try:
        filename = "../Resources/myMemory.dat"
        file = open(filename, "rb")
        memory = pickle.load(file)
        print("Memory file successfully loaded.")
        file.close()
    except:
        print("No Memory file exists.  A new one will be made.")
        memory = Memory()
        
def saveMemory():
    global memory
    filename = "../Resources/myMemory.dat"
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
    print("update ID -- opens edit dialogue for the specified entry")
    print("help -- prints this super helpful list")
    print("lookup TASK -- creates a new lookup entry which can be found under todolist and lookuplist")
    print("lookuplist -- lists all lookup entries")
    print("print detail -- prints detail view of full memory")
    print("quickprint -- prints ID and name of all entries in memory")
    print("remove ENTRYID -- removes the entry with the given ID")
    print("save -- saves the current memory to myMemory.dat")
    print("search QUERY -- searches memory for given query (not case sensitive) and displays detail print of results")
    print("todo TASK -- creates a new todo entry with the value TASK")
    print("valuelist QUERY -- prints only values of search results for given query")
    print("view ID -- displays detail print of entry with given ID")

def removeProtocol(entryID):
    if not(memory.isValidID(entryID)):
        return
    entry = memory.getByID(entryID)
    print("Are you sure you want to remove the following entry?")
    entry.printDetail()
    sure = input("-->")
    if (sure.lower().startswith('y')):
        memory.remove(entry)
        print("Entry removed")
        saveMemory()
    else:
        return

def valueList(query):
    queryList = query.split(' ')
    memory.searchListValues(queryList)

def nameList(query):
    queryList = query.split(' ')
    memory.searchListNames(queryList)

def openURL(searchID):
    if not memory.isValidID(searchID):
        return
    url = memory.getByID(searchID).getValue()
    webbrowser.open(url)

def expressAdd(toAdd, prefix='', extraTags=''):
    name = prefix+toAdd
    value = toAdd
    tagString = toAdd+' '+extraTags
    tagList = tagString.lower().split(' ')
    memory.addNewEntry(name, value, tagList)
    print("New Entry Added")
    saveMemory()

def openTabs(anID):
    if not memory.isValidID(anID):
        return
    someURLs = memory.getByID(anID).getValue()
    urlList = someURLs.split(' ')
    for each in urlList:
        webbrowser.open(each)

def associateTags(inputString):
    toAssociate = inputString.split(' ')
    if not (len(toAssociate) == 2):
        print("That was not formatted correctly")
    memory.associateTags(toAssociate[0],toAssociate[1])

def updateAssociations():
    for pair in associatedList:
        memory.associateTags(pair[0],pair[1])
    

def dispatch(userInput):
    rawInput = userInput
    userInput = userInput.lower()
    if userInput.startswith('search '):
        nameList(userInput[7:])
    elif userInput.startswith('detail '):
        memory.searchMatchAll(userInput[7:].split(' '))
    elif userInput.startswith('searchany '):
        memory.searchMatchOne(userInput[10:].split(' '))
    elif userInput.startswith('view '):
        if memory.isValidID(userInput[5:]):
            memory.getByID(userInput[5:]).printDetail()
    elif userInput.startswith('update '):
        updateEntry(userInput[7:])
    elif userInput == 'help':
        printHelp()
    elif userInput == 'save':
        saveMemory()
    elif userInput == 'quickprint':
        memory.printSimple()
    elif userInput == 'print detail':
        memory.printDetail()
    elif userInput  == 'add':
        createEntryDialogue()
    elif userInput.startswith('add '):
        expressAdd(rawInput[4:])
    elif userInput.startswith('remove '):
        removeProtocol(userInput[7:])
    elif userInput.startswith('valuelist '):
        valueList(userInput[10:])
    elif userInput.startswith('todo '):
        expressAdd(rawInput[5:], "","todo to do")
    elif userInput == 'todolist':
        nameList('todo')
    elif userInput.startswith('wish '):
        expressAdd(rawInput[5:],"",'wishlist wish list')
    elif userInput == 'wishlist':
        valueList('wish')
    elif userInput.startswith("url "):
        openURL(rawInput[4:])
    elif userInput.startswith('lookup '):
        expressAdd(rawInput[7:],'Lookup: ','lookup look up todo to do')
    elif userInput == 'lookuplist':
        valueList('lookup')
    elif userInput.startswith('opentabs '):
        openTabs(userInput[9:])
    elif userInput.startswith('associate tags '):
        associateTags(userInput[15:])
    else:
        print("I didn't recognize that command")
    
def main():
    global memory
    loadMemory()
    print("Welcome to your memory!")
    while True:
        print("---------------------------------------------")
        print("What would you like to do?")
        userChoice = input("-->")
        if userChoice.lower() == 'exit':
            shouldSave = input("Do you want to save before exiting?")
            if (shouldSave.lower().startswith('y')):
                updateAssociations()
                saveMemory()
            else:
                print("Alright, whatevs.")
                updateAssociations()
            print("TTYL!")
            return
        dispatch(userChoice)
        print('\n\n')
       
main()
