import cbas
import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

class TokenChainOptimizer():

    def __init__(self):
        pass

    def main(self, token):
        pass

class TokenDebugger(TokenChainOptimizer):

    def __init__(self):
        super().__init__()

    def main(self, token):
        while token:
            self.printToken(token)
            token = token.next

    def printToken(self, token):
        print("{}".format(token))
    
    def printToken(self, token):
            colWidth = 30
            _current = str(token)
            _prev = str(token.prev)
            _next = str(token.next)

            if len(_prev) > colWidth: _prev = _prev[:colWidth-3]+"..."
            if len(_current) > colWidth: _current = _current[:colWidth-3]+"..."
            if len(_next) > colWidth: _next = _next[:colWidth-3]+"..."
            formatstring = " * {:<"+str(colWidth)+"} <= {:<"+str(colWidth)+"} => {:<"+str(colWidth)+"}"
            cbas.log(
                formatstring.format(
                    _prev,
                    _current,
                    _next
                ),
                "debug"
            )
    
    

class TokenRemover(TokenChainOptimizer):

    def __init__(self,tokensToRemove):
        self.removeTypes = tokensToRemove

    def main(self, token):
        while token:
            if token.type in self.removeTypes:
                print("remove {}".format(token.type) )
                token.remove()

            token = token.next
