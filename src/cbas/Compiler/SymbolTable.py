
class SymbolKind():
    
    VARIABLE_FLOAT     = 0
    VARIABLE_STRING    = 1
    VARIABLE_INTEGER   = 2

    LITERAL_STRING     = 3
    LITERAL_FLOAT      = 4
    LITERAL_INTEGER    = 5
    LITERAL_SCIENTIFIC = 6
    LITERAL_BOOLEAN    = 7

    __matchTable = {
        "variable string":    VARIABLE_STRING,
        "variable float":     VARIABLE_FLOAT,
        "variable integer":   VARIABLE_INTEGER,
        "literal string":     LITERAL_STRING,
        "literal float":      LITERAL_FLOAT,
        "literal integer":    LITERAL_INTEGER,
        "literal scientific": LITERAL_SCIENTIFIC,
        "literal boolean":    LITERAL_BOOLEAN
    }

    @staticmethod
    def toType(value):
        if value in SymbolKind.__matchTable:
            return SymbolKind.__matchTable[value]
        raise ValueError("Token type '{}' not recognized!".format(value))

    @staticmethod
    def toString(value):
        for e in SymbolKind.__matchTable:
            if SymbolKind.__matchTable[e] == value:
                return e
        #raise ValueError("Token type '{}' not recognized!".format(value))

##
#
#
class Symbol():

    def __init__(self):

        # ENUM SymbolKind
        self.kind = None

        # The code represented by the symbol.
        # Its a literal or a variable.
        self.code = None

        # line and pos tuple of declaration
        self.declaration = None

        # list of line and pos tuples of usage
        self.usages = []

        # Name of the variable in generated basic code.
        self.variableName = None

        # placeholder
        # the symbolId
        self.placeholder = ""

    @property
    def hasParameters(self):
        if self.parameters is None:
            return False
        return True

    def isLiteral(self):
        return self.kind in [
            SymbolKind.LITERAL_BOOLEAN, SymbolKind.LITERAL_FLOAT,
            SymbolKind.LITERAL_INTEGER, SymbolKind.LITERAL_SCIENTIFIC,
            SymbolKind.LITERAL_STRING
        ]
    
    def isVariable(self):
        return self.kind in [
            SymbolKind.VARIABLE_FLOAT, SymbolKind.VARIABLE_STRING,
            SymbolKind.VARIABLE_INTEGER
        ]
    
    def __str__(self):
        result = "{} {} {}\n ".format(self.kind, self.code, self.declaration)
        for i in self.usages:
            result += "({}:{})".format(i[0],i[1])
        return result

##
#
#
class SymbolTable():

    __ID = 0

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
        
        # Reuses variable names from scopes
        self.reuseVariables = False

        # build global literals
        self.buildGlobals = False        

    def debug(self):
        for k,s in self.__symbols.items():
            print( "{} {}".format(k,s) )

    ## Deletes all symbols
    #
    #
    def reset(self):
        self.__symbols = {}

    ## Returns the ID of the symbol with the given variable name.
    #
    #
    def getId(self,name):
    
        for k,s in self.__symbols.items():
            if s.code == name:
                return k
            
        return None
    
    ## Returns the symbol of the given ID.
    #
    #
    def getSymbol(self, id):
        return self.__symbols[id]
    
    ##
    #
    #
    def __isGlobal(self, symbol):
        
        if not self.buildGlobals:
            return False
        
        if (len(symbol.usages) >= 1 and symbol.kind != SymbolKind.LITERAL_STRING) or \
            (len(symbol.name) > 4 and len(symbol.usages) >= 1 and symbol.kind == SymbolKind.LITERAL_STRING):
            return True
        return False
    
    ##
    #
    #
    def getGlobals(self):
        result = []

        for k,symbol in self.__symbols.items():
            if symbol.isLiteral():
                if self.__isGlobal(symbol):
                    result.append(symbol)

        return result

    ##
    #
    #
    def getLiterals(self):
        result = []

        for k,symbol in self.__symbols.items():
            if symbol.isLiteral():
                if not self.__isGlobal(symbol):
                    result.append(symbol)

        return result
    
    ## Adds a symbol to the table and returns the unique ID.
    #
    #
    def addSymbol(self, code, line = None, pos = None, kind = 0):
        
        id = self.getId(code)
        if id:
            symbol = self.__symbols[id]
            symbol.usages.append((line,pos))
            return id
        
        id = "#{:0>3}".format(SymbolTable.__ID)

        symbol = Symbol()
        symbol.kind = kind
        symbol.code = code
        symbol.declaration = (line,pos)
        symbol.placeholder = id

        self.__symbols[id] = symbol
        SymbolTable.__ID += 1
        return id

    ## Opens a scope.
    #  All new variables are stored in the current scope.
    #  After closed the scope local variables will be released.
    #
    def openScope(self):
        if not self.reuseVariables:
            return
        
        self.usedVariableNames.append({})

    ## Closes the current scope.
    #  Local variable names will be released.
    #
    def closeScope(self):
        if not self.reuseVariables:
            return
        
        self.usedVariableNames.pop()

    ## Generates a variable name for the symbol defined by id
    #  and returns it.
    #
    def getVariableName(self,id):

        #
        # Return a already fixed variable name
        #
        symbol = self.__symbols[id]

        if symbol.variableName is not None:
            return symbol.variableName

        
        #
        # Generate the next free variable name.
        #
        suffix = ""
        if symbol.kind == SymbolKind.VARIABLE_STRING:
            suffix = "$"
        elif symbol.kind == SymbolKind.VARIABLE_INTEGER:
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

                    #
                    # Store the variable name to the symbol
                    # and return the variable name.
                    #
                    self.usedVariableNames[len(self.usedVariableNames)-1][id] = candidate
                    symbol.variableName = candidate
                    print((" "*len(self.usedVariableNames))+"new: {}".format(candidate))
                    return candidate
        
