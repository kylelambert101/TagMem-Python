from Memory import Memory
from ENTRY import ENTRY
import pickle

menu = ['Add Entry', 'QuickSearch','Search Memory', 'QuickPrint','Print Detail', 'Edit Entry','Save','Exit']
memory = []

def printMenu():
    print("---------------------------------------------")
    print("What would you like to do? (Enter a number)")
    for i in range(len(menu)):
        print("{}) {}".format(i,menu[i]))

def getCommand(number):
    return menu[number]

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

def searchDialogue():
    print()
    numTags = input("How many tags would you like to search for?\n-->")
    both = input("Please select parameters:\n1)Match all tags\n2)Match at least one tag\n-->")
    searchTags = []
    for count in range(int(numTags)):
        newTag = input("Enter tag to search: ")
        searchTags.append(newTag)
    if (both == '1'):
        memory.searchMatchAll(searchTags)
    elif (both == '2'):
        memory.searchMatchOne(searchTags)
    else:
        print("There was a problem with your search parameters")

def changeTags(entryID):
    addOrRemove = input("Please select the number of the action you would like to perform:\n1)Add Tag\n2)Remove Tag\n-->")
    if (addOrRemove == '1'):
        toAdd = input("What is the tag you would like to add?")
        memory.addTag(entryID, toAdd)
    elif(addOrRemove == '2'):
        toRemove = input("Which tag would you like to remove")
        memory.removeTag(entryID, toRemove)

def changeEntry():
    entryID = input("Please enter the ID of the entry you wish to edit")
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
        '''
        tagString = input("Enter tags in the following format: tag1 tag2 tag3...\nNote: No spaces allowed in a single tag\n-->")
        tagList = tagString.split(' ')
        for each in tagList:
            each = each.lower()
        memory.getByID(entryID).setTagList(tagList)
        '''
    else:
        print("Invalid field type")
        return

        
def executeCommand(number):
    stringCommand = getCommand(number)
    if (stringCommand == 'Search Memory'):
        searchDialogue()
    elif (stringCommand == 'Add Entry'):
        newEntry = createEntry()
        memory.add(newEntry)
        saveMemory()
    elif (stringCommand == 'QuickSearch'):
        query = input("What is your search query?\n-->")
        queryList = [query]
        memory.searchMatchAll(queryList)
    elif (stringCommand == 'QuickPrint'):
        memory.printSimple()
    elif (stringCommand == 'Print Detail'):
        memory.printDetail()
    elif (stringCommand == 'Edit Entry'):
        changeEntry()
    elif (stringCommand == 'Save'):
        saveMemory()
    else:
        print("Uh oh. Trying to execute a non-existent command")

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
    
def main():
    global memory
    loadMemory()
    print("Welcome to your memory!")
    while True:
        printMenu()
        userChoice = input("-->")

        #if user selected exit, just quit. But with style.
        if (getCommand(int(userChoice)) == 'Exit'):
            shouldSave = input("Do you want to save before exiting? (y/n)")
            if (shouldSave == 'y'):
                saveMemory()
            else:
                print("Alright, whatevs.")
            print("TTYL!")
            return
        
        if (int(userChoice) not in range(len(menu))):
            print("That was not an option.")
        else:
            executeCommand(int(userChoice))
            #use the command to determine what to do
        print('\n\n')
       
main()
