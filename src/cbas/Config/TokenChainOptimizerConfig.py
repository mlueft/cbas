import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Lexer.TokenTypes

TokenTypes          = cbas.Lexer.TokenTypes.TokenTypes
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenChainOptimizer
TokenRemove         = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenRemover
TokenDebugger       = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenDebugger

class Matrix():


    Definitions = {
        "debug":    { "instance": TokenDebugger() },
        "remove":   { "instance": TokenRemove() }
    }
    Matrix = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "debug":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "remove":          [ 0,    0,    0,    0,    0,    0,    0,    0,    0    ]
    }


class TokenChainOptimizerConfig():

    def __init__(self):
        self.tokens = []
    