
class CompilerPasses():
    
    POST_LEXER     = 0
    CHECK_SEMANTIC = 1
    POST_PARSER    = 2

    __matchTable = {
        "postLexer":     POST_LEXER,
        "checkSemantic": CHECK_SEMANTIC,
        "postParser":    POST_PARSER,
    }
    
    @staticmethod
    def toType(value):
        if value in CompilerPasses.__matchTable:
            return CompilerPasses.__matchTable[value]
        raise ValueError("CompilerPasses '{}' not recognized!".format(value))

    @staticmethod
    def toString(value):
        for e in CompilerPasses.__matchTable:
            if CompilerPasses.__matchTable[e] == value:
                return e
        #raise ValueError("CompilerPasses'{}' not recognized!".format(value))