class LexerConfig():

    def __init__(self):
        self.name          = ""
        self.description   = ""
        self.markLinestart = False
        self.markLineend   = True
        self.markEOF       = True
        self.tokens        = []

    def hasTokenType(self, tokenType):

        for t in self.tokens:
            if t.type == tokenType:
                return True
        return False