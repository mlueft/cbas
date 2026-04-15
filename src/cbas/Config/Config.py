from operator import attrgetter

import cbas.Config.LexerConfig
import cbas.Config.TokenChainOptimizerConfig
import cbas.Config.ParserConfig
import cbas.Config.AstOptimizerConfig

import cbas.Lexer.TokenTypes
import cbas.Lexer.ConfigToken

import cbas.Parser.BindingPower
import cbas.Parser.ConfigToken

import cbas.Ast.Expressions
import cbas.Ast.Statements

#import cbas.AstOptimizer.AstOptimizer
import cbas.AstOptimizer.ConfigToken
import cbas.DataStructures.TraverseMode

import cbas.Config.LexerMatrix
import cbas.Config.ParserMatrix
import cbas.Config.AstOptimizerMatrix
import cbas.Compiler.CompilerPasses

TokenTypes                = cbas.Lexer.TokenTypes.TokenTypes
BindingPower              = cbas.Parser.BindingPower.BindingPower
LexerConfigToken          = cbas.Lexer.ConfigToken.ConfigToken
LexerConfig               = cbas.Config.LexerConfig.LexerConfig
TokenChainOptimizerConfig = cbas.Config.TokenChainOptimizerConfig.TokenChainOptimizerConfig
ParserConfigToken         = cbas.Parser.ConfigToken.ConfigToken
ParserConfig              = cbas.Config.ParserConfig.ParserConfig
ExpressionParser          = cbas.Ast.Expressions.ExpressionParser
StatementParser           = cbas.Ast.Statements.StatementParser
#ArithmeticOptimizer       = cbas.AstOptimizer.AstOptimizer.ArithmeticOptimizer
#LogicOptimizer            = cbas.AstOptimizer.AstOptimizer.LogicOptimizer
AstOptimizerConfig        = cbas.Config.AstOptimizerConfig.AstOptimizerConfig
AstOptimizerToken         = cbas.AstOptimizer.ConfigToken.ConfigToken
#SyntaxCheckerV2           = cbas.AstOptimizer.AstOptimizer.SyntaxCheckerV2
TraverseMode              = cbas.DataStructures.TraverseMode.TraverseMode
CompilerPasses            = cbas.Compiler.CompilerPasses.CompilerPasses

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

    def __init__(self, configIndex):
        self.configIndex = configIndex

        pass

    def getLexerConfig(self):
        parameters = cbas.Config.LexerMatrix.LexerMatrix.Parameters[self.configIndex]
        result = LexerConfig()
        result.name = parameters["name"]
        result.description = parameters["description"]
        result.markLinestart = parameters["markLinestart"]
        result.markLineend = parameters["markLineend"]
        result.markEOF = parameters["markEOF"]
        
        for key in cbas.Config.LexerMatrix.LexerMatrix.Matrix.keys():
            if cbas.Config.LexerMatrix.LexerMatrix.Matrix[key][self.configIndex] == 1:
                token = cbas.Config.LexerMatrix.LexerMatrix.Tokens[key]
                result.tokens.append(
                    LexerConfigToken(
                        token["type"],
                        token["expression"],
                        token["order"],
                        token["handler"]
                    )
                )

        result.tokens = sorted(result.tokens, key=attrgetter('order'))
        return result
    
    def getTokenChainOptimizerConfig(self):
        result = TokenChainOptimizerConfig()

        return result

    def getParserConfig(self):
        parameters = cbas.Config.ParserMatrix.ParserMatrix.Parameters[self.configIndex]
        result = ParserConfig()
        result.name = parameters["name"]
        result.functions = cbas.Config.ParserMatrix.ParserMatrix.Functions
        result.statements = cbas.Config.ParserMatrix.ParserMatrix.Statements
        keys = cbas.Config.ParserMatrix.ParserMatrix.Matrix.keys()
        for key in keys:
            if cbas.Config.ParserMatrix.ParserMatrix.Matrix[key][self.configIndex] == 1:
                token = cbas.Config.ParserMatrix.ParserMatrix.Tokens[key]
                result.tokens.append(
                    ParserConfigToken(
                        token["bindingpower"],
                        token["type"],
                        token["category"],
                        token["handler"],
                    )
                )

        result.tokens = sorted(result.tokens, key=attrgetter('bindingpower'))
        
        return result

    def getAstOptimizerConfig(self,compilerPass):
        result = AstOptimizerConfig()

        parameters = cbas.Config.AstOptimizerMatrix.AstOptimizerMatrix.Parameters[self.configIndex]
        result.name = parameters["name"]
        result.description = parameters["description"]
    
        if compilerPass == CompilerPasses.CHECK_SEMANTIC:
            matrix = cbas.Config.AstOptimizerMatrix.AstOptimizerMatrix.Matrixsemanticcheck
            tokens = cbas.Config.AstOptimizerMatrix.AstOptimizerMatrix.TokensSemanticcheck

        elif compilerPass == CompilerPasses.POST_PARSER:
            matrix = cbas.Config.AstOptimizerMatrix.AstOptimizerMatrix.MatrixPostParser
            tokens = cbas.Config.AstOptimizerMatrix.AstOptimizerMatrix.TokensPostParser

        keys = tokens.keys()
        for key in keys:
            if matrix[key][self.configIndex] == 1:
                #print(key)
                result.handlers.append(
                    [tokens[key]["instance"],tokens[key]["direction"]]
                )
        
        return result
