

class Symbol():

    def __init__(self):
        self.type = None
        self.name = None
        self.value = None
        self.params = None

    @property
    def hasParameters(self):
        if self.params is None:
            return False
        if len(self.params) == 0:
            return False
        
        return True
    
    def __str__(self):
        result = "{} {} {}\n ".format(self.name, self.value, self.declaration)
        for i in self.usages:
            result += "({}:{})".format(i[0],i[1])
        return result

class SymbolTable():

    ID = 0

    def __init__(self):
        self.__symbols = {}
        self.reset()

    def debug(self):
        for k,s in self.__symbols.items():
            print( "{} {}".format(k,s) )
    ##
    #
    #
    def reset(self):
        self.__symbols = {}

    def getId(self,name):

        for k,s in self.__symbols.items():
            if s.name == name:
                return k
            
        return None
    
    ##
    #
    #
    def addSymbol(self, name, value=None, params=None):

        id = self.getId(name)
        if id:
            symbol = self.__symbols[id]
        else:
            id = "#{:0>3}".format(SymbolTable.ID)
            symbol = Symbol()

        symbol.name = name
        symbol.value = value
        symbol.params = params

        self.__symbols[id] = symbol
        SymbolTable.ID += 1
        return id

    ##
    #
    #
    def removeSymbol(self,name):
        id = self.getId(name)
        del self.__symbols[id]

    ##
    #
    #
    def symbolExists(self, name):

        keys = list(self.__symbols.keys())
        keys.sort(key=len)
        for key in keys:
            symbol = self.getSymbol(key)
            if name == symbol.name:
                return True
        return False
    
    ##
    #
    #
    def getSymbol(self, name):
        return self.__symbols[name]
    
    ## Replaces all Symbols in line
    #  with the symbols' values.
    #
    def replaceSymbols(self, line):
        
        keys = list(self.__symbols.keys())
        keys.sort(key=len)
        
        for key in keys:
            
            symbol = self.getSymbol(key)
            
            if not symbol.hasParameters:
                line = line.replace(symbol.name,symbol.value)

            else:
                
                
                # position of the macro call
                #startPos = line.find(key)
                startPos = line.find(symbol.name)
                
                # we found a macro call
                # If the macro call is followed by a open parenthesis 
                # we scan for parameters
                if startPos >= 0 and line[startPos+len(symbol.name)] == "(":

                    currentPos = startPos + len(symbol.name)
                    macroParameters = {}
                    currentParameter = 0
                    macroParameters[currentParameter] = ""
                    
                    # nesting level for parenthesis
                    level = 0
                    
                    #
                    # We extract parameters from macro call.
                    #
                    while True:
                        
                        c = line[currentPos]
                        
                        if c == "(":
                            level += 1
                            if level > 1:
                                # we are not interested in ( on level 0.
                                macroParameters[currentParameter] += c
                        
                        elif c == ")" and level == 1:
                            # we reached the end of parameter list
                            currentPos += 1
                            break

                        elif c == ")":
                            # we found a ) of part of the parameter
                            level -= 1
                            macroParameters[currentParameter] += c

                        
                        elif c == "," and level == 1:
                            # next parameter starts
                            currentParameter += 1
                            macroParameters[currentParameter] = ""
                        
                        else:
                            # c is part of the parameter
                            macroParameters[currentParameter] += c

                        currentPos += 1
                        
                        if currentPos >= len(line):
                            # we reached the end of the line
                            # but the closing ) is missing
                            raise ValueError( "Macro call '{}' seems missing a closing parenthesis!".format(key) )

                    #
                    # Do the call have the same amount of parameters as the macro definition?
                    #
                    if len(macroParameters) != len(symbol.params):
                        raise ValueError( "Macro call '{}' has the wrong amount of parameters!".format(key) )
                    
                    #
                    # we take the macro value and replace each parameter with it's value.
                    #
                    macroLine = symbol.value

                    for i,p in enumerate(symbol.params):
                        macroLine = macroLine.replace( p,macroParameters[i] )

                    #
                    # We replace the macro call by the parst macroLine
                    #
                    linePrefix = line[:startPos]
                    lineSuffix = line[currentPos:]
                    line = linePrefix + macroLine + lineSuffix

        return line
