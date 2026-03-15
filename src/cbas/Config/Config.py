from operator import attrgetter

import cbas.Config.LexerConfig
import cbas.Config.ParserConfig
import cbas.Config.AstOptimizerConfig

import cbas.Lexer.TokenTypes
import cbas.Lexer.ConfigToken

import cbas.Parser.BindingPower
import cbas.Parser.ConfigToken

import cbas.Ast.Expressions
import cbas.Ast.Statements

import cbas.AstOptimizer.AstOptimizer
import cbas.AstOptimizer.ConfigToken

import cbas.Config.LexerMatrix
import cbas.Config.ParserMatrix


TokenTypes          = cbas.Lexer.TokenTypes.TokenTypes
BindingPower        = cbas.Parser.BindingPower.BindingPower
LexerConfigToken    = cbas.Lexer.ConfigToken.ConfigToken
LexerConfig         = cbas.Config.LexerConfig.LexerConfig
ParserConfigToken   = cbas.Parser.ConfigToken.ConfigToken
ParserConfig        = cbas.Config.ParserConfig.ParserConfig
ExpressionParser    = cbas.Ast.Expressions.ExpressionParser
StatementParser     = cbas.Ast.Statements.StatementParser
ArithmeticOptimizer = cbas.AstOptimizer.AstOptimizer.ArithmeticOptimizer
LogicOptimizer      = cbas.AstOptimizer.AstOptimizer.LogicOptimizer
AstOptimizerConfig  = cbas.Config.AstOptimizerConfig.AstOptimizerConfig
AstOptimizerToken   = cbas.AstOptimizer.ConfigToken.ConfigToken

class Config():

    ARITHMETIC   = 0
    PREPROCESSOR = 1
    V2           = 2
    V35          = 3
    V36          = 4
    V4           = 5
    V4P          = 6
    V7           = 7
    V10          = 8

    # =============================================
    # LEXER
    # =============================================
    lexerTokens = cbas.Config.LexerMatrix.LexerMatrix.Tokens
    lexerConfig = cbas.Config.LexerMatrix.LexerMatrix.Matrix
    lexerParameters = cbas.Config.LexerMatrix.LexerMatrix.Parameters

    # Order is important

    # =============================================
    # PARSER
    # =============================================
    parserTokens = cbas.Config.ParserMatrix.ParserMatrix.Tokens
    parserConfig = cbas.Config.ParserMatrix.ParserMatrix.Matrix
    parserParameters = cbas.Config.ParserMatrix.ParserMatrix.Parameters

    # Order is important


    # =============================================
    # LEXER OPTIMIZER
    # =============================================

    # =============================================
    # AST OPTIMIZER
    # =============================================

    astOptimizerConfigTokens = {
        "arithmetic": ArithmeticOptimizer,
        "logical"   : LogicOptimizer
    }

    astOptimizerConfig = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "arithmetic":             [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logical":                [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

    }

    def __init__(self, configIndex):
        self.configIndex = configIndex

        pass

    def getLexerToken(self, token):
        return LexerConfigToken(
                            token["type"],
                            token["expression"],
                            token["order"],
                            token["handler"]
                        )
    
    def getParserToken(self, token):
        return ParserConfigToken(
                        token["bindingpower"],
                        token["type"],
                        token["category"],
                        token["handler"],
                    )


    def getLexerConfig(self):
        parameters = Config.lexerParameters[self.configIndex]
        result = LexerConfig()
        result.name = parameters["name"]
        result.description = parameters["description"]
        result.markLinestart = parameters["markLinestart"]
        result.markLineend = parameters["markLineend"]
        result.markEOF = parameters["markEOF"]
        
        for key in Config.lexerConfig.keys():
            if Config.lexerConfig[key][self.configIndex] == 1:
                result.tokens.append(self.getLexerToken(self.lexerTokens[key]))

        result.tokens = sorted(result.tokens, key=attrgetter('order'))
        return result
    
    def getParserConfig(self):
        parameters = Config.parserParameters[self.configIndex]
        result = ParserConfig()
        result.name = parameters["name"]
        keys = Config.parserConfig.keys()
        for key in keys:
            if Config.parserConfig[key][self.configIndex] == 1:
                result.tokens.append(self.getParserToken(self.parserTokens[key]))

        result.tokens = sorted(result.tokens, key=attrgetter('bindingpower'))
        
        return result

    def getAstOptimizerConfig(self):
        result = AstOptimizerConfig()
        keys = Config.astOptimizerConfig.keys()
        for key in keys:
            if Config.astOptimizerConfig[key][self.configIndex] == 1:
                #print(key)
                result.handlers.append(self.astOptimizerConfigTokens[key])
        return result
