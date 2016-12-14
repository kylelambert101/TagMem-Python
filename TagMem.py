#TagMem Version 7.2.0
from Memory import Memory
from ENTRY import ENTRY
from datetime import datetime
import pickle, webbrowser

memory = []
dropboxMemoryFilePath = 'pathToMemory'
localMemoryFilePath = '../Resources/myMemory.dat'
changelog = []
'''
To be correctly parsed, changelog should be a List of tuples
(changeItem string, datetime.now())
The string changeItem should be formatted as:
<command>$---$<arguments>
specific to the command.
add$---$<name>$---$<value>$---$<comma-separated tags>
remove$---$<ID>$---$<checkValue>
update$---$<ID>$---$<checkValue>$---$<field>$---$<new value>
associate$---$<tag1>$---$<tag2>
hide$---$<ID>$---$<checkValue>
unhide$---$<ID>$---$<checkValue>
'''

def createEntryDialogue():
    global memory
    name = input("Name: ")
    value = input("Value: ")
    tagString = input("Enter tags in the following format: tag1 tag2 tag3...\n-->")
    tagList = tagString.lower().split(' ')
    freshID = memory.addNewEntry(name, value, tagList)
    print("New Entry added! (ID {})".format(freshID))
    changeItem = 'add$---${}$---${}$---$'.format(name,value)
    tags = ','.join(tagList)
    changeItem = changeItem + tags
    changelog.append((changeItem,datetime.now()))
    saveMemory()

def loadMemory(start=False):
    global memory, changelog
    
    try:
        memFile = open(dropboxMemoryFilePath, "rb")
        memory = pickle.load(memFile)
        if start:
            print("Memory file successfully loaded.")
        memFile.close()
    except:
        print("No Memory file exists.  A new one will be made.")
        memory = Memory()

    try:
        cFilename = "../Resources/changeLog.dat"
        cFile = open(cFilename, "rb")
        changelog = pickle.load(cFile)
        if start:
            print("Change Log successfully loaded.")
        cFile.close()
    except:
        print("No Change Log exists. A new one will be made.")
        
def saveMemory():
    global memory,changelog
    filename = dropboxMemoryFilePath
    file = open(filename, "wb")
    if file == None:
        print("There was an error creating the file")
        return
    pickle.dump(memory, file)
    file.close()
    print("Saved Memory to",filename)

    cFilename = "../Resources/changelog.dat"
    cFile = open(cFilename, "wb")
    if cFile == None:
        print("There was an error creating the changelog file")
        return
    pickle.dump(changelog,cFile)
    cFile.close()
    print("Saved Change Log to ",cFilename)

def printHelp():
    print()
    print("The following are the available commands for the TagMem program:")
    print("add -- opens add dialogue")
    print("add STRING -- generates and adds new entry from STRING info")
    print("associate TAG1 TAG2 -- associates TAG2 with TAG1 in the database")
    print("help -- prints this super helpful list")
    print("hide ID -- hides specified entry from future searches")
    print("lookup TASK -- creates a new lookup entry")
    print("lookuplist -- lists all lookup entries")
    print("opentabs ID -- opens all URLs from specified entry in browser")
    print("print detail -- prints detail view of full memory")
    print("quickprint -- prints ID and name of all entries in memory")
    print("remove ENTRYID -- removes the entry with the given ID")
    print("save -- saves the current memory to myMemory.dat")
    print("search QUERY -ARGS $IGTAG -- performs search on all QUERY TERMS")
    print("\t-any/-all - specifies whether to match all or any queries")
    print("\t-r/-name/-value/-detail - specifies what information to print")
    print("\t*entries that contain IGTAG will be skipped in search")
    print("supersearch -- replaces search, includes hidden entries")
    print("todo TASK -- creates a new todo entry with the value TASK")
    print("unhide ID -- exposes specified entry to future searches")
    print("update ID -- opens edit dialogue for the specified entry")
    print("url ID -- opens specified entry's URL in default web browser")
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
    tag1 = toAssociate[0]
    tag2 = toAssociate[1]
    changeItem = 'associate$---${}$---${}'.format(tag1,tag2)
    changelog.append((changeItem,datetime.now()))
    memory.getByID(440).addTag("{}:{}".format(tag1,tag2))
    print("Tags associated. Associations will update when the program closes")
    saveMemory()

def updateAssociations():
    #get associatedTags from entry 440
    associatedList = memory.getByID(440).getTagList()[1:]
    associatedList.remove('_hide_')

    associatedPairs = []
    #parse into two-element lists
    for pairString in associatedList:
        associatedPairs.append(pairString.split(':'))
    
    for pair in associatedPairs:
        memory.associateTags(pair[0],pair[1])

    saveMemory()

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
        changeItem = 'remove$---${}$---${}'.format(entryID,entry.getName())
        changelog.append((changeItem,datetime.now()))
        memory.remove(entry)
        print("Entry removed")
        saveMemory()
    else:
        return

