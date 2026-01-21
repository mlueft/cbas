import re

from cbas.Config.Config import Config
from cbas.TokenChainOptimizer import TokenchainOptimizer
from cbas.Parser import Parser
#from cbas.Config.ConfigLoader import ConfigLoader
from cbas.Lexer.Lexer import Lexer


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
	conf = Config()

	#
 	# Run Lexer
	#
	lexer = Lexer(configIndex,contextFile)
	lexer.config = conf.getLexerConfig(configIndex)
	lexer._verbose = True
	lex = lexer.lex(inputFile)

	#debugLexerChainList(lexer.firstToken)

	#
	# Run Chain optimizers
	#
	optimizer = TokenchainOptimizer()
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


def main():
	configFile  = "/home/work/programming/cbas/config/config.json"
	inputFile   = "/home/work/programming/cbas/examples/main1.bas"

	compile( inputFile, configFile, 0 )

main()