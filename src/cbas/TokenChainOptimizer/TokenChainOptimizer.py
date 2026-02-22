import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

class TokenchainOptimizer():

    def __init__(self):
        self.removeTypes = [
            #TokenTypes.LINESTART,
            #TokenTypes.LINEEND
        ]

    def main(self, token):
        
        while token:
            if token.type in self.removeTypes:
                print("remove {}".format(token.type) )
                token.remove()

            token = token.next
        
    