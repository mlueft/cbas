import re

import cbas
import cbas.Lexer.Tokens
import cbas.Lexer.TokenTypes
import cbas.Exceptions.Exceptions
import cbas.Compiler.SymbolTable

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
ChainToken = cbas.Lexer.Tokens.ChainToken
SyntaxErrorException = cbas.Exceptions.Exceptions.SyntaxErrorException
SymbolKind = cbas.Compiler.SymbolTable.SymbolKind

class Lexer():

    MODE_ASSIGNMENT = 0
    MODE_EQ         = 1

    def __init__(self):
        self.currentToken    = None
        self.firstToken      = None
        self.line            = 1
        self.pos             = 1
        self.config          = None
        self.mode            = Lexer.MODE_ASSIGNMENT

    ##
    #
    #
    def _handleFirstRemoved(self,ev):
        token = ev.eventSource
        token.onRemoved.remove(self._handleFirstRemoved)
        token.onInsertedBefore.remove(self._handleFirstInsertedBefore)

        self.firstToken = token.next
        self.firstToken.onRemoved.add(self._handleFirstRemoved)
        self.firstToken.onInsertedBefore.add(self._handleFirstInsertedBefore)

    ##
    #
    #
    def _handleFirstInsertedBefore(self, ev):
        if ev.eventSource == self.firstToken:
            self.firstToken.onRemoved.remove(self._handleFirstRemoved)
            self.firstToken.onInsertedBefore.remove(self._handleFirstInsertedBefore)

            self.firstToken = self.firstToken.prev
            self.firstToken.onRemoved.add(self._handleFirstRemoved)
            self.firstToken.onInsertedBefore.add(self._handleFirstInsertedBefore)

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
    
    ## The idea of this function is to remove all colons
    #  so the parser doesn't have to care about
    #  
    #  This works:
    #  print"a":print"b" =>
    #
    #  {
    #     print "a"
    #     print "b"
    #  }
    #
    #  Not yet implemented!!
    #
    #  if a=3 then print "a":print "b" =>
    #
    #  if a=3 then{ print "a":print "b"}
    #   print "a"
    #   print "b"
    #  }
    #
    #
    #  for i = 0 to 10 print "a":print"b": next i =>
    #  for i = 0 to 10{
    #      print "a"
    #      print "b"
    #      next i
    #  }
    #
    def __seperateLines(self, line):
        return [line]
        #
        # Seperate lines by colon
        #
        parts = []
        pos = 0
        partLine = ""
        while pos < len(line):
            c = line[pos]

            if c == ":":
                parts.append(partLine)
                partLine = ""
            else:
                partLine += c

            pos += 1

        parts.append(partLine) 

        if len(parts) > 1:
            parts.insert(0, "{")
            parts.append("}")

        return parts

    ##
    #
    #
    def tokenizeFile(self,file):
        if self.config is None:
            raise ValueError("Lexer config not set!")

        with open(file, "r", encoding='utf8') as source:
            
            while True:
                line = source.readline()
                if line == "": break

                partLines = self.__seperateLines(line)

                for partLine in partLines:
                    partLine = partLine.strip("\n")
                    Tokenizer.tokenizeLine(self,partLine)
                
                self.line += 1
            
            if self.config.markEOF:
                token = Tokenizer.createUniqueToken(self,TokenTypes.EOF, self.pos)
                self.appendToken(token)
            
        return 0

    ##
    #
    #
    def tokenizeLine(self,line):
        if self.config is None:
            raise ValueError("Lexer config not set!")
        
        Tokenizer.tokenizeLine(self,line)

        if self.config.markEOF:
            token = Tokenizer.createUniqueToken(self, TokenTypes.EOF, self.pos)
            self.appendToken(token)

        return 0

    ##
    #
    #
    def appendToken(self,token):
        if self.firstToken is None:
            self.firstToken = token
            self.firstToken.onRemoved.add(self._handleFirstRemoved)
            self.firstToken.onInsertedBefore.add(self._handleFirstInsertedBefore)
        
        if self.currentToken is None:
            self.currentToken = token
        else:
            self.currentToken.insertAfter(token)
            self.currentToken = token

    ##
    #
    #
    def getHandler(self,token):
        
        for h in self.config.tokens:
            if token.type ==h.type:
                return h.handler

        raise ValueError("No handler defined for '{}'".format( TokenTypes.toString(token.type)))






