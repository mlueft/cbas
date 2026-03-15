import cbas.Config.Config
import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Parser.Parser
import cbas.Lexer.Lexer
import cbas.Ast.Expressions
import cbas.Ast.Statements

Lexer = cbas.Lexer.Lexer.Lexer
Parser = cbas.Parser.Parser.Parser
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenchainOptimizer
Config = cbas.Config.Config.Config

class Compiler():
    
    ##
    #
    #
    def __init__(self, configIndex=0):
        self.debug = True
        
        self.config = self._createConfig(configIndex)
        self.lexer = self._createLexer(configIndex)
        self.tokenChainOptimizer = self._createTokenChainOptimizer(configIndex)
        self.parser = self._createParser(configIndex)

    def _createConfig(self, configIndex):
        return Config(configIndex)
    
    def _createLexer(self, configIndex):
        result = Lexer()
        result.debug = self.debug
        return result
    
    def _createTokenChainOptimizer(self, configIndex):
        result = TokenChainOptimizer()
        result.debug = self.debug
        return result
    
    def _createParser(self, configIndex):
        result = Parser()
        result.debug = self.debug
        return result
    

    def log(self,msg,level="log"):
        if self.debug:
            print(msg)

    def __runLexer(self, inputFile):
        self.log("", "debug")
        self.log("lexer ...", "debug")
        self.log("============================================", "debug")
        self.lexer.config = self.config.getLexerConfig()
        self.lexer.tokenizeFile(inputFile)

    def __runChainOptimizer(self):
        self.log("", "debug")
        self.log("chainoptimizing ...", "debug")
        self.log("============================================", "debug")
        self.tokenChainOptimizer.main(self.lexer.firstToken)

    def __runParser(self):
        self.log("", "debug")
        self.log("parser ...", "debug")
        self.log("============================================", "debug")
        self.parser.config = self.config.getParserConfig()
        tokenList = self.lexer.getTokenList()
        return self.parser.parse(tokenList)

    def __runPostParsingOptimizer(self, ast):
        #
        # RunOptimizer 'POST_PARSER_TD'
        #
        self.log("", "debug")
        self.log("POST_PARSER_TD", "debug")
        self.log("============================================", "debug")
        conf = self.config.getAstOptimizerConfig()
        for o in conf.handlers:
            ast.topDown(o.main)


    def __debugLexerChainList(self,token):
        self.log("TOKENS:")
        while token:
            
            colWidth = 30
            _current = str(token)
            _prev = str(token.prev)
            _next = str(token.next)

            if len(_prev) > colWidth: _prev = _prev[:colWidth-3]+"..."
            if len(_current) > colWidth: _current = _current[:colWidth-3]+"..."
            if len(_next) > colWidth: _next = _next[:colWidth-3]+"..."
            formatstring = " * {:<"+str(colWidth)+"} <= {:<"+str(colWidth)+"} => {:<"+str(colWidth)+"}"
            self.log(
                formatstring.format(
                    _prev,
                    _current,
                    _next
                )
            )

            token=token.next

    def __debugTokenlist(self,tokens):
        if not self.debug:
            return
        self.log("TOKENS List:", "debug")
        for t in tokens:
            self.log("{}".format(t), "debug")

    def __debugAst(self, ast):
        if not self.debug:
            return
        
        self.log("", "debug")
        self.log("debug ...", "debug")
        self.log("============================================", "debug")
        ast.debug()

    #def callBack(self,node):
    #    self.log( "{}{}".format(node.id, node) , "debug")
    

    ##
    #
    #
    def compileExpression(self, expression):

        #
        # Run Lexer
        #
        self.log("", "debug")
        self.log("lexer ...", "debug")
        self.log("============================================", "debug")
        self.lexer.config = self.config.getLexerConfig()
        self.lexer.tokenizeLine(expression)

        self.__runChainOptimizer()

        self.__debugTokenlist( self.lexer.getTokenList() )

        ast = self.__runParser()

        self.__debugAst(ast)

        self.__runPostParsingOptimizer(ast)

        self.__debugAst(ast)

        return ast
    
    ##
    #
    #
    def compileFile(self, inputFile ):

        self.__runLexer(inputFile)

        self.__runChainOptimizer()

        self.__debugTokenlist( self.lexer.getTokenList() )

        ast = self.__runParser()
   
        self.__debugAst(ast)
        
        self.__runPostParsingOptimizer(ast)
        
        self.__debugAst(ast)

        return ast