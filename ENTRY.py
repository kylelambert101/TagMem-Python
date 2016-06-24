class ENTRY:
    
    def __init__(self, idNum, name, value, tagList):
        self.idNum = idNum
        self.name = name
        self.value = value
        self.tagList = tagList

    def getValue(self):
        return self.value

    def getTagList(self):
        return self.tagList

    def setTagList(self, newTagList):
        self.tagList = newTagList

    def addTag(self, newTag):
        self.tagList.append(newTag)

    def setValue(self, newValue):
        self.value = newValue

    def getID(self):
        return self.idNum

    def getname(self):
        return self.name

    def setname(self, newName):
        self.name = newName

    def __str__(self):
        return self.name

    def printDetail(self):
        print('Entry "{}"'.format(self.name))
        print('\tID: {}'.format(self.idNum))
        print('\tvalue: {}'.format(self.value))
        print('\ttags: {',end="")
        for index in range(len(self.tagList)):
            #if the last item in the list, no comma
            if (index == len(self.tagList)-1):
                print(self.tagList[index],end="}\n")
            else:
                print(self.tagList[index],end=", ")

    def printName(self):
        print("({}) {}".format(self.idNum, self.name))

    def addTag(self, newTag):
        self.tagList.append(newTag)
                
    def removeTag(self, toRemove):
        if (toRemove in self.tagList):
            self.tagList.remove(toRemove)
        else:
            print("There is no tag '{}' in {}".format(toRemove, self.name))

    def printValue(self):
        print("({}) {}".format(self.idNum, self.value))

    def hasTag(self, tag):
        return tag in self.tagList
