import cbas
import cbas.Parser.Lookups
import cbas.Lexer.TokenTypes
import cbas.Ast.Statements

StatementParser = cbas.Ast.Statements.StatementParser
BlockStatement = cbas.Ast.Statements.BlockStatement
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
Lookups = cbas.Parser.Lookups.Lookups

class Parser():

	def __init__(self):
		self.tokens = None
		self.pos	= 0
		self.errors = []
		self.config = None
		
		self.__first = None
		self.indentation = 0
		
	def parse(self, tokens):
		cbas.log("start:parsing()", "debug")

		if self.config is None:
			raise ValueError("Parser context not set!")
		
		self.createLookupTables()
		self.tokens = tokens
		self.__first = None
		statements = []
		while self.hasTokens:
			cbas.log("=========================================", "debug")
			cbas.log("while hasToken ...", "debug")
			cbas.log("=========================================", "debug")
			statements.append( StatementParser.parseStatement(self) )
		
		cbas.log("end:parsing()", "debug")
		return BlockStatement(statements)

	def createLookupTables(self):
		Lookups.reset()

		for token in self.config.tokens:
			#print( "register: {} {} {}".format(i.type,category,handler) )
			if token.category == "led":
				Lookups.registerLed( token.type, token.bindingpower, token.handler )
			elif token.category == "nud":
				Lookups.registerNud( token.type, token.handler )
			elif token.category == "statement":
				Lookups.registerStatement( token.type, token.handler )
			else:
				raise ValueError("Category for '{}' not found!".format( TokenTypes.toString(token.type) ))
		
	@property
	def currentToken(self):
		return self.tokens[self.pos]
	
	@property
	def currentTokenType(self):
		return self.tokens[self.pos].type

	@property
	def lastTokenType(self):
		return self.tokens[self.pos-1].type

	@property
	def hasTokens(self):
		return self.pos < len(self.tokens) and self.currentTokenType != TokenTypes.EOF #and self.currentTokenType != TokenTypes.LINEEND
	
	def advance(self):
		tk = self.currentToken
		#if self.pos < len(self.tokens)-1:
		self.pos += 1
		return tk
	
	def expect(self, tokenType):
		return self.expectError( tokenType )
	
	def expectError(self, tokenType, error=None):
		token = self.currentToken
		type = token.type

		if type != tokenType:
			if error == None:
				raise ValueError("Expected {} but received {}!".format( TokenTypes.toString(tokenType), TokenTypes.toString(type) ))
			
			raise ValueError( error )
		
		return self.advance()
	

