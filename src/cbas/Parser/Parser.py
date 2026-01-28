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
		
	def log(self,message, type="log"):
		
		if message.lower()[0:4] == "end:":
			self.indentation -= 4
			
		print( (" "*self.indentation)+message )
		
		if message.lower()[0:6] == "start:":
			self.indentation += 4

	def parse(self, tokens):
		self.log("start:parsing()")

		if self.config is None:
			raise ValueError("Parser context not set!")
		
		self.createLookupTables()
		self.tokens = tokens
		self.__first = None
		while self.hasTokens:
			self.log("=========================================")
			self.log("while hasToken ...")
			self.log("=========================================")
			if self.__first == None:
				self.__first = StatementParser.parseStatement(self)
			else:
				self.__first.last.insertAfter( StatementParser.parseStatement(self) )
		
		self.log("end:parsing()")
		return BlockStatement(self.__first)

	def createLookupTables(self):
		Lookups.reset()

		for i in self.config.tokens:

			handler = Lookups.getHandler( i.type )
			category = i.category
			
			if category == "led":
				Lookups.registerLed( i.type, i.bindingpower, handler )
			elif category == "nud":
				Lookups.registerNud( i.type, handler )
			elif category == "statement":
				Lookups.registerStatement( i.type, handler )
			else:
				raise ValueError("Category for '{}' not found!".format( TokenTypes.getString(i.type) ))
		
	@property
	def currentToken(self):
		return self.tokens[self.pos]
	
	@property
	def currentTokenType(self):
		return self.tokens[self.pos].type


	@property
	def hasTokens(self):
		return self.pos < len(self.tokens) and self.currentTokenType != TokenTypes.EOF
	
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
				raise ValueError("Expected {} but received {}!".format( tokenType, TokenTypes.getString(type) ))
			
			raise ValueError( error )
		
		return self.advance()
	
