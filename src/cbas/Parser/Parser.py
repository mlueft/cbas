import cbas.Parser.Lookups as LU
import cbas.Lexer.TokenTypes as TT
import cbas.Ast.Statements as STS

class Parser():

	def __init__(self):
		self.tokens = None
		self.pos	= 0
		self.errors = []
		self.config = None
		
		self.body = None
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
		self.body = []
		while self.hasTokens:
			self.log("=========================================")
			self.log("while hasToken ...")
			self.log("=========================================")
			self.body.append( STS.StatementParser.parseStatement(self) )
		
		self.log("end:parsing()")
		return STS.BlockStatement(self.body)

	def createLookupTables(self):
		LU.Lookups.reset()

		for i in self.config.tokens:

			handler = LU.Lookups.getHandler( i.type )
			category = i.category
			
			if category == "led":
				LU.Lookups.registerLed( i.type, i.bindingpower, handler )
			elif category == "nud":
				LU.Lookups.registerNud( i.type, handler )
			elif category == "statement":
				LU.Lookups.registerStatement( i.type, handler )
			else:
				raise ValueError("Category for '{}' not found!".format( cbas.Lexer.TokenTypes.getString(i.type) ))
		
	@property
	def currentToken(self):
		return self.tokens[self.pos]
	
	@property
	def currentTokenType(self):
		return self.tokens[self.pos].type

	@property
	def hasTokens(self):
		return self.pos < len(self.tokens) and self.currentTokenType != TT.TokenTypes.EOF
	
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
				raise ValueError("Expected {} but received {}!".format( tokenType, cbas.Lexer.TokenTypes.getString(type) ))
			
			raise ValueError( error )
		
		return self.advance()
	
