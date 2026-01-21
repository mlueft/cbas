import re

import cbas.Config.Config as Config
import cbas.TokenChainOptimizer.TokenChainOptimizer as TO
import cbas.Parser.Parser as P
#from cbas.Config.ConfigLoader import ConfigLoader
import cbas.Lexer.Lexer as L


def debugLexerChainList(token):
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

def debugTokenlist(tokens):
	print("TOKENS List:")
	for t in tokens:
		print("{}".format(t))
		
def compile(inputFile, contextFile, configIndex):

	#
	# Load config
	#
	#conf = ConfigLoader(contextFile)
	conf = Config.Config()

	#
 	# Run Lexer
	#
	lexer = L.Lexer(configIndex,contextFile)
	lexer.config = conf.getLexerConfig(configIndex)
	lexer._verbose = True
	lex = lexer.lex(inputFile)

	#debugLexerChainList(lexer.firstToken)

	#
	# Run Chain optimizers
	#
	optimizer = TO.TokenchainOptimizer()
	lex = optimizer.optimize(lexer.firstToken)

	debugTokenlist( lexer.getTokenList() )

	#
	# Run Parser
	#
	parser = P.Parser()
	parser.config = conf.getParserConfig(configIndex)
	tokenList = lexer.getTokenList()
	ast = parser.parse(tokenList)

	ast.debug()


def main():
	configFile  = "/home/work/cbas/config/config.json"
	inputFile   = "/home/work/cbas/examples/main1.bas"

	compile( inputFile, configFile, 0 )

main()