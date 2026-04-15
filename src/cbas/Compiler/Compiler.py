import os

import cbas
import cbas.Config.Config
import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Parser.Parser
import cbas.Lexer.Lexer
import cbas.Ast.Expressions
import cbas.Ast.Statements
import cbas.DataStructures.TraverseMode
import cbas.Compiler.CompilerPasses
import cbas.CodeBuilder.BasicBuilder
import cbas.Linker.Linker

Lexer = cbas.Lexer.Lexer.Lexer
Parser = cbas.Parser.Parser.Parser
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenChainOptimizer
Config = cbas.Config.Config.Config
TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
CompilerPasses = cbas.Compiler.CompilerPasses.CompilerPasses
BasicBuilder = cbas.CodeBuilder.BasicBuilder.BasicBuilder
Linker = cbas.Linker.Linker.Linker

class Compiler():
    
    ##
    #
    #
    def __init__(self, configIndex=0):
        
        self.config = self._createConfig(configIndex)
        self.lexer  = self._createLexer(configIndex)
        self.parser = self._createParser(configIndex)
        self.basicBuilder = self._createBasicBuilder(configIndex)
        self.linker = self._createLinker(configIndex)
        self.objectFolder = None
        self.binFolder = None

        self.basicLines = []

    def _createConfig(self, configIndex):
        return Config(configIndex)
    
    def _createLexer(self, configIndex):
        result = Lexer()
        return result
    
    def _createParser(self, configIndex):
        result = Parser()
        return result
   
    def _createBasicBuilder(self, configIndex):
        result = BasicBuilder()
        return result

    def _createLinker(self, configIndex):
        result = Linker()
        return result
    
    def __runLexer(self, inputFile):
        cbas.log("", "debug")
        cbas.log("lexer ...", "debug")
        cbas.log("============================================", "debug")
        self.lexer.config = self.config.getLexerConfig()
        self.lexer.tokenizeFile(inputFile)

    def __runTokenChainOptimizer(self, lex):
        cbas.log("", "debug")
        cbas.log("chainoptimizing ...", "debug")
        cbas.log("============================================", "debug")
        config = self.config.getTokenChainOptimizerConfig()
        for o in config.passes:
            o["instance"].main(lex)

    def __runParser(self,tokenList):
        cbas.log("", "debug")
        cbas.log("parser ...", "debug")
        cbas.log("============================================", "debug")
        self.parser.config = self.config.getParserConfig()
        return self.parser.parse(tokenList)

    def __runAstOptimizer(self, ast, compilerPass):

        cbas.log("ast optimizer ...".format(), "debug")
        conf = self.config.getAstOptimizerConfig(compilerPass)
        for o in conf.handlers:
            print( TraverseMode.toString(o[1]), o[0])
            if o[1] == TraverseMode.TOP_DOWN:
                ast.topDown(o[0].main)
            elif o[1] == TraverseMode.BOTTOM_UP:
                ast.bottomUp(o[0].main)
            elif o[1] == TraverseMode.OUTLINE:
                ast.outline(o[0].main)

        return ast

    def __runBasicBuilder(self,ast):
        cbas.log("BasicBuilder ...".format(), "debug")
        return self.basicBuilder.main(ast)

    def __runLinker(self,lines):
        return self.linker.main(lines)

    def __debugAst(self, ast):

        cbas.log("", "debug")
        cbas.log("debug ...", "debug")
        cbas.log("============================================", "debug")
        ast.debug()

    def _toBasic(self):
        self.basicLines = []
        #ast = self.ast
        #ast.topDown(self.__callBackBasic)
        return self.basicLines
    
    def __callBackBasic(self,node,traverseMode):
        if node.isLeaf:
            return
        lines = node.toBasic()
        if lines is not None:
            for l in lines:
                self.basicLines.append(l)

    def writeLines(self, lines, file):
        try:
            os.remove(file)
        except FileNotFoundError as e:
            pass

        with open(file, 'w') as f:
            for line in lines:
                f.write("{}\n".format(line))

    ##
    #
    #
    def compileExpression(self, expression):

        #
        # Run Lexer
        #
        cbas.log("", "debug")
        cbas.log("lexer ...", "debug")
        cbas.log("============================================", "debug")
        self.lexer.config = self.config.getLexerConfig()
        self.lexer.tokenizeLine(expression)
        
        self.__runTokenChainOptimizer(self.lexer.firstToken)

        tokenList = self.lexer.getTokenList()

        ast = self.__runParser(tokenList)

        # SemanticCheck
        ast = self.__runAstOptimizer(ast,CompilerPasses.CHECK_SEMANTIC)

        # Optimizer
        ast = self.__runAstOptimizer(ast,CompilerPasses.POST_PARSER)

        self.__debugAst(ast)

        return ast
    
    ##
    #
    #
    def compileFile(self, inputFile ):

        self.__runLexer(inputFile)

        self.__runTokenChainOptimizer(self.lexer.firstToken)

        tokenList = self.lexer.getTokenList()

        ast = self.__runParser(tokenList)
   
        # DEBUG
        self.__debugAst(ast)

        # SemanticCheck
        ast = self.__runAstOptimizer(ast,CompilerPasses.CHECK_SEMANTIC)

        # Optimizer
        ast = self.__runAstOptimizer(ast,CompilerPasses.POST_PARSER)
        
        # DEBUG
        self.__debugAst(ast)

        # BASICBUILDER
        lines = self.__runBasicBuilder(ast)

        # Linker
        lines = self.__runLinker(lines)



        if os.path.isdir( self.objectFolder ):
            basicFile = os.path.join( self.objectFolder, os.path.basename(inputFile) )+".basic"
            self.writeLines(lines, basicFile)

        if os.path.isdir( self.binFolder ):
            basicFile = os.path.join( self.binFolder, os.path.basename(inputFile) )
            self.writeLines(lines, basicFile)


        cbas.symbolTable.debug()
        
        return ast