
class TokenchainOptimizer():

    def __init__(self):
        self.removeTypes = [
            #"linestart",
            #"lineend"
        ]

    def optimize(self, token):
        
        while token:
            if token.type in self.removeTypes:
                print("remove {}".format(token.type) )
                token.remove()
            
            token = token.next
        
    