def expressAdd(toAdd, prefix='', extraTags=''):
    name = prefix+toAdd
    value = toAdd
    #below needed to prevent extra blank tag in
    #cases where extraTags is empty
    if (len(extraTags) >0):
        spacer = ' '
    else:
        spacer = ''
    tagString = toAdd+spacer+extraTags
    tagList = tagString.lower().split(' ')
    freshID = memory.addNewEntry(name, value, tagList)
    print("New Entry Added (ID {})".format(freshID))
    changeItem = 'add$---${}$---${}$---$'.format(name,value)
    tags = ','.join(tagList)
    changeItem = changeItem + tags
    changelog.append((changeItem,datetime.now()))
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
        editField = ''
        edited = True
        if editChoice.lower().startswith('new name '):
            newName = editChoice[9:]
            changeItem = 'update$---${}$---${}$---$name$---${}'.format(toUpdate.getID(),toUpdate.getName(),newName)
            toUpdate.setName(newName)
        elif editChoice.lower().startswith('new value '):
            newValue = editChoice[10:]
            changeItem = 'update$---${}$---${}$---$value$---${}'.format(toUpdate.getID(),toUpdate.getName(),newValue)
            toUpdate.setValue(newValue)
        elif editChoice.lower().startswith('add tag '):
            newTag = editChoice[8:]
            changeItem = 'update$---${}$---${}$---$addTag$---${}'.format(toUpdate.getID(),toUpdate.getName(),newTag)
            toUpdate.addTag(newTag)
        elif editChoice.lower().startswith('remove tag '):
            rTag = editChoice[11:]
            changeItem = 'update$---${}$---${}$---$remTag$---${}'.format(toUpdate.getID(),toUpdate.getName(),rTag)
            toUpdate.removeTag(rTag)
        elif editChoice.lower() == 'done':
            print("Returning to main menu")
            return
        else:
            print("That didn't make sense to me.")
            edited = False
        if edited:
            changelog.append((changeItem,datetime.now()))
            saveMemory()
            print("Entry updated")

def getHits(queryList, allorany):
    if len(queryList) == 0:
        print("Hey! There were no searchable tags!")
        return []
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
    ignoreList = ['_hide_']#ignore hidden entries
    for token in inputList:
        if token.startswith('-'):
            argList.append(token)#add to argList
        elif token.startswith('$'):
            ignoreList.append(token[1:])#add to ignoreList
            
    #magic voodoo that returns queries sans-arguments
    queries = [each for each in inputList if not (each.startswith('-') or each.startswith('$')) ]
    
    if '-any' in argList:
        inclusionParam = 'any'

    hits = getHits(queries, inclusionParam)

    #remove any hits with the ignore tag
    for iTag in ignoreList:
        hits = [hit for hit in hits if iTag not in hit.getTagList()]

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

def hide(inputList):
    #inputList should have only one entry and it should be an id.
    if len(inputList)!=1:
        print("That wasn't formatted correctly. Try again")
        return
    entryID = inputList[0]
    if not (memory.isValidID(entryID)):
        print("Not a valid ID")
        return

    toHide = memory.getByID(entryID)

    #make sure user wants to hide this entry
    print("Are you sure you want to hide this entry?")
    toHide.printDetail()
    doIt = input("(y/n)-->")

    if doIt.lower().startswith('n'):
        print("Aborting")
        return
    
    #now for the hiding
    changeItem = 'hide$---${}$---${}'.format(toHide.getID(),toHide.getName())
    changelog.append((changeItem,datetime.now()))
    toHide.addTag('_hide_')
    print("Entry {} hidden".format(entryID))
    saveMemory()

def unhide(inputList):
    #inputList should have only one entry and it should be an id.
    if len(inputList)!=1:
        print("That wasn't formatted correctly. Try again")
        return
    entryID = inputList[0]
    if not (memory.isValidID(entryID)):
        print("Not a valid ID")
        return

    toExpose = memory.getByID(entryID)
    #entry should be hidden.
    if '_hide_' not in toExpose.getTagList():
        print("Entry {} is not hidden.".format(entryID))
        return
    #else
    changeItem = 'unhide$---${}$---${}'.format(toExpose.getID(),toExpose.getName())
    changelog.append((changeItem,datetime.now()))
    toExpose.removeTag('_hide_')
    print('Entry {} unhidden'.format(entryID))
    saveMemory()

def supersearch(inputList):
    #unhide everything
    for entry in memory.storage:
        for tag in entry.getTagList():
            if tag == '_hide_':
                entry.removeTag('_hide_')
                entry.addTag('xhide_')
    #regular search with inputList
    searchDispatch(inputList)
    #rehide the hidden things
    for entry in memory.storage:
        for tag in entry.getTagList():
            if tag == 'xhide_':
                entry.removeTag('xhide_')
                entry.addTag('_hide_')

def dispatch(userInput):
    loadMemory()
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
        expressAdd(rawInput[5:], "","todo")
    elif command == 'todolist':
        nameList(getHits(['todo'],'all'))
    elif command == 'wish' and len(args)>0:
        expressAdd(rawInput[5:],"",'wishlist wish list')
    elif command == 'wishlist':
        valueList(getHits(['wish'],'all'))
    elif command == "url":
        openURL(args)
    elif command == 'lookup' and len(args)>0:
        expressAdd(rawInput[7:],'Lookup: ','lookup look up todo')
    elif command == 'lookuplist':
        valueList(getHits(['lookup'],'all'))
    elif command == 'opentabs':
        openTabs(args)
    elif command == 'associate':
        associateTags(args)
    elif command == 'hide':
        hide(args)
    elif command == 'unhide':
        unhide(args)
    elif command == 'supersearch':
        supersearch(args)
    else:
        print("I didn't recognize that command")
    
def main():
    global memory
    print("Welcome to your memory!")
    start = True
    while True:
        loadMemory(start)
        start = False
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
            print("TTYL!")
            return
        dispatch(userChoice)
        print('\n\n')
       
main()
