class ENTRY:
    
    def __init__(self, idNum, nickName, value, tagList):
        self.idNum = idNum
        self.nickName = nickName
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

    def getNickName(self):
        return self.nickName

    def setNickName(self, newName):
        self.nickName = newName

    def __str__(self):
        return self.nickName

    def printDetail(self):
        print('Entry "{}"'.format(self.nickName))
        print('\tID: {}'.format(self.idNum))
        print('\tvalue: {}'.format(self.value))
        print('\ttags: {',end="")
        for index in range(len(self.tagList)):
            #if the last item in the list, no comma
            if (index == len(self.tagList)-1):
                print(self.tagList[index],end="}\n")
            else:
                print(self.tagList[index],end=", ")

    def addTag(self, newTag):
        self.tagList.append(newTag)
                
    def removeTag(self, toRemove):
        self.tagList.remove(toRemove)
