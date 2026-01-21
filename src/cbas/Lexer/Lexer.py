import re

import cbas.Lexer.Tokens as T
import cbas.Lexer.TokenTypes as TT

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
		return T.ChainToken("",self.__line+1,self.pos+1,type)
	
	##
	#
	#
	def createToken(self,match,expression):
		return T.ChainToken(match[0],self.__line+1,self.pos+1,expression.type)

	##
	#
	#
	def createHandlerList(self):
		return {
			TT.TokenTypes.INTEGER     :self.__defaultHandler,
			TT.TokenTypes.FLOAT       :self.__defaultHandler,
			TT.TokenTypes.SIENTIFIC   :self.__defaultHandler,
			TT.TokenTypes.LINENUMBER  :self.__defaultHandler,
			TT.TokenTypes.STRING      :self.__stringHandler,
			TT.TokenTypes.STATEMENT   :self.__defaultHandler,
			TT.TokenTypes.FUNCTION    :self.__defaultHandler,
			
			TT.TokenTypes.ADD         :self.__defaultHandler,
			TT.TokenTypes.MINUS       :self.__defaultHandler,
			TT.TokenTypes.MUL         :self.__defaultHandler,
			TT.TokenTypes.DIV         :self.__defaultHandler,
			TT.TokenTypes.EXPONENTIAL :self.__defaultHandler,
			
			TT.TokenTypes.EQ          :self.__defaultHandler,
			TT.TokenTypes.NEQ         :self.__defaultHandler,
			TT.TokenTypes.LE          :self.__defaultHandler,
			TT.TokenTypes.GE          :self.__defaultHandler,
			TT.TokenTypes.LESS        :self.__defaultHandler,
			TT.TokenTypes.MORE        :self.__defaultHandler,
			
			TT.TokenTypes.AND         :self.__defaultHandler,
			TT.TokenTypes.OR          :self.__defaultHandler,
			TT.TokenTypes.NOT         :self.__defaultHandler,
   
			TT.TokenTypes.CURLYOPEN   :self.__defaultHandler,
			TT.TokenTypes.CURLYCLOSE  :self.__defaultHandler,
			TT.TokenTypes.ROUNDOPEN   :self.__defaultHandler,
			TT.TokenTypes.ROUNDCLOSE  :self.__defaultHandler,
			
			TT.TokenTypes.SEMICOLON   :self.__defaultHandler,
			TT.TokenTypes.COLON       :self.__defaultHandler,
			
			TT.TokenTypes.COMMA       :self.__defaultHandler,
			TT.TokenTypes.COMMENT     :self.__defaultHandler,
			TT.TokenTypes.IGNORE      :self.__ignoreHandler,
			TT.TokenTypes.LINESTART   :self.__defaultHandler,
			TT.TokenTypes.LINEEND     :self.__defaultHandler,
			TT.TokenTypes.IDENTIFIER  :self.__defaultHandler,
			TT.TokenTypes.WHITESPACE  :self.__ignoreHandler,
			
			TT.TokenTypes.EOF         :self.__defaultHandler
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
					token = self.createUniqueToken(TT.TokenTypes.LINESTART,0)
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
					token = self.createUniqueToken(TT.TokenTypes.LINEEND, self.pos)
					self.appendToken(token)

				self.log("", "verbose")
				line = source.readline()
				self.__line += 1
				
			token = self.createUniqueToken(TT.TokenTypes.EOF, self.pos)
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
				self.log( ((" "*posOld)+"{}-{}").format(match[0],TT.TokenTypes.getString(token.type)), "verbose" )
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