
class Symbol():

    def __init__(self,name,value,params):
        self.name = name
        self.value = value
        self.params = params

    @property
    def hasParameters(self):
        if self.params is None:
            return False
        if len(self.params) == 0:
            return False
        
        return True
    

class SymbolTable():

    def __init__(self):
        self.__symbols = {}
        self.reset()

    ##
    #
    #
    def reset(self):
        self.__symbols = {}

    ##
    #
    #
    def addSymbol(self, name, value=None, params=None):
        self.__symbols[name] = Symbol( name, value, params )

    ##
    #
    #
    def removeSymbol(self,name):
        del self.__symbols[name]

    ##
    #
    #
    def symbolExists(self, name):
        return name in self.__symbols
    
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
                line = line.replace(key,self.__symbols[key].value)

            else:
                
                
                # position of the macro call
                startPos = line.find(key)
                
                # we found a macro call
                # If the macro call is followed by a open parenthesis 
                # we scan for parameters
                if startPos >= 0 and line[startPos+len(key)] == "(":

                    currentPos = startPos + len(key)
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
