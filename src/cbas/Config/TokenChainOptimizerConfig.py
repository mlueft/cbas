import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Lexer.TokenTypes

TokenTypes          = cbas.Lexer.TokenTypes.TokenTypes
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenChainOptimizer
TokenRemove         = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenRemover
TokenDebugger       = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenDebugger

class TokenChainOptimizerConfig():

    def __init__(self):
        self.passes = [
            #{ "instance":TokenRemove([ TokenTypes.LINESTART, TokenTypes.LINEEND ]) }
            { "instance":TokenDebugger() }
        ]
    