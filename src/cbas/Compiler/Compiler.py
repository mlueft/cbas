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
    def __init__(self):
        self.debug = False
    
    def log(msg,level=0):
        print(msg)
    ##
    #
    #
    def debugLexerChainList(self,token):
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

    ##
    #
    #
    def debugTokenlist(self,tokens):
        self.log("TOKENS List:")
        for t in tokens:
            self.log("{}".format(t))

    ##
    #
    #
    def compileExpression(self, expression, configIndex):

        #
        # Load config
        #
        #conf = ConfigLoader(contextFile)
        if self.debug:
            self.log("")
            self.log("config ...")
            self.log("============================================")
        conf = Config()


        #
        # Run Lexer
        #
        if self.debug:
            self.log("")
            self.log("lexer ...")
            self.log("============================================")
        lexer = Lexer()
        lexer.config = conf.getLexerConfig(configIndex)
        lexer._verbose = True
        lexer.tokenizeLine(expression)


        #
        # Run Chain optimizers
        #
        if self.debug:
            self.log("")
            self.log("chainoptimizing ...")
            self.log("============================================")
        optimizer = TokenChainOptimizer()
        optimizer.main(lexer.firstToken)


        if self.debug:
            self.debugTokenlist( lexer.getTokenList() )


        #
        # Run Parser
        #
        if self.debug:
            self.log("")
            self.log("parser ...")
            self.log("============================================")
        parser = Parser()
        config = conf.getParserConfig(configIndex)
        parser.config = config
        tokenList = lexer.getTokenList()
        ast = parser.parse(tokenList)


        #
        # DEBUG
        #
        if self.debug:
            self.log("")
            self.log("debug ...")
            self.log("============================================")
            ast.debug()

        if False:
            #
            # OUTLINE
            #
            self.log("")
            self.log("OUTLINE")
            self.log("============================================")
            ast.outline(self.callBack)

            #
            # BOTTOMUP
            #
            self.log("")
            self.log("BOTTOMUP")
            self.log("============================================")
            ast.bottomUp(self.callBack)

            #
            # TOPDOWN
            #
            self.log("")
            self.log("TOPDOWN")
            self.log("============================================")
            ast.topDown(self.callBack)


        #
        # RunOptimizer 'POST_PARSER_TD'
        #
        if self.debug:
            self.log("")
            self.log("POST_PARSER_TD")
            self.log("============================================")
        conf = conf.getAstOptimizerConfig(configIndex)
        for o in conf.handlers:
            ast.topDown(o.main)

        #
        # DEBUG
        #
        if self.debug:
            self.log("")
            self.log("debug ...")
            self.log("============================================")
            ast.debug()


        #
        # RunOptimizer 'POST_PARSER_BU'
        #
        if self.debug:
            self.log("")
            self.log("POST_PARSER_BU")
            self.log("============================================")
        #conf = conf.getAstOptimizerConfig(configIndex)
        for o in conf.handlers:
            ast.bottomUp(o.main)

        #
        # DEBUG
        #
        if self.debug:        
            self.log("")
            self.log("debug ...")
            self.log("============================================")
            ast.debug()

        return ast
    
    def callBack(self,node):
        
        self.log( "{}{}".format(node.id, node) )
        return
    
    ##
    #
    #
    def compileFile(self, inputFile, configIndex ):
        
        #
        # Load config
        #
        #conf = ConfigLoader(contextFile)
        conf = Config()

        #
        # Run Lexer
        #
        lexer = Lexer()
        lexer.config = conf.getLexerConfig(configIndex)
        lexer._verbose = True
        lex = lexer.tokenize(inputFile)

        #debugLexerChainList(lexer.firstToken)

        #
        # Run Chain optimizers
        #
        optimizer = TokenChainOptimizer()
        lex = optimizer.optimize(lexer.firstToken)

        self.debugTokenlist( lexer.getTokenList() )

        #
        # Run Parser
        #
        parser = Parser()
        parser.config = conf.getParserConfig(configIndex)
        tokenList = lexer.getTokenList()
        ast = parser.parse(tokenList)

        ast.debug()


