import cbas.Config.Config
import cbas.TokenChainOptimizer.TokenChainOptimizer
import cbas.Parser.Parser
#from cbas.Config.ConfigLoader import ConfigLoader
import cbas.Lexer.Lexer

Lexer = cbas.Lexer.Lexer.Lexer
Parser = cbas.Parser.Parser.Parser
TokenChainOptimizer = cbas.TokenChainOptimizer.TokenChainOptimizer.TokenchainOptimizer
Config = cbas.Config.Config.Config

class Compiler():
    
    def __init__(self):
        pass
    
    def compile(self):
        
        #
        # Load config
        #
        #conf = ConfigLoader(contextFile)
        conf = Config()

        #
        # Run Lexer
        #
        lexer = Lexer(configIndex,contextFile)
        lexer.config = conf.getLexerConfig(configIndex)
        lexer._verbose = True
        lex = lexer.tokenize(inputFile)

        #debugLexerChainList(lexer.firstToken)

        #
        # Run Chain optimizers
        #
        optimizer = TokenChainOptimizer()
        lex = optimizer.optimize(lexer.firstToken)

        debugTokenlist( lexer.getTokenList() )

        #
        # Run Parser
        #
        parser = Parser()
        parser.config = conf.getParserConfig(configIndex)
        tokenList = lexer.getTokenList()
        ast = parser.parse(tokenList)

        ast.debug()