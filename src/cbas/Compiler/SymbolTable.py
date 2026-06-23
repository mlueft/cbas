
class SymbolKind():
    
    VARIABLE_FLOAT     = 0
    VARIABLE_STRING    = 1
    VARIABLE_INTEGER   = 2

    LITERAL_STRING     = 3
    LITERAL_FLOAT      = 4
    LITERAL_INTEGER    = 5
    LITERAL_SCIENTIFIC = 6
    LITERAL_BOOLEAN    = 7

    FUNCTION           = 8

    __matchTable = {
        "variable string":    VARIABLE_STRING,
        "variable float":     VARIABLE_FLOAT,
        "variable integer":   VARIABLE_INTEGER,
        "literal string":     LITERAL_STRING,
        "literal float":      LITERAL_FLOAT,
        "literal integer":    LITERAL_INTEGER,
        "literal scientific": LITERAL_SCIENTIFIC,
        "literal boolean":    LITERAL_BOOLEAN,
        "function":           FUNCTION
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
        self.symbols = {}
        self.reset()

    def debug(self):
        for k,s in self.symbols.items():
            print( "{} {}".format(k,s) )

    ## Deletes all symbols
    #
    #
    def reset(self):
        self.symbols = {}

    ## 
    #
    #
    def getId(self,code):
        for k,s in self.symbols.items():
            if s.code == code:
                return k
        return None
    
    ## Returns the symbol of the given ID.
    #
    #
    def getSymbol(self, id):
        return self.symbols[id]
    
    ## Adds a symbol to the table and returns the unique ID.
    #
    #
    def addSymbol(self, code, line = None, pos = None, kind = 0):
        
        id = self.getId(code)
        if id:
            symbol = self.symbols[id]
            symbol.usages.append((line,pos))
            return id
        
        id = "#{:0>3}".format(SymbolTable.__ID)

        symbol = Symbol()
        symbol.kind = kind
        symbol.code = code
        symbol.declaration = (line,pos)
        symbol.placeholder = id

        self.symbols[id] = symbol
        SymbolTable.__ID += 1
        return id




        
