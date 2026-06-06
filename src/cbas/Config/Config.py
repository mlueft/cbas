from operator import attrgetter

import cbas.Config.TokenChainOptimizerConfig

import cbas.Lexer.TokenTypes
import cbas.Lexer.ConfigToken

import cbas.Parser.BindingPower
import cbas.Parser.ConfigToken

import cbas.Ast.Expressions
import cbas.Ast.Statements

#import cbas.AstOptimizer.AstOptimizer
import cbas.AstOptimizer.ConfigToken
import cbas.DataStructures.TraverseMode

import cbas.Config.LexerConfig
import cbas.Config.ParserConfig
import cbas.Config.AstOptimizerConfig
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
        parameters = cbas.Config.LexerConfig.Matrix.Parameters[self.configIndex]
        result = LexerConfig()
        result.name = parameters["name"]
        result.description = parameters["description"]
        result.markLinestart = parameters["markLinestart"]
        result.markLineend = parameters["markLineend"]
        result.markEOF = parameters["markEOF"]
        
        definitions = cbas.Config.LexerConfig.Matrix.Definitions
        matrix = cbas.Config.LexerConfig.Matrix.Matrix

        for key in matrix.keys():
            if matrix[key][self.configIndex] == 1:
                
                token = definitions[key]
                
                if token["type"] == "alias":
                    target = token["target"]
                    tokenTmp = definitions[target]
                    if "expression" in token:
                        tokenTmp["expression"] = token["expression"]
                    if "order" in token:
                        tokenTmp["order"] = token["order"]
                    token = tokenTmp

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

        definitions = cbas.Config.TokenChainOptimizerConfig.Matrix.Definitions
        matrix = cbas.Config.TokenChainOptimizerConfig.Matrix.Matrix

        keys = definitions.keys()
        for key in keys:
            if matrix[key][self.configIndex] == 1:
                token = definitions[key]
                result.tokens.append( token )
        
        return result

    def getParserConfig(self):
        parameters = cbas.Config.ParserConfig.Matrix.Parameters[self.configIndex]
        result = ParserConfig()
        result.name = parameters["name"]
        result.functions = cbas.Config.ParserConfig.Matrix.Functions
        result.statements = cbas.Config.ParserConfig.Matrix.Statements
        
        matrix = cbas.Config.ParserConfig.Matrix.Matrix
        definitions = cbas.Config.ParserConfig.Matrix.Definitions

        keys = matrix.keys()
        for key in keys:
            if matrix[key][self.configIndex] == 1:
                token = definitions[key]
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

        parameters = cbas.Config.AstOptimizerConfig.Matrix.Parameters[self.configIndex]
        result.name = parameters["name"]
        result.description = parameters["description"]
    
        definitions = cbas.Config.AstOptimizerConfig.Matrix.Definitions

        if compilerPass == CompilerPasses.CHECK_SEMANTIC:
            matrix = cbas.Config.AstOptimizerConfig.Matrix.Matrixsemanticcheck
        elif compilerPass == CompilerPasses.POST_PARSER:
            matrix = cbas.Config.AstOptimizerConfig.Matrix.MatrixPostParser

        keys = definitions.keys()
        for key in keys:
            if key in matrix and matrix[key][self.configIndex] == 1:
                #print(key)
                result.handlers.append(
                    [definitions[key]["instance"],definitions[key]["direction"]]
                )
        
        return result
