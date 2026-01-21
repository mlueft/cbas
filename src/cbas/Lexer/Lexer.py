import re

import cbas.Lexer.Tokens as Tokens
import cbas.Lexer.TokenTypes as TokenTypes

class Lexer():

	def __init__(self, contextName, contextFile):
		self.currentToken    = None
		self.firstToken      = None
		self.__line          = 0
		self.pos             = 0
		self.__markLinestart = False
		self.__markLineend   = False
		self.config          = None
		self._verbose        = False
		self._handlerList    = self.createHandlerList()

	##
	#
	#
	def createUniqueToken(self,type=0, pos=0):
		return Tokens.ChainToken("",self.__line+1,self.pos+1,type)
	
	##
	#
	#
	def createToken(self,match,expression):
		return Tokens.ChainToken(match[0],self.__line+1,self.pos+1,expression.type)

	##
	#
	#
	def createHandlerList(self):
		return {
			TokenTypes.INTEGER     :self.__defaultHandler,
			TokenTypes.FLOAT       :self.__defaultHandler,
			TokenTypes.SIENTIFIC   :self.__defaultHandler,
			TokenTypes.LINENUMBER  :self.__defaultHandler,
			TokenTypes.STRING      :self.__stringHandler,
			TokenTypes.STATEMENT   :self.__defaultHandler,
			TokenTypes.FUNCTION    :self.__defaultHandler,
			
			TokenTypes.ADD         :self.__defaultHandler,
			TokenTypes.MINUS       :self.__defaultHandler,
			TokenTypes.MUL         :self.__defaultHandler,
			TokenTypes.DIV         :self.__defaultHandler,
			TokenTypes.EXPONENTIAL :self.__defaultHandler,
			
			TokenTypes.EQ          :self.__defaultHandler,
			TokenTypes.NEQ         :self.__defaultHandler,
			TokenTypes.LE          :self.__defaultHandler,
			TokenTypes.GE          :self.__defaultHandler,
			TokenTypes.LESS        :self.__defaultHandler,
			TokenTypes.MORE        :self.__defaultHandler,
			
			TokenTypes.AND         :self.__defaultHandler,
			TokenTypes.OR          :self.__defaultHandler,
			TokenTypes.NOT         :self.__defaultHandler,
   
			TokenTypes.CURLYOPEN   :self.__defaultHandler,
			TokenTypes.CURLYCLOSE  :self.__defaultHandler,
			TokenTypes.ROUNDOPEN   :self.__defaultHandler,
			TokenTypes.ROUNDCLOSE  :self.__defaultHandler,
			
			TokenTypes.SEMICOLON   :self.__defaultHandler,
			TokenTypes.COLON       :self.__defaultHandler,
			
			TokenTypes.COMMA       :self.__defaultHandler,
			TokenTypes.COMMENT     :self.__defaultHandler,
			TokenTypes.IGNORE      :self.__ignoreHandler,
			TokenTypes.LINESTART   :self.__defaultHandler,
			TokenTypes.LINEEND     :self.__defaultHandler,
			TokenTypes.IDENTIFIER  :self.__defaultHandler,
			TokenTypes.WHITESPACE  :self.__ignoreHandler,
			
			TokenTypes.EOF         :self.__defaultHandler
		}
	
	##
	#
	#
	def log(self,message,type="log"):
		if not self._verbose:
			return
		print(message)

	##
	#
	#
	def lex(self,file):

		if self.config is None:
			raise ValueError("Lexer config not set!")

		with open(file, "r", encoding='utf8') as source:
			
			line = source.readline()
			while line:
				line = line.strip("\n")

				if self.config.markLinestart:
					token = self.createUniqueToken(TokenTypes.LINESTART,0)
					self.appendToken(token)

				self.pos = 0

				while self.pos < len(line):

					self.log( "{}".format(line), "verbose")

					while True or self.pos < len(line):
						
						#self.verbose("start scanning ...")
						restart = True
						while restart:
							restart = False
							for expression in self.config.tokens:
								if self.testExpression(line,expression) and self.pos < len(line):
									restart=True
									break

						# Here we have reached a code that we can't parse.
						# So we skip the rest of the line.
						if self.pos < len(line):
							raise ValueError( "Syntax error @ {}:{}".format(self.__line, self.pos) )

						break

				if self.config.markLineend:
					token = self.createUniqueToken(TokenTypes.LINEEND, self.pos)
					self.appendToken(token)

				self.log("", "verbose")
				line = source.readline()
				self.__line += 1
				
			token = self.createUniqueToken(TokenTypes.EOF, self.pos)
			self.appendToken(token)
			
		return 0
	
	##
	#
	#
	def appendToken(self,token):
		if self.firstToken == None:
			self.firstToken = token
		
		if self.currentToken == None:
			self.currentToken = token
		else:
			self.currentToken = self.currentToken.insertAfter(token)

	##
	#
	#
	def testExpression(self,line,expression):
		#self.verbose( "'{}'  '{}' @{}".format(line, expression.expression, self.pos) )
  
		# TODO: We compile each expression each time. Some kind of cache would be nice.
		pattern = re.compile(expression.expression)
  
		#self.log("testing :{}".format(expression),"verbose")
		#self.log(""+line,"verbose")
		#self.log((" "*self.pos)+"*","verbose")
  
		# TODO: search could be faster because it just searches for the first one.
		match = pattern.match(line,self.pos)
		if match:
      
      
			posOld = self.pos
			handler = self.getHandler(expression)
			token = handler(match,expression)
			if token is not None:
				self.appendToken(token)
				self.log( ((" "*posOld)+"{}-{}").format(match[0],TokenTypes.getString(token.type)), "verbose" )
			return True
		return False

	##
	#
	#
	def getHandler(self,expression):

		if expression.type in self._handlerList:
			return self._handlerList[expression.type]

		raise ValueError("No handler defined for {}".format( expression.type))


	##
	#
	#
	def __ignoreHandler(self,match,expression):
		self.pos = match.end()
		return

	##
	#
	#
	def __stringHandler(self,match,expression):
		result = self.createToken(match,expression)
		self.pos = match.end()
		return result

	##
	#
	#
	def __defaultHandler(self,match,expression):
		result = self.createToken(match,expression)
		self.pos = match.end()
		return result

	##
	#
	#
	def getTokenList(self):
		result = []
		token = self.firstToken
		while token:
			result.append(token.generateListToken())
			token = token.next
		return result