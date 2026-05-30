import os
import struct

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
        
        self.objectFolder = None
        self.binFolder = None
        self.lineNumberStart = 1
        self.lineNumberStep = 1
        self.beautify = False
        self.basicStartAddress = 2048
        self.basicLines = []

        self.__config = self._createConfig(configIndex)
        self.__lexer  = self._createLexer(configIndex)
        self.__parser = self._createParser(configIndex)
        self.__codeBuilder = self._createBasicBuilder(configIndex)
        self.__linker = self._createLinker()

    def _createConfig(self, configIndex):
        result = Config(configIndex)
        return result
    
    def _createLexer(self, configIndex):
        result = Lexer()
        return result
    
    def _createParser(self, configIndex):
        result = Parser()
        return result
   
    def _createBasicBuilder(self, configIndex):
        result = BasicBuilder(configIndex,self.beautify)
        return result

    def _createLinker(self, prg=True):
        result = Linker(prg)
        result.lineNumberStart = self.lineNumberStart
        result.lineNumberStep = self.lineNumberStep
        result.basicStartAddress = self.basicStartAddress
        return result
    

    def __runLexer(self, inputFile):
        cbas.log("", "debug")
        cbas.log("lexer ...", "debug")
        cbas.log("============================================", "debug")
        self.__lexer.config = self.__config.getLexerConfig()
        self.__lexer.tokenizeFile(inputFile)

    def __runTokenChainOptimizer(self, lex):
        cbas.log("", "debug")
        cbas.log("chainoptimizing ...", "debug")
        cbas.log("============================================", "debug")
        config = self.__config.getTokenChainOptimizerConfig()
        for o in config.passes:
            o["instance"].main(lex)

    def __runParser(self,tokenList):
        cbas.log("", "debug")
        cbas.log("parser ...", "debug")
        cbas.log("============================================", "debug")
        self.__parser.config = self.__config.getParserConfig()
        return self.__parser.parse(tokenList)

    def __runAstOptimizer(self, ast, compilerPass):

        cbas.log("ast optimizer ...".format(), "debug")
        conf = self.__config.getAstOptimizerConfig(compilerPass)
        for o in conf.handlers:
            #print( TraverseMode.toString(o[1]), o[0])
            if o[1] == TraverseMode.TOP_DOWN:
                ast.topDown(o[0].main)
            elif o[1] == TraverseMode.BOTTOM_UP:
                ast.bottomUp(o[0].main)
            elif o[1] == TraverseMode.OUTLINE:
                ast.outline(o[0].main)

        return ast

    def __runCodeBuilder(self,ast):
        cbas.log("CodeBuilder ...".format(), "debug")
        self.__resetAst(ast)
        return self.__codeBuilder.main(ast)

    def __runLinker(self,lines):
        return self.__linker.main(lines)


    def __debugAst(self, ast):

        cbas.log("", "debug")
        cbas.log("debug ...", "debug")
        cbas.log("============================================", "debug")
        ast.debug()

    def __callBackBasic(self,node,traverseMode):
        if node.isLeaf:
            return
        lines = node.toBasic()
        if lines is not None:
            for l in lines:
                self.basicLines.append(l)

    def __writeLines(self, lines, file):
        try:
            os.remove(file)
        except FileNotFoundError as e:
            pass

        with open(file, 'wb') as f:
            for line in lines:
                b1 = bytes(line)
                #for b in line:
                #b1 = (b).to_bytes(1, byteorder='big', signed=False)
                #b1 = struct.pack("{}b".format(len(line)), *line)
                f.write(b1)

    def __resetAst(self,ast):
        ast.topDown(self.__astResetHandler)

    def __astResetHandler(self, node, traverseMode):
        node._basicGenerated = False

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
        self.__lexer.config = self.__config.getLexerConfig()
        self.__lexer.tokenizeLine(expression)
        
        self.__runTokenChainOptimizer(self.__lexer.firstToken)

        tokenList = self.__lexer.getTokenList()

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

        #
        # Generalize files
        #
        # 1. : is replaced by a linebreak
        # 2. _ at the end of a line, contatenates the current and the next line.
        # 3. Comments are removed.
        

        #
        # LEXER
        #
        self.__runLexer(inputFile)

        #
        # TokenchainOptimizer
        #
        self.__runTokenChainOptimizer(self.__lexer.firstToken)

        tokenList = self.__lexer.getTokenList()

        #
        # PARSER
        #
        ast = self.__runParser(tokenList)
   
        # DEBUG
        self.__debugAst(ast)

        #
        # ASTOPTIMIZER
        #
        # SemanticCheck
        ast = self.__runAstOptimizer(ast,CompilerPasses.CHECK_SEMANTIC)

        # Optimizer
        ast = self.__runAstOptimizer(ast,CompilerPasses.POST_PARSER)
        
        # DEBUG
        self.__debugAst(ast)


        #
        # CODEBUILDER
        #
        codeLines = None
        if True:
            self.__codeBuilder = self._createBasicBuilder(BasicBuilder.PRG)
            self.__linker=self._createLinker(True)
            codeLines = self.__runCodeBuilder(ast)
            codeLines = self.__runLinker(codeLines)

        #
        # BASICBUILDER
        #
        basicLines = None
        if True:
            self.__codeBuilder = self._createBasicBuilder(BasicBuilder.BASIC)
            self.__linker=self._createLinker(False)
            basicLines = self.__runCodeBuilder(ast)
            basicLines = self.__runLinker(basicLines)



        if basicLines is not None:
            if os.path.isdir( self.objectFolder ):
                basicFile = os.path.join( self.binFolder, os.path.basename(inputFile) )+".basic"
                self.__writeLines(basicLines, basicFile)


        if codeLines is not None:
            if os.path.isdir( self.binFolder ):
                basicFile = os.path.join( self.binFolder, os.path.basename(inputFile)+".prg" )
                self.__writeLines(codeLines, basicFile)


        cbas.symbolTable.debug()
        
        return ast