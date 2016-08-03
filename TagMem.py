#TagMem Version 6
from Memory import Memory
from ENTRY import ENTRY
import pickle, webbrowser

memory = []
associatedList = [('job', 'career'), ('career', 'job'), ('url', 'webpage'), ('raspberry','linda'),('pi','linda'),('linda','raspberry'),('linda','pi')]

def createEntryDialogue():
    global memory
    name = input("Name: ")
    value = input("Value: ")
    tagString = input("Enter tags in the following format: tag1 tag2 tag3...\n-->")
    tagList = tagString.lower().split(' ')
    freshID = memory.addNewEntry(name, value, tagList)
    print("New Entry added! (ID {})".format(freshID))
    saveMemory()

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
    print()
    print("The following are the available commands for the TagMem program:")
    print("add -- starts the add dialogue for adding a new entry to memory")
    print("associatetags TAG1 TAG2 -- adds TAG2 to any entry with TAG1")
    print("help -- prints this super helpful list")
    print("lookup TASK -- creates a new lookup entry which can be found under todolist and lookuplist")
    print("lookuplist -- lists all lookup entries")
    print("opentabs ID -- opens all URLs from specified entry value in default web browser")
    print("print detail -- prints detail view of full memory")
    print("quickprint -- prints ID and name of all entries in memory")
    print("remove ENTRYID -- removes the entry with the given ID")
    print("save -- saves the current memory to myMemory.dat")
    print("search QUERY -- searches memory for given query (not case sensitive) and displays detail print of results")
    print("todo TASK -- creates a new todo entry with the value TASK")
    print("update ID -- opens edit dialogue for the specified entry")
    print("url ID -- opens the URL value of the specified entry in default web browser")
    print("valuelist QUERY -- prints only values of search results for given query")
    print("view ID -- displays detail print of entry with given ID")

#updated to use inputList----------------------------------------------

def openURL(inputList):
    if len(inputList) != 1:
        print("That wasn't formatted correctly")
        return
    searchID = inputList[0]
    if not memory.isValidID(searchID):
        print("Not a valid ID")
        return
    url = memory.getByID(searchID).getValue()
    webbrowser.open(url)

def openTabs(inputList):
    if len(inputList) != 1:
        print("That wasn't formatted correctly")
        return
    anID = inputList[0]    
    if not memory.isValidID(anID):
        print("Not a valid ID")
        return
    someURLs = memory.getByID(anID).getValue()
    urlList = someURLs.split(' ')
    for each in urlList:
        webbrowser.open(each)

def associateTags(inputList):
    toAssociate = inputList
    if not (len(toAssociate) == 2):
        print("That was not formatted correctly")
    memory.associateTags(toAssociate[0],toAssociate[1])

def updateAssociations():
    for pair in associatedList:
        memory.associateTags(pair[0],pair[1])

def removeProtocol(inputList):
    if len(inputList)!=1:
        print("That wasn't formatted correctly. Try again")
        return
    entryID = inputList[0]    
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

def expressAdd(toAdd, prefix='', extraTags=''):
    name = prefix+toAdd
    value = toAdd
    tagString = toAdd+' '+extraTags
    tagList = tagString.lower().split(' ')
    freshID = memory.addNewEntry(name, value, tagList)
    print("New Entry Added (ID {})".format(freshID))
    saveMemory()

def updateEntry(inputList):
    if len(inputList)!=1:
        print("That wasn't formatted correctly. Try again")
        return
    entryID = inputList[0]
    if not (memory.isValidID(entryID)):
        print("Not a valid ID")
        return
    while True:
        print("\n\nWhat about the following entry would you like to change?")
        print("Type 'done' when done.")
        toUpdate = memory.getByID(entryID)
        toUpdate.printDetail()
        editChoice = input('\n-->')
        if editChoice.lower().startswith('new name '):
            toUpdate.setName(editChoice[9:])
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

def getHits(queryList, allorany):
    if allorany == 'all':
        hitList = memory.searchMatchAll(queryList)
    else:
        hitList = memory.searchMatchAny(queryList)
    return hitList

def valueList(hitList):
    for each in hitList:
        print('{}: {}'.format(each.getID(),each.getValue()))

def nameList(hitList):
    for each in hitList:
        print('{}: {}'.format(each.getID(),each.getName()))

def revealPrint(hitList):
    for each in hitList:
        print('\n{}: {}'.format(each.getID(),each.getName()))
        print('\t{}'.format(each.getValue()))

def detailPrint(hitList):
    for each in hitList:
        each.printDetail()

def searchDispatch(inputList):
    inclusionParam = 'all' #default
    argList = []
    for token in inputList:
        if token.startswith('-'):
            argList.append(token)#add to argList
            
    #magic voodoo that returns queries sans-arguments
    queries = [each for each in inputList if not each.startswith('-')]
    
    if '-any' in argList:
        inclusionParam = 'any'

    hits = getHits(queries, inclusionParam)

    if '-value' in argList:
        valueList(hits)
    elif '-r' in argList:
        revealPrint(hits)
    elif '-detail' in argList:
        detailPrint(hits)
    else:#default print name
        nameList(hits)

def view(inputList):
    #correctly formatted, inputList should be the id to view
    if len(inputList) !=1:
        print("That wasn't formatted correctly.")
        return
    toView = inputList[0]
    if memory.isValidID(toView):
        memory.getByID(toView).printDetail()
    
def dispatch(userInput):
    rawInput = userInput
    userInput = userInput.lower()
    inputList = userInput.split(' ')
    if len(inputList) == 0:
        print("No input detected. Do better next time.")
        return
    command = inputList[0]
    args = inputList[1:]
    if command == 'search':
        searchDispatch(args)
    elif command == 'view':
        view(args)
    elif command == 'update':
        updateEntry(args)
    elif command == 'help':
        printHelp()
    elif command == 'save':
        saveMemory()
    elif command == 'quickprint':
        memory.printSimple()
    elif command == 'print' and args == ['detail']:
        memory.printDetail()
    elif command == 'add' and len(args) == 0:#if the input is just 'add'
        createEntryDialogue()
    elif command == 'add':#if there's more after add
        expressAdd(' '.join(args))#make it a string again
    elif command == 'remove':
        removeProtocol(args)
    elif command == 'todo' and len(args)>0:#make sure there's more after todo
        expressAdd(rawInput[5:], "","todo to do")
    elif command == 'todolist':
        nameList(getHits(['todo'],'all'))
    elif command == 'wish' and len(args)>0:
        expressAdd(rawInput[5:],"",'wishlist wish list')
    elif command == 'wishlist':
        valueList(getHits(['wish'],'all'))
    elif command == "url":
        openURL(args)
    elif command == 'lookup' and len(args)>0:
        expressAdd(rawInput[7:],'Lookup: ','lookup look up todo to do')
    elif command == 'lookuplist':
        valueList(getHits(['lookup'],'all'))
    elif command == 'opentabs':
        openTabs(args)
    elif command == 'associate':
        associateTags(args)
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
