import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

##
#
#
class ListToken():

	def __init__(self,code="",line=0,pos=0,type=None):
		self.line = line
		self.pos  = pos
		self.code = code
		self.type = type

	def __str__(self):
		return "{}:{} - '{}' '{}'".format( self.line, self.pos, self.code, TokenTypes.getString(self.type) )

	def __repr__(self):
		if self.isString:
			return "'{}'".format(self.code)
		else:
			return "{}".format(self.code)

##
#
#
class ChainToken(ListToken):

	def __init__(self,code="",line=0,pos=0,type=None):
		super().__init__(code,line,pos,type)
		self.next = None
		self.prev = None
		
	def insertAfter(self, token):
		
		token.prev = self
		token.next = self.next
		
		if self.next != None:
			self.next.pref = token
		
		self.next = token
		
		return token
	
	def insertBefore(self, token):
		token.prev = self.prev
		token.next = self

		if self.prev != None:
			self.pref.next = token
		
		self.prev = token
		
		return self
	
	# TODO: Bug: We can't remove the first linestart
	#       because lexers first node reverences it!
	def remove(self):

		if self.prev != None:
			self.prev.next = self.next

		if self.next != None:
			self.next.prev = self.prev

		# Don't remove these settinge
		# Otherwise traversing the chain
		# doesn't work!
		#self.prev = None
		#self.next = None

	def generateListToken(self):
		result      = ListToken()
		result.line = self.line
		result.pos  = self.pos
		result.code = self.code
		result.type = self.type
		return result
	