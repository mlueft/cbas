
class Label():
    def __init__(self):
        pass

class LabelTable():
    ID = 0
    def __init__(self):
        self.__labels = {}

    def addLabel(self, name):
        found = False
        for l in self.__labels:
            if self.__labels[l][0] == name:
                self.__labels[l][1] += 1
                return l
        
        id = "@label_{:0>5}".format(LabelTable.ID)
        self.__labels[id] = [name,1]
        LabelTable.ID += 1
        return id
    