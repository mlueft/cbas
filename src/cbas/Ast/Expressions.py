import cbas.Lexer.TokenTypes
import cbas.Parser.Lookups
import cbas.Parser.BindingPower
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList
import cbas.DataStructures.TreeNode
import cbas.DataStructures.TraverseMode

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
Lookups = cbas.Parser.Lookups.Lookups
BindingPower = cbas.Parser.BindingPower.BindingPower
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event
LinkedList = cbas.DataStructures.LinkedList.LinkedList
TreeNode = cbas.DataStructures.TreeNode.TreeNode

class ExpressionParser():
    
    STATEMENTS = [
        TokenTypes.CLR,
        TokenTypes.NEW,
        TokenTypes.RESTORE,
        TokenTypes.RETURN,
        TokenTypes.ST,
        TokenTypes.STATUS,
        TokenTypes.STOP,
        TokenTypes.TI,
        TokenTypes.TI_DOLLAR,
        TokenTypes.TIME,
        TokenTypes.TIME_DOLLAR,
        TokenTypes.PISIGN,
        TokenTypes.END,
        TokenTypes.CONT,
        TokenTypes.GOTO,
        TokenTypes.GOSUB,
        TokenTypes.RUN,
        TokenTypes.CLOSE,
        TokenTypes.POKE,
        TokenTypes.VERIFY,
        TokenTypes.SAVE,
        TokenTypes.LOAD,
        TokenTypes.WAIT,
        TokenTypes.OPEN,
        TokenTypes.NEXT,
        TokenTypes.LIST,
        TokenTypes.READ,
        TokenTypes.DATA,
        TokenTypes.GET,
        TokenTypes.GET_SHARP,
        TokenTypes.INPUT_SHARP,
        TokenTypes.PRINT_SHARP,
        TokenTypes.CMD,
        TokenTypes.DEF,
        TokenTypes.ON,
        TokenTypes.INPUT,
        TokenTypes.DIM,
        TokenTypes.PRINT,
        TokenTypes.SEMICOLON,
        TokenTypes.IF,
        TokenTypes.FOR
    ]
    
    FUNCTIONS = [
        TokenTypes.SYS,
        TokenTypes.ABS,
        TokenTypes.LEFT_DOLLAR,
        TokenTypes.MID_DOLLAR,
        TokenTypes.RIGHT_DOLLAR,
        TokenTypes.STR_DOLLAR,
        TokenTypes.CHR_DOLLAR,
        TokenTypes.ABS,
        TokenTypes.ASC,
        TokenTypes.ATN,
        TokenTypes.PEEK,
        TokenTypes.COS,
        TokenTypes.FRE,
        TokenTypes.INT,
        TokenTypes.LEN,
        TokenTypes.LOG,
        TokenTypes.POS,
        TokenTypes.RND,
        TokenTypes.SGN,
        TokenTypes.SIN,
        TokenTypes.SPC,
        TokenTypes.SQR,
        TokenTypes.TAB,
        TokenTypes.TAN,
        TokenTypes.USR,
        TokenTypes.VAL,
        TokenTypes.EXP
    ]

    ## 4
    #  "BLA"
    #  4.1
    #  5.4+e3
    #
    @staticmethod
    def parsePrimaryExpression(parser):
        parser.log("start:parsePrimaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        type = parser.currentTokenType
        
        if type == TokenTypes.INTEGER:
            token = parser.advance()
            result = PrimaryExpression( "int", int(token.code), token )
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.FLOAT:
            token = parser.advance()
            result = PrimaryExpression( "float", float(token.code), token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.SIENTIFIC:
            token = parser.advance()
            result = PrimaryExpression( "scientific", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.STRING:
            token = parser.advance()
            result = PrimaryExpression( "string", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.BOOLEAN:
            token = parser.advance()
            result = PrimaryExpression( "boolean", token.code.lower() == 'true', token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
            
        elif type == TokenTypes.IDENTIFIER:
            token = parser.advance()
            result = PrimaryExpression( "symbol", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LINENUMBER:
            token = parser.advance()
            result = PrimaryExpression( "linenumber", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COMMENT:
            token = parser.advance()
            result = PrimaryExpression( "comment", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LINEEND:
            token = parser.advance()
            result = PrimaryExpression( "lineend", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COLON:
            token = parser.advance()
            result = PrimaryExpression( "colon", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.SEMICOLON:
            token = parser.advance()
            result = PrimaryExpression( "semicolon", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COMMA:
            token = parser.advance()
            result = PrimaryExpression( "comma", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result


        elif type in [ TokenTypes.MUL, TokenTypes.DIV, TokenTypes.ADD, TokenTypes.MINUS ]:
            token = parser.advance()
            result = PrimaryExpression( "arithmetic", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
                
        elif type in [ TokenTypes.EQ, TokenTypes.NEQ, TokenTypes.LESS, TokenTypes.MORE, TokenTypes.LE, TokenTypes.GE, TokenTypes.AND, TokenTypes.OR, TokenTypes.NOT]:
            token = parser.advance()
            result = PrimaryExpression( "logical", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type in ExpressionParser.FUNCTIONS:
            token = parser.advance()
            result = PrimaryExpression( "function", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type in ExpressionParser.STATEMENTS:
            token = parser.advance()
            result = PrimaryExpression( "statement", token.code, token)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result        
        else:
            raise ValueError( "Can't generate primary expression for {}!".format(TokenTypes.getString(type)) )
    
    ##
    #
    #    
    @staticmethod
    def parseExpression(parser, bp):
        parser.log("start:parseExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )


        # parse nud
        tokenType   = parser.currentTokenType

        if tokenType not in Lookups.nud:
            raise ValueError("Nud handler expected for token type ({})".format(TokenTypes.getString(tokenType)) )
        
        nudFunction = Lookups.nud[tokenType]

        left = nudFunction(parser)
         
        # This is for linenumber/labels/eof
        if parser.currentTokenType not in Lookups.bp:
            parser.log("end:parseExpression ... ", "debug" )
            return left

        while  Lookups.bp[parser.currentTokenType] > bp:
            tokenType = parser.currentTokenType
            
            if tokenType not in Lookups.led:
                raise ValueError("Led handler expected for token type ({})".format(TokenTypes.getString(tokenType)) )
            
            ledFunction = Lookups.led[tokenType]
            left = ledFunction(parser,left,Lookups.bp[parser.currentTokenType])

            # This is for linenumber/labels/eof
            if parser.currentTokenType not in Lookups.bp:
                parser.log("end:parseExpression ... ", "debug" )
                return left
            
        parser.log("end:parseExpression ... ", "debug" )
        return left

    ##
    #
    #
    @staticmethod
    def parseIgnoreToken(parser, left=None, bp=None ):
        parser.advance()
        
    ##
    #
    #
    @staticmethod
    def parseBinaryExpression(parser, left, bp ):
        parser.log("start:parseBinaryExpression ... '{}' ({}) @ {}".format(
            parser.currentToken.code,
            TokenTypes.getString( parser.currentToken.type ),
            parser.pos
        ), "debug" )

        operatorToken = ExpressionParser.parsePrimaryExpression(parser) #parser.advance()
        right = ExpressionParser.parseExpression(parser, bp)

        result = BinaryExpression(
            left,
            operatorToken,
            right
        )

        parser.log("end:parseBinaryExpression", "debug" )
        return result
   
    ##
    #
    #
    @staticmethod
    def parsePrefixExpression(parser):
        parser.log("start:parsePrefixExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        operatorToken = ExpressionParser.parsePrimaryExpression(parser) #parser.advance()
        right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = PrefixExpression(
            operatorToken,
            right
        )
        
        parser.log("end:parsePrefixExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseGroupingExpression(parser):
        parser.log("start:parseGroupingExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        start = parser.advance()
        expression = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = GroupingExpression(
            expression
        )
        parser.expect( TokenTypes.ROUNDCLOSE )

        parser.log("end:parseGroupingExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseAssignmentExpression(parser, left, bp):
        parser.log("start:parseAssignmentExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # We skip the "="
        parser.advance()
        right = ExpressionParser.parseExpression(parser,bp)
        result = AssignmentExpression(left, right)
        parser.log("end:parseAssignmentExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseProcedureCallExpression(parser, left,bp):
        parser.log("start:parseProcedureCallExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        functionName = left #ExpressionParser.parseExpression(parser,BindingPower.DEFAULT) #parser.advance()
        parameters = []

        # we skip the "("
        parser.advance()

        # we collect all parameters
        ct = parser.currentTokenType
        while ct != TokenTypes.ROUNDCLOSE:
            expr = ExpressionParser.parseExpression(parser,bp)# BindingPower.DEFAULT)
            parameters.append( expr )
            
            # We skip the parameter seperator
            if parser.currentTokenType == TokenTypes.COMMA:
                parser.advance()

            ct = parser.currentTokenType

        # we skip ")"
        parser.advance()

        result = CallExpression(functionName,parameters)
        parser.log("end:parseProcedureCallExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseStatementExpression(parser):
        parser.log("start:parseStatementExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []

        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            if parser.currentTokenType == TokenTypes.COMMA:
                parser.advance()
        
        result = StatementExpression(statement,parameters)
        parser.log("end:parseStatementExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseListStatement(parser):
        parser.log("start:parseListStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []

        if parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parsePrimaryExpression(parser)
            parameters.append(right)
            
            if parser.currentTokenType == TokenTypes.MINUS:
                # We skip the "-"
                parser.advance()

                right = ExpressionParser.parsePrimaryExpression(parser)
                parameters.append(right)
        result = StatementExpression(statement,parameters)
        parser.log("end:parseListStatement", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseFNExpression(parser):
        parser.log("start:parseFNExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        parameters = []
        # we skip "FN"
        parser.advance()
        functionName = ExpressionParser.parsePrimaryExpression(parser)
        parser.expect(TokenTypes.ROUNDOPEN)
        parameters.append( ExpressionParser.parsePrimaryExpression(parser))
        parser.expect(TokenTypes.ROUNDCLOSE)
        
        result = FunctionCallExpression(functionName,parameters)
        parser.log("end:parseFNExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseCMDExpression(parser):
        parser.log("start:parseCMDExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            if parser.currentTokenType in[TokenTypes.COMMA,TokenTypes.SEMICOLON]:
                parser.advance()
        result =  StatementExpression(statement,parameters)
        parser.log("end:parseCMDExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseDEFExpression(parser):
        parser.log("start:parseDEFExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # we skip "def"
        parser.advance()
        # we skip "fn"
        parser.advance()
        functionName = ExpressionParser.parsePrimaryExpression(parser)
        # we skip "("
        parser.advance()
        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.ROUNDCLOSE,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parsePrimaryExpression(parser)
            parameters.append(right)
            
            if parser.currentTokenType in[TokenTypes.COMMA]:
                parser.advance()
        # we skip ")"
        parser.advance()
        # we skip "="
        parser.advance()
        body = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)
        
        result = FunctionDefinitionExpression(functionName,parameters,body)
        parser.log("end:parseDEFExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseONExpression(parser):
        parser.log("start:parseONExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # We skip "on"
        parser.advance()

        index = ExpressionParser.parsePrimaryExpression(parser)

        # We expect goto or gosub
        if not parser.currentTokenType in [TokenTypes.GOTO, TokenTypes.GOSUB]:
            raise ValueError("Expecting goto or gosub!")
        
        jumpMethode = ExpressionParser.parsePrimaryExpression(parser)

        lineNumbers = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parsePrimaryExpression(parser)
            lineNumbers.append(right)
            
            if parser.currentTokenType in[TokenTypes.COMMA]:
                parser.advance()
        result = OnExpression(index,jumpMethode,lineNumbers)
        parser.log("end:parseGroupingExpression", "debug" )
        return result
    
    ##
    #
    #
    @staticmethod
    def parseINPUTExpression(parser):
        parser.log("start:parseINPUTExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)

        message = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        
        # We skip ";"
        parser.advance()

        parameters = [message]
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            if parser.currentTokenType in[TokenTypes.COMMA]:
                parser.advance()
        parser.log("end:parseINPUTExpression", "debug" )
        result = StatementExpression(statement,parameters)
        return result

    ##
    #
    #
    @staticmethod
    def parseDIMExpression(parser):
        parser.log("start:parseDIMExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # We skip "dim"
        parser.advance()

        variable = ExpressionParser.parsePrimaryExpression(parser)
        
        # We skip "("
        parser.advance()

        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.ROUNDCLOSE,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            if parser.currentTokenType in[TokenTypes.COMMA]:
                parser.advance()

        # We skip ")"
        parser.advance()

        assignment = None
        # There yould be an assignment
        if parser.currentTokenType in [TokenTypes.ASSIGNMENT]:
            # We skip thee "="
            parser.advance()

            assignment = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)
        result = DimExpression(variable,parameters, assignment)
        parser.log("end:parseDIMExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parsePRINTExpression(parser):
        parser.log("start:parsePRINTExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            if parser.currentTokenType in [TokenTypes.COMMA, TokenTypes.SEMICOLON]:
                seperator = ExpressionParser.parsePrimaryExpression(parser)
                parameters.append(seperator)
        result = StatementExpression(statement,parameters)
        parser.log("end:parsePRINTExpression", "debug" )
        return result
    
    ##
    #
    #
    @staticmethod
    def parseIFExpression(parser):
        parser.log("start:parseIFExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # We skip "if"
        parser.advance()

        condition = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        # We skip "then"
        if parser.currentTokenType in [TokenTypes.THEN]:
            parser.advance()

        code = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            code.append(right)
            
            # We skip ":"
            if parser.currentTokenType in [TokenTypes.COLON]:
                parser.advance()
        result = IfExpression(condition, code)
        parser.log("end:parseIFExpression", "debug" )
        return result
    
    ##
    #
    #
    @staticmethod
    def parseFORExpression(parser):
        parser.log("start:parseFORExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        # We skip "for"
        parser.advance()

        runner = ExpressionParser.parsePrimaryExpression(parser)

        # We skip "="
        parser.advance()

        start = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        # We skip "TO"
        parser.advance()

        end = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        step = None
        if parser.currentTokenType in [TokenTypes.STEP]:
            # We skip "step"
            parser.advance()
            step = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        loopCode = []
        while parser.currentTokenType not in [TokenTypes.NEXT,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            loopCode.append(right)
            
            # We skip ":"
            if parser.currentTokenType in [TokenTypes.COLON]:
                parser.advance()

        # 
        result = ForExpression(runner,start,end,step, loopCode)
        parser.log("end:parseFORExpression", "debug" )
        return result









##
#
#
class Expression(TreeNode):

    def __init__(self, value = None):
        super().__init__()
        self.value = value

    def _getNodes(self):
        return [self.value]

##
#
#
class PrimaryExpression(Expression):
    
    def __init__(self, tag=None, value = None, token = None):
        super().__init__(value)
        self.tag = tag
        self.__token = token
        self._isLeaf = True

    @property
    def type(self):
        if self.__token is None:
            return TokenTypes.UNDEFINED
        return self.__token.type
    
    @property
    def code(self):
        if self.__token is None:
            return None
        return self.__token.code

    @property
    def line(self):
        if self.__token is None:
            return None
        return self.__token.line

    @property
    def pos(self):
        if self.__token is None:
            return None
        return self.__token.pos

    def _getNodes(self):
        return []

    def debug(self,level=0):
        print( "{:<4}:{}tag:'{}' value:'{}' type:{} @{}:{}".format(self.id, " "*level*self.indentation, self.tag, self.value,  TokenTypes.getString(self.__token),self.line,self.pos) )

    def __str__(self):
        return "{:<4} {}".format( self.tag, self.value)
    
    def outline(self, handler):
        handler(self,TraverseMode.OUTLINE)

    def bottomUp(self, handler):
        handler(self,TraverseMode.BOTTOM_UP)

    def topDown(self, handler):
        handler(self,TraverseMode.TOP_DOWN)

##
#   4+3
#   4-3
#   4*3
#   ...
# 
class BinaryExpression(Expression):

    def __init__(self, left, operator, right):
        super().__init__()

        self.left = left
        self.operator = operator
        self.right = right
        
        self.left.onReplace.add(self._hndReplaceLeft)
        self.operator.onReplace.add(self._hndReplaceOperator)
        self.right.onReplace.add(self._hndReplaceRight)

    def _hndReplaceLeft(self,ev):
        #print("BinaryExpression::_hndReplaceLeft")
        self.left.onReplace.remove(self._hndReplaceLeft)
        self.left = ev.replacement
        self.left.onReplace.add(self._hndReplaceLeft)

    def _hndReplaceOperator(self,ev):
        #print("BinaryExpression::_hndReplaceOperator")
        self.operator.onReplace.remove(self._hndReplaceOperator)
        self.operator = ev.replacement
        self.operator.onReplace.add(self._hndReplaceOperator)

    def _hndReplaceRight(self,ev):
        #print("BinaryExpression::_hndReplaceRight")
        self.right.onReplace.remove(self._hndReplaceRight)
        self.right = ev.replacement
        self.right.onReplace.add(self._hndReplaceRight)

    def _getNodes(self):
        return [self.left,self.operator,self.right]


##
#
#
class PrefixExpression(Expression):

    def __init__(self, operator, right):
        super().__init__()
        
        self.operator = operator
        self.right = right

        self.operator.onReplace.add(self._hndReplaceOperator)
        self.right.onReplace.add(self._hndReplaceRight)

    def _hndReplaceOperator(self,ev):
        #print("PrefixExpression::_hndReplaceOperator")
        self.operator.onReplace.remove(self._hndReplaceOperator)
        self.operator = ev.replacement
        self.operator.onReplace.add(self._hndReplaceOperator)

    def _hndReplaceRight(self,ev):
        #print("PrefixExpression::_hndReplaceRight")
        self.right.onReplace.remove(self._hndReplaceRight)
        self.right = ev.replacement
        self.right.onReplace.add(self._hndReplaceRight)

    def _getNodes(self):
        return [self.operator,self.right]
    
##
#
#
class GroupingExpression(Expression):

    def __init__(self, expression):
        super().__init__(expression)
        self.value.onReplace.add(self._hndReplaceValue)

    def _hndReplaceValue(self,ev):
        #print("GroupingExpression::_hndReplaceValue")
        self.value.onReplace.remove(self._hndReplaceValue)
        self.value = ev.replacement
        self.value.onReplace.add(self._hndReplaceValue)

##
#
#
class AssignmentExpression(Expression):

    def __init__(self,right, left):
        super().__init__()
        self.right = right
        self.left = left
        
        self.left.onReplace.add(self._hndReplaceLeft)
        self.right.onReplace.add(self._hndReplaceRight)
    

    def _hndReplaceLeft(self,ev):
        #print("BinaryExpression::_hndReplaceLeft")
        self.left.onReplace.remove(self._hndReplaceLeft)
        self.left = ev.replacement
        self.left.onReplace.add(self._hndReplaceLeft)

    def _hndReplaceRight(self,ev):
        #print("BinaryExpression::_hndReplaceRight")
        self.right.onReplace.remove(self._hndReplaceRight)
        self.right = ev.replacement
        self.right.onReplace.add(self._hndReplaceRight)

    def _getNodes(self):
        return [self.right, self.left]
##
#
#
class CallExpression(Expression):

    def __init__(self, function, parameters):
        super().__init__()
        self.function = function
        self.parameters = parameters

        self.function.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.function.onReplace.remove(self._hndReplaceFunction)
        self.function = ev.replacement
        self.function.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):

        result = []
        result.append(self.function) 
        for p in self.parameters:
            result.append(p)
        return result
    
##
#
#
class StatementExpression(Expression):

    def __init__(self, statement, parameters):
        super().__init__()
        self.statement = statement
        self.parameters = parameters

        self.statement.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.statement.onReplace.remove(self._hndReplaceFunction)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.statement) 
        for p in self.parameters:
            result.append(p)
        return result
    
##
#
#
class FunctionCallExpression(Expression):

    def __init__(self, functionName, parameters):
        super().__init__()
        self.functionName = functionName
        self.parameters = parameters

        self.functionName.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.functionName.onReplace.remove(self._hndReplaceFunction)
        self.functionName = ev.replacement
        self.functionName.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.functionName) 
        for p in self.parameters:
            result.append(p)
        return result
    
##
#
#
class FunctionDefinitionExpression(Expression):

    def __init__(self, functionName, parameters, body):
        super().__init__()
        self.functionName = functionName
        self.parameters = parameters
        self.body = body

        self.functionName.onReplace.add(self._hndReplaceFunction)
        self.body.onReplace.add(self._hndReplaceBody)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.functionName.onReplace.remove(self._hndReplaceFunction)
        self.functionName = ev.replacement
        self.functionName.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceBody(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.body.onReplace.remove(self._hndReplaceBody)
        self.body = ev.replacement
        self.body.onReplace.add(self._hndReplaceBody)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.functionName) 
        for p in self.parameters:
            result.append(p)
        result.append(self.body)
        return result
    
##
#
#
class OnExpression(Expression):

    def __init__(self, index, jumpMethode, lineNumbers):
        super().__init__()
        self.index = index
        self.jumpMethode = jumpMethode
        self.lineNumbers = lineNumbers

        self.index.onReplace.add(self._hndReplaceIndex)
        self.jumpMethode.onReplace.add(self._hndReplaceJumpMethode)

        for s in self.lineNumbers:
            s.onReplace.add(self._hndReplaceLineNumber)

    def _hndReplaceIndex(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.index.onReplace.remove(self._hndReplaceIndex)
        self.index = ev.replacement
        self.index.onReplace.add(self._hndReplaceIndex)

    def _hndReplaceJumpMethode(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.jumpMethode.onReplace.remove(self._hndReplaceJumpMethode)
        self.jumpMethode = ev.replacement
        self.jumpMethode.onReplace.add(self._hndReplaceJumpMethode)

    def _hndReplaceLineNumber(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.lineNumbers):
            if ev.eventSource == v:
                self.lineNumbers[i].onReplace.remove(self._hndReplaceLineNumber)
                self.lineNumbers[i] = ev.replacement
                self.lineNumbers[i].onReplace.add(self._hndReplaceLineNumber)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.index) 
        result.append(self.jumpMethode) 
        for p in self.lineNumbers:
            result.append(p)
        return result
    
##
#
#
class DimExpression(Expression):

    def __init__(self, variable, dimensions, assignment=None):
        super().__init__()
        self.variable = variable
        self.dimensions = dimensions
        self.assignment = None
        
        self.variable.onReplace.add(self._hndReplaceVariable)

        if assignment is not None:
            self.assignment = assignment
            self.assignment.onReplace.add(self._hndReplaceAssignment)


        for s in self.dimensions:
            s.onReplace.add(self._hndReplaceDimension)

    def _hndReplaceVariable(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.variable.onReplace.remove(self._hndReplaceVariable)
        self.variable = ev.replacement
        self.variable.onReplace.add(self._hndReplaceVariable)

    def _hndReplaceAssignment(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.assignment.onReplace.remove(self._hndReplaceAssignment)
        self.assignment = ev.replacement
        self.assignment.onReplace.add(self._hndReplaceAssignment)

    def _hndReplaceDimension(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.dimensions):
            if ev.eventSource == v:
                self.dimensions[i].onReplace.remove(self._hndReplaceDimension)
                self.dimensions[i] = ev.replacement
                self.dimensions[i].onReplace.add(self._hndReplaceDimension)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.variable)
        for p in self.dimensions:
            result.append(p)
        if self.assignment is not None:
            result.append(self.assignment)
        return result
    
##
#
#
class IfExpression(Expression):

    def __init__(self, condition, code):
        super().__init__()
        self.condition = condition
        self.code = code
        
        self.condition.onReplace.add(self._hndReplaceCondition)
        for s in self.code:
            s.onReplace.add(self._hndReplaceCode)


    def _hndReplaceCondition(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.condition.onReplace.remove(self._hndReplaceCondition)
        self.condition = ev.replacement
        self.condition.onReplace.add(self._hndReplaceCondition)

    def _hndReplaceCode(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.code):
            if ev.eventSource == v:
                self.code[i].onReplace.remove(self._hndReplaceCode)
                self.code[i] = ev.replacement
                self.code[i].onReplace.add(self._hndReplaceCode)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.condition)
        for p in self.code:
            result.append(p)
        return result
    
##
#
#
class ForExpression(Expression):

    def __init__(self, runner, start, end, step=None, loopCode=None):
        super().__init__()
        
        self.runner = runner
        self.start = start
        self.end = end
        self.step = step
        self.loopCode = loopCode
        
        self.runner.onReplace.add(self._hndReplaceRunner)
        self.start.onReplace.add(self._hndReplaceStart)
        self.end.onReplace.add(self._hndReplaceEnd)
        if self.step is not None:
            self.step.onReplace.add(self._hndReplaceStep)

        if self.loopCode is not None:
            for s in self.loopCode:
                s.onReplace.add(self._hndReplaceLoopCode)            

    def _hndReplaceRunner(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.runner.onReplace.remove(self._hndReplaceRunner)
        self.runner = ev.replacement
        self.runner.onReplace.add(self._hndReplaceRunner)

    def _hndReplaceStart(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.start.onReplace.remove(self._hndReplaceStart)
        self.start = ev.replacement
        self.start.onReplace.add(self._hndReplaceStart)

    def _hndReplaceEnd(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.end.onReplace.remove(self._hndReplaceEnd)
        self.end = ev.replacement
        self.end.onReplace.add(self._hndReplaceEnd)

    def _hndReplaceStep(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.step.onReplace.remove(self._hndReplaceStep)
        self.step = ev.replacement
        self.step.onReplace.add(self._hndReplaceStep)

    def _hndReplaceLoopCode(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.loopCode):
            if ev.eventSource == v:
                self.loopCode[i].onReplace.remove(self._hndReplaceLoopCode)
                self.loopCode[i] = ev.replacement
                self.loopCode[i].onReplace.add(self._hndReplaceLoopCode)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.runner)
        result.append(self.start)
        result.append(self.end)
        if self.step is not None:
            result.append(self.step)
        if self.loopCode is not None:
            for p in self.loopCode:
                result.append(p)            
        return result