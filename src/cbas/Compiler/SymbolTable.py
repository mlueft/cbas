
class Symbol():

    def __init__(self):
        self.type = None
        self.name = None
        self.value = None
        self.parameters = 0
        self.declaration = None
        self.usages = []
        self.variableName = None

    @property
    def hasParameters(self):
        if self.parameters is None:
            return False
        return True
    
    def __str__(self):
        result = "{} {} {} {} {}\n ".format(self.type, self.name, self.value, self.declaration, self.parameters)
        for i in self.usages:
            result += "({}:{})".format(i[0],i[1])
        return result

class SymbolTable():

    ID = 0

    def __init__(self):
        self.__symbols = {}
        self.reset()
        self.usedVariableNames = [{
            "reserved0":"DO",
            "reserved1":"DS",
            "reserved2":"DS$",
            "reserved3":"EL",
            "reserved4":"ER",
            "reserved5":"GO",
            "reserved6":"OR",
            "reserved7":"PI",
            "reserved8":"ST",
            "reserved9":"TI",
            "reserved10":"TI$",
            "reserved11":"TO",
            "reserved12":"π"

        }]
        self.reuseVariables = False

    def debug(self):
        for k,s in self.__symbols.items():
            print( "{} {}".format(k,s) )

    def reset(self):
        self.__symbols = {}

    def getId(self,name):
    
        for k,s in self.__symbols.items():
            if s.name == name:
                return k
            
        return None
    
    def getSymbol(self, id):
        return self.__symbols[id]
    
    ##
    #
    #
    def addSymbol(self, type, name, line = None, pos = None, value=None, params=None):
        print("  addSymbol")
        id = self.getId(name)
        if id:
            symbol = self.__symbols[id]
            symbol.usages.append((line,pos))
            return id
        
        id = "#{:0>3}".format(SymbolTable.ID)

        symbol = Symbol()
        symbol.type = type
        symbol.name = name
        symbol.value = value
        symbol.parameters = params
        symbol.declaration = (line,pos)

        self.__symbols[id] = symbol
        SymbolTable.ID += 1
        return id

    def openScope(self):
        if self.reuseVariables:
            self.usedVariableNames.append({})

    def closeScope(self):
        if self.reuseVariables:
            self.usedVariableNames.pop()

    def obsolet__freeVariable(self,variableName):
        for s in self.usedVariableNames:
            if self.usedVariableNames[s] == variableName:
                del self.usedVariableNames[s]
                return
    
    def getVariable(self,symbolName):

       
        #for i in range(len(self.usedVariableNames)-1,-1,-1):
        #    usedVariableNames = self.usedVariableNames[i]
        #    if symbolName in usedVariableNames:
        #        return usedVariableNames[symbolName]
        
        symbol = self.__symbols[symbolName]

        if symbol.variableName is not None:
            return symbol.variableName

        
        suffix = ""
        if symbol.type == "string":
            suffix = "$"
        elif symbol.type == "integer":
            suffix = "%"
        
        vnames0 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        vnames1 = [""]+vnames0
        for v1 in vnames1:
            for v0 in vnames0:
                candidate = v0+v1+suffix

                found = False
                for i in range(len(self.usedVariableNames)-1,-1,-1):
                    usedVariableNames = self.usedVariableNames[i]
                    for k in usedVariableNames:
                        if usedVariableNames[k] == candidate:
                            found = True

                if not found:

                    self.usedVariableNames[len(self.usedVariableNames)-1][symbolName] = candidate
                    symbol.variableName = candidate
                    print(" new: {}".format(candidate))
                    return candidate
        