class Tokenizer():
 
    ##
    #
    #
    @staticmethod
    def createUniqueToken(lexer,type=0, pos=0):
        return ChainToken("",lexer.line+1,lexer.pos+1,type)
    
    ##
    #
    #
    @staticmethod
    def createToken(lexer,match,token):
        return ChainToken(match[0],lexer.line,lexer.pos,token.type)

    ##          
    #
    #
    @staticmethod
    def tokenizeLine(lexer, line):
     
        if lexer.config.markLinestart:
            token = Tokenizer.createUniqueToken(lexer,TokenTypes.LINESTART,0)
            lexer.appendToken(token)

        lexer.pos = 0

        while lexer.pos < len(line):

            cbas.log( "{}".format(line), "debug")

            while lexer.pos < len(line):
                
                #self.verbose("start scanning ...")
                restart = True
                while restart:
                    restart = False
                    for expression in lexer.config.tokens:
                        if Tokenizer.testExpression(lexer,line,expression) and lexer.pos < len(line):
                            restart=True
                            break

                # Here we have reached a code that we can't parse.
                # So we skip the rest of the line.
                if lexer.pos < len(line):
                    raise SyntaxErrorException( line, lexer.line, lexer.pos )

                break

        # End of line reached
        lexer.mode = Lexer.MODE_ASSIGNMENT
        
        if lexer.config.markLineend:
            token = Tokenizer.createUniqueToken(lexer,TokenTypes.LINEEND, lexer.pos)
            lexer.appendToken(token)

        return 0

    ##
    #
    #
    @staticmethod
    def testExpression(lexer,line,token):
  
        # TODO: We compile each expression each time. Some kind of cache would be nice.
        pattern = re.compile(token.expression)
  
        match = pattern.match(line,lexer.pos)
        if match:
      
            posOld = lexer.pos
            handler = lexer.getHandler(token)
            token = handler(lexer,match,token)

            # ignoreHandler returns None
            if token is not None:
                
                if token.type in [ TokenTypes.ASSIGNMENT, TokenTypes.EQ]:
                    #
                    # We assume the first = is an assgnment, all following are EQ
                    #
                    if lexer.mode == Lexer.MODE_ASSIGNMENT and lexer.config.hasTokenType(TokenTypes.ASSIGNMENT):
                        token.type = TokenTypes.ASSIGNMENT
                        lexer.mode = Lexer.MODE_EQ
                    else:
                        token.type = TokenTypes.EQ
                
                #
                # Between "if" and "then" we are in mode 1
                # Between "FOR" and "TO" we are in mode 1
                #
                if token.type in [TokenTypes.IF,TokenTypes.FOR]:
                    lexer.mode = Lexer.MODE_EQ

                #
                # End of command reached.
                #
                if token.type in [TokenTypes.COLON, TokenTypes.THEN, TokenTypes.TO]:
                    lexer.mode = Lexer.MODE_ASSIGNMENT

                #
                # Add token to list.
                #
                lexer.appendToken(token)


                cbas.log(((" "*posOld)+"'{}' - ({})").format(match[0],TokenTypes.toString(token.type)),"debug")
            
            return True
        
        return False


    ## Ignors the found match.
    #
    #
    @staticmethod
    def ignoreHandler(lexer,match,expression):
        lexer.pos = match.end()

    ## Creates a string token and adds it to the list
    #
    #
    @staticmethod
    def stringHandler(lexer,match,expression):

        literal = match[0]
        line = lexer.line
        pos = lexer.pos
        type = "string"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,literal,line,pos,SymbolKind.LITERAL)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result
        

    ## Creates a string token and adds it to the list
    #
    #
    @staticmethod
    def scientificHandler(lexer,match,expression):
        #result = Tokenizer.createToken(lexer,match,expression)
        #lexer.pos = match.end()
        #return result
        
        literal = match[0]
        line = lexer.line
        pos = lexer.pos
        type = "scientific"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,literal,line,pos,SymbolKind.LITERAL)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result


    
    ## Creates a string token and adds it to the list
    #
    #
    @staticmethod
    def floatHandler(lexer,match,expression):
        #result = Tokenizer.createToken(lexer,match,expression)
        #lexer.pos = match.end()
        #return result
        literal = match[0]
        line = lexer.line
        pos = lexer.pos
        type = "float"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,literal,line,pos,SymbolKind.LITERAL)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result
    
    ## Creates a string token and adds it to the list
    #
    #
    @staticmethod
    def intHandler(lexer,match,expression):
        #result = Tokenizer.createToken(lexer,match,expression)
        #lexer.pos = match.end()
        #return result
        literal = match[0]
        line = lexer.line
        pos = lexer.pos
        type = "integer"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,literal,line,pos,SymbolKind.LITERAL)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result

    ## Creates a string token and adds it to the list
    #
    #
    @staticmethod
    def booleanHandler(lexer,match,expression):
        #result = Tokenizer.createToken(lexer,match,expression)
        #lexer.pos = match.end()
        #return result
        literal = match[0]
        line = lexer.line
        pos = lexer.pos
        type = "boolean"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,literal,line,pos,SymbolKind.LITERAL)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result
    
    ## Create a token and adds it to the list
    #
    #
    @staticmethod
    def defaultHandler(lexer,match,expression):
        result = Tokenizer.createToken(lexer,match,expression)
        lexer.pos = match.end()
        return result

    ## Adds a variable to the symbol table.
    #
    #
    @staticmethod
    def identifierHandler(lexer,match,expression):
        
        # Variable name
        symbolName = match[0]
        
        line = lexer.line
        pos = lexer.pos

        # Type
        type = "float"
        if symbolName[-1:] == "%":
            type = "integer"
        elif symbolName[-1:] == "$":
            type = "string"

        # Add symbol to table
        symbolId = cbas.symbolTable.addSymbol(type,symbolName,line,pos,SymbolKind.VARIABLE)
        
        # Create token for variable
        result = ChainToken(symbolId,line,pos,expression.type)
        
        lexer.pos = match.end()

        return result