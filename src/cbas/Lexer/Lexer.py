import re

import cbas.Lexer.Tokens
import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
ChainToken = cbas.Lexer.Tokens.ChainToken

class Lexer():

    def __init__(self):
        self.debug           = False
        self.currentToken    = None
        self.firstToken      = None
        self.line            = 0
        self.pos             = 0
        self.config          = None
        self.debug = False
        # 0 => = is assignment
        # 1 => = is EQ
        self.mode = 0

    ##
    #
    #
    def log(self,message,type="log"):
        if self.debug:
            print(message)

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
    
    ##
    #
    #
    def tokenizeFile(self,file):
        if self.config is None:
            raise ValueError("Lexer config not set!")

        with open(file, "r", encoding='utf8') as source:
            
            line = source.readline()
            while line:
                line = line.strip("\n")

                Tokenizer.tokenizeLine(self,line)

                self.log("", "debug")
                line = source.readline()
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
        if self.firstToken == None:
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
    def getHandler(self,expression):
        
        for h in self.config.tokens:
            if expression.type ==h.type:
                return h.handler

        raise ValueError("No handler defined for '{}'".format( TokenTypes.getString(expression.type)))






class Tokenizer():


    ##
    #
    #
    @staticmethod
    def __createHandlerList():
        return {
            TokenTypes.INTEGER     :Tokenizer.defaultHandler,
            TokenTypes.FLOAT       :Tokenizer.defaultHandler,
            TokenTypes.SIENTIFIC   :Tokenizer.defaultHandler,
            TokenTypes.LINENUMBER  :Tokenizer.defaultHandler,
            TokenTypes.STRING      :Tokenizer.stringHandler,
            TokenTypes.BOOLEAN     :Tokenizer.defaultHandler,
            
            TokenTypes.ADD         :Tokenizer.defaultHandler,
            TokenTypes.MINUS       :Tokenizer.defaultHandler,
            TokenTypes.MUL         :Tokenizer.defaultHandler,
            TokenTypes.DIV         :Tokenizer.defaultHandler,
            TokenTypes.EXPONENTIAL :Tokenizer.defaultHandler,
            
            TokenTypes.EQ          :Tokenizer.defaultHandler,
            TokenTypes.NEQ         :Tokenizer.defaultHandler,
            TokenTypes.LE          :Tokenizer.defaultHandler,
            TokenTypes.GE          :Tokenizer.defaultHandler,
            TokenTypes.LESS        :Tokenizer.defaultHandler,
            TokenTypes.MORE        :Tokenizer.defaultHandler,
            
            TokenTypes.AND         :Tokenizer.defaultHandler,
            TokenTypes.OR          :Tokenizer.defaultHandler,
            TokenTypes.NOT         :Tokenizer.defaultHandler,
   
            TokenTypes.CURLYOPEN   :Tokenizer.defaultHandler,
            TokenTypes.CURLYCLOSE  :Tokenizer.defaultHandler,
            TokenTypes.ROUNDOPEN   :Tokenizer.defaultHandler,
            TokenTypes.ROUNDCLOSE  :Tokenizer.defaultHandler,
            
            TokenTypes.SEMICOLON   :Tokenizer.defaultHandler,
            TokenTypes.COLON       :Tokenizer.defaultHandler,
            
            TokenTypes.COMMA       :Tokenizer.defaultHandler,
            TokenTypes.COMMENT     :Tokenizer.defaultHandler,
            TokenTypes.IGNORE      :Tokenizer.ignoreHandler,
            TokenTypes.LINESTART   :Tokenizer.defaultHandler,
            TokenTypes.LINEEND     :Tokenizer.defaultHandler,
            TokenTypes.IDENTIFIER  :Tokenizer.defaultHandler,
            TokenTypes.WHITESPACE  :Tokenizer.ignoreHandler,
            
            TokenTypes.EOF         :Tokenizer.defaultHandler,

            TokenTypes.CLR         :Tokenizer.defaultHandler,
            TokenTypes.NEW         :Tokenizer.defaultHandler,
            TokenTypes.RESTORE     :Tokenizer.defaultHandler,
            TokenTypes.RETURN      :Tokenizer.defaultHandler,
            TokenTypes.ST          :Tokenizer.defaultHandler,
            TokenTypes.STATUS      :Tokenizer.defaultHandler,
            TokenTypes.STOP        :Tokenizer.defaultHandler,
            TokenTypes.TI          :Tokenizer.defaultHandler,
            TokenTypes.TI_DOLLAR   :Tokenizer.defaultHandler,
            TokenTypes.TIME        :Tokenizer.defaultHandler,
            TokenTypes.TIME_DOLLAR :Tokenizer.defaultHandler,
            TokenTypes.PISIGN      :Tokenizer.defaultHandler,
            TokenTypes.END         :Tokenizer.defaultHandler,
            TokenTypes.CONT        :Tokenizer.defaultHandler,

            TokenTypes.SYS         :Tokenizer.defaultHandler,
            TokenTypes.RSPCOLOR    :Tokenizer.defaultHandler,
            TokenTypes.RSSPRITE    :Tokenizer.defaultHandler,
            TokenTypes.RIGHT_DOLLAR:Tokenizer.defaultHandler,
            TokenTypes.HEX_DOLLAR  :Tokenizer.defaultHandler,
            TokenTypes.RSPPOS      :Tokenizer.defaultHandler,
            TokenTypes.LEFT_DOLLAR :Tokenizer.defaultHandler,
            TokenTypes.INSTR       :Tokenizer.defaultHandler,
            TokenTypes.CHR_DOLLAR  :Tokenizer.defaultHandler,
            TokenTypes.MID_DOLLAR  :Tokenizer.defaultHandler,
            TokenTypes.STR_DOLLAR  :Tokenizer.defaultHandler,
            TokenTypes.ERR_DOLLAR  :Tokenizer.defaultHandler,
            TokenTypes.RDOT        :Tokenizer.defaultHandler,
            TokenTypes.PEEK        :Tokenizer.defaultHandler,
            TokenTypes.POKE        :Tokenizer.defaultHandler,
            TokenTypes.VERIFY      :Tokenizer.defaultHandler,
            TokenTypes.SAVE        :Tokenizer.defaultHandler,
            TokenTypes.LOAD        :Tokenizer.defaultHandler,
            TokenTypes.WAIT        :Tokenizer.defaultHandler,

            TokenTypes.DEC         :Tokenizer.defaultHandler,
            TokenTypes.PEN         :Tokenizer.defaultHandler,
            TokenTypes.POT         :Tokenizer.defaultHandler,
            TokenTypes.USR         :Tokenizer.defaultHandler,
            TokenTypes.ABS         :Tokenizer.defaultHandler,
            TokenTypes.ASC         :Tokenizer.defaultHandler,
            TokenTypes.ATN         :Tokenizer.defaultHandler,
            TokenTypes.INT         :Tokenizer.defaultHandler,
            TokenTypes.COS         :Tokenizer.defaultHandler,
            TokenTypes.EXP         :Tokenizer.defaultHandler,
            TokenTypes.FRE         :Tokenizer.defaultHandler,
            TokenTypes.LEN         :Tokenizer.defaultHandler,
            TokenTypes.LOG         :Tokenizer.defaultHandler,
            TokenTypes.POS         :Tokenizer.defaultHandler,
            TokenTypes.RND         :Tokenizer.defaultHandler,
            TokenTypes.SGN         :Tokenizer.defaultHandler,
            TokenTypes.SIN         :Tokenizer.defaultHandler,
            TokenTypes.SPC         :Tokenizer.defaultHandler,
            TokenTypes.SQR         :Tokenizer.defaultHandler,
            TokenTypes.SYS         :Tokenizer.defaultHandler,
            TokenTypes.TAB         :Tokenizer.defaultHandler,
            TokenTypes.TAN         :Tokenizer.defaultHandler,
            TokenTypes.VAL         :Tokenizer.defaultHandler,
            TokenTypes.TO          :Tokenizer.defaultHandler,
            TokenTypes.GOTO        :Tokenizer.defaultHandler,
            TokenTypes.GOSUB       :Tokenizer.defaultHandler,
            TokenTypes.RUN         :Tokenizer.defaultHandler,
            TokenTypes.CLOSE       :Tokenizer.defaultHandler,
            TokenTypes.OPEN        :Tokenizer.defaultHandler,
            TokenTypes.NEXT        :Tokenizer.defaultHandler,
            TokenTypes.LIST        :Tokenizer.defaultHandler,
            TokenTypes.LET         :Tokenizer.ignoreHandler,
            TokenTypes.FN          :Tokenizer.defaultHandler,
            TokenTypes.READ        :Tokenizer.defaultHandler,
            TokenTypes.DATA        :Tokenizer.defaultHandler,
            TokenTypes.GET         :Tokenizer.defaultHandler,
            TokenTypes.GET_SHARP   :Tokenizer.defaultHandler,
            TokenTypes.INPUT_SHARP :Tokenizer.defaultHandler,
            TokenTypes.PRINT_SHARP :Tokenizer.defaultHandler,
            TokenTypes.CMD         :Tokenizer.defaultHandler,
            TokenTypes.SEMICOLON   :Tokenizer.defaultHandler,
            TokenTypes.DEF         :Tokenizer.defaultHandler,
            TokenTypes.ON          :Tokenizer.defaultHandler,
            TokenTypes.INPUT       :Tokenizer.defaultHandler,
            TokenTypes.DIM         :Tokenizer.defaultHandler,
            TokenTypes.PRINT       :Tokenizer.defaultHandler,
            TokenTypes.IF          :Tokenizer.defaultHandler,
            TokenTypes.THEN        :Tokenizer.defaultHandler,
            TokenTypes.FOR         :Tokenizer.defaultHandler,
            TokenTypes.TO          :Tokenizer.defaultHandler,
            TokenTypes.STEP        :Tokenizer.defaultHandler,
            
        }
    

            
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
    def createToken(lexer,match,expression):
        return ChainToken(match[0],lexer.line+1,lexer.pos+1,expression.type)


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

            lexer.log( "{}".format(line), "debug")

            while True or lexer.pos < len(line):
                
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
                    raise ValueError( "Syntax error @ {}:{}".format(lexer.line, lexer.pos) )

                break

        # End of line reached
        lexer.mode = 0
        
        if lexer.config.markLineend:
            token = Tokenizer.createUniqueToken(lexer,TokenTypes.LINEEND, lexer.pos)
            lexer.appendToken(token)

        return 0


    ##
    #
    #
    @staticmethod
    def testExpression(lexer,line,expression):
  
        # TODO: We compile each expression each time. Some kind of cache would be nice.
        pattern = re.compile(expression.expression)
  
        match = pattern.match(line,lexer.pos)
        if match:
      
      
            posOld = lexer.pos
            handler = lexer.getHandler(expression)
            token = handler(lexer,match,expression)
            if token is not None:
                
                if token.type in [ TokenTypes.ASSIGNMENT, TokenTypes.EQ]:
                    # We assume the first = is an assgnment, all following are EQ
                    if lexer.mode == 0 and lexer.config.hasTokenType(TokenTypes.ASSIGNMENT):
                        token.type = TokenTypes.ASSIGNMENT
                        lexer.mode = 1
                    else:
                        token.type = TokenTypes.EQ
                
                # Between "if" and "then" we are in mode 1
                # Between "FOR" and "TO" we are in mode 1
                if token.type in [TokenTypes.IF,TokenTypes.FOR]:
                    lexer.mode = 1

                # End of command reached.
                if token.type in [TokenTypes.COLON, TokenTypes.THEN, TokenTypes.TO]:
                    lexer.mode = 0

                lexer.appendToken(token)
                lexer.log(((" "*posOld)+"'{}' - ({})").format(match[0],TokenTypes.getString(token.type)),"debug")

            return True
        return False

    ##
    #
    #
    @staticmethod
    def ignoreHandler(lexer,match,expression):
        lexer.pos = match.end()
        return

    ##
    #
    #
    @staticmethod
    def stringHandler(lexer,match,expression):
        result = Tokenizer.createToken(lexer,match,expression)
        lexer.pos = match.end()
        return result

    ##
    #
    #
    @staticmethod
    def defaultHandler(lexer,match,expression):
        result = Tokenizer.createToken(lexer,match,expression)
        lexer.pos = match.end()
        return result

