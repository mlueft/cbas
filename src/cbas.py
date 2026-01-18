import re

from cbas.TokenChainOptimizer import TokenchainOptimizer
from cbas.Parser import Parser
from cbas.Config.ConfigLoader import ConfigLoader
from cbas.Lexer.Lexer import Lexer

def compile(inputFile, contextFile, configName):

	#
	# Load config
	#
	cl = ConfigLoader(contextFile)

	#
 	# Run Lexer
	#
	lexer = Lexer(configName,contextFile)
	lexer.config = cl.getLexerConfig(configName)
	lexer._verbose = True
	lex = lexer.lex(inputFile)

	#
	# Run Chain optimizers
	#
	optimizer = TokenchainOptimizer()
	lex = optimizer.optimize(lexer.firstToken)
	
	#
	# Run Parser
	#
	parser = Parser.Parser()
	parser.config = cl.getParserConfig(configName)
	ast = parser.parse(lexer.getTokenList())
	

	if False:
		print("TOKENS List:")
		tokens = lexer.getTokenList()
		for t in tokens:
			print("{}".format(t))

	if False:
		print("TOKENS:")
		token = lexer.firstToken
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

	if True:
		ast.debug()


def main():
	configFile  = "/home/work/programming/cbas/config/config.json"
	inputFile    = "/home/work/programming/cbas/examples/main.bas"
	#inputFile    = "/home/work/programming/cbas/examples/main1.bas"
	configName   = "COMMODORE_BASIC_V2"
	#contextName = "TEST"

	compile( inputFile, configFile, configName )

main()