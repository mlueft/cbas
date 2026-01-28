import cbas.Config.Config
import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Parser.Parser
import cbas.Lexer.Lexer

Lexer = cbas.Lexer.Lexer.Lexer
Parser = cbas.Parser.Parser.Parser
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenchainOptimizer
Config = cbas.Config.Config.Config

class Compiler():
    
    ##
    #
    #
    def __init__(self):
        pass
    
    ##
    #
    #
    def debugLexerChainList(self,token):
        print("TOKENS:")
        while token:
            
            colWidth = 30
            _current = str(token)
            _prev = str(token.prev)
            _next = str(token.next)

            if len(_prev) > colWidth: _prev = _prev[:colWidth-3]+"..."
            if len(_current) > colWidth: _current = _current[:colWidth-3]+"..."
            if len(_next) > colWidth: _next = _next[:colWidth-3]+"..."
            formatstring = " * {:<"+str(colWidth)+"} <= {:<"+str(colWidth)+"} => {:<"+str(colWidth)+"}"
            print(
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
        print("TOKENS List:")
        for t in tokens:
            print("{}".format(t))

    ##
    #
    #
    def compileLine(self, line, configIndex):

        print("config ...")
        #
        # Load config
        #
        #conf = ConfigLoader(contextFile)
        conf = Config()

        print("lexer ...")
        #
        # Run Lexer
        #
        lexer = Lexer()
        lexer.config = conf.getLexerConfig(configIndex)
        lexer._verbose = True
        lex = lexer.tokenizeLine(line)

        print("chainoptimizing ...")
        #
        # Run Chain optimizers
        #
        optimizer = TokenChainOptimizer()
        lex = optimizer.optimize(lexer.firstToken)

        self.debugTokenlist( lexer.getTokenList() )

        print("parser ...")
        #
        # Run Parser
        #
        parser = Parser()
        parser.config = conf.getParserConfig(configIndex)
        tokenList = lexer.getTokenList()
        ast = parser.parse(tokenList)

        print("debug ...")
        #
        # RunOptimizer 'POST_PARSER'
        #

        print(ast)
        ast.debug()
    
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