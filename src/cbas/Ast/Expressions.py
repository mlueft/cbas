import cbas
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

    ##
    #
    #    
    @staticmethod
    def parseExpression(parser, bp):
        cbas.log("start:parseExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )


        # parse nud
        tokenType   = parser.currentTokenType

        if tokenType not in Lookups.nud:
            raise ValueError("Nud handler expected for token type ({})".format(TokenTypes.toString(tokenType)) )
        
        nudFunction = Lookups.nud[tokenType]

        left = nudFunction(parser)
         
        # This is for linenumber/labels/eof/curlyclose
        if parser.currentTokenType not in Lookups.bp:
            cbas.log("end:parseExpression ... ", "debug" )
            return left

        while  Lookups.bp[parser.currentTokenType] > bp:
            tokenType = parser.currentTokenType
            
            if tokenType not in Lookups.led:
                raise ValueError("Led handler expected for token type ({})".format(TokenTypes.toString(tokenType)) )
            
            ledFunction = Lookups.led[tokenType]
            left = ledFunction(parser,left,Lookups.bp[parser.currentTokenType])

            # This is for linenumber/labels/eof
            if parser.currentTokenType not in Lookups.bp:
                cbas.log("end:parseExpression ... ", "debug" )
                return left
            
        cbas.log("end:parseExpression ... ", "debug" )
        return left


    ## 4
    #  "BLA"
    #  4.1
    #  5.4+e3
    #
    @staticmethod
    def parsePrimaryExpression(parser):
        cbas.log("start:parsePrimaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        type = parser.currentTokenType
        
        if type == TokenTypes.INTEGER:
            token = parser.advance()
            result = PrimaryExpression( token.code, token )
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.FLOAT:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.SIENTIFIC:
            token = parser.advance()
            parts = token.code.lower().split("e")
            base = float(parts[0])
            if len(parts[1]) == 0:
                exp = 0
            else:
                exp = int(parts[1])

            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.STRING:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.BOOLEAN:
            token = parser.advance()
            result = PrimaryExpression( token.code.lower() == 'true', token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
            
        elif type == TokenTypes.IDENTIFIER:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LINENUMBER:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.LINEEND:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COLON:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.SEMICOLON:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COMMA:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LABEL:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type in [ TokenTypes.MUL, TokenTypes.DIV, TokenTypes.ADD, TokenTypes.MINUS ]:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
                
        elif type in [ TokenTypes.EQ, TokenTypes.NEQ, TokenTypes.LESS, TokenTypes.MORE, TokenTypes.LE, TokenTypes.GE, TokenTypes.AND, TokenTypes.OR, TokenTypes.NOT]:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type in parser.config.functions:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type in parser.config.statements:
            token = parser.advance()
            result = PrimaryExpression( token.code, token)
            cbas.log("end:parsePrimaryExpression", "debug" )
            return result
        
        else:
            raise ValueError( "Can't generate primary expression for {}!".format(TokenTypes.toString(type)) )
    

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
        cbas.log("start:parseBinaryExpression ... '{}' ({}) @ {}".format(
            parser.currentToken.code,
            TokenTypes.toString( parser.currentToken.type ),
            parser.pos
        ), "debug" )

        operatorToken = ExpressionParser.parsePrimaryExpression(parser) #parser.advance()
        right = ExpressionParser.parseExpression(parser, bp)

        result = BinaryExpression(
            left,
            operatorToken,
            right
        )

        cbas.log("end:parseBinaryExpression", "debug" )
        return result
   
    ##
    #
    #
    @staticmethod
    def parsePrefixExpression(parser):
        cbas.log("start:parsePrefixExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        operatorToken = ExpressionParser.parsePrimaryExpression(parser) #parser.advance()
        right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = PrefixExpression(
            operatorToken,
            right
        )
        
        cbas.log("end:parsePrefixExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseGroupingExpression(parser):
        cbas.log("start:parseGroupingExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        # We skip (
        parser.expect(TokenTypes.ROUNDOPEN)

        expression = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = GroupingExpression(
            expression
        )

        # We skip )
        parser.expect( TokenTypes.ROUNDCLOSE )

        cbas.log("end:parseGroupingExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseAssignmentExpression(parser, left, bp):
        cbas.log("start:parseAssignmentExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # We skip the "="
        parser.expect(TokenTypes.ASSIGNMENT)

        right = ExpressionParser.parseExpression(parser,bp)
        result = AssignmentExpression(left, right)

        cbas.log("end:parseAssignmentExpression", "debug" )
        return result

    ##
    #  ABS()
    #  ASC()
    #  SYS()
    #  ...
    #
    @staticmethod
    def parseProcedureCallExpression(parser, left,bp):
        cbas.log("start:parseProcedureCallExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        functionName = left #ExpressionParser.parseExpression(parser,BindingPower.DEFAULT) #parser.advance()
        parameters = []

        # we skip the (
        parser.expect(TokenTypes.ROUNDOPEN)

        # we collect all parameters
        ct = parser.currentTokenType
        while ct != TokenTypes.ROUNDCLOSE:
            expr = ExpressionParser.parseExpression(parser,BindingPower.ASSIGNMENT)# BindingPower.DEFAULT)
            parameters.append( expr )
            
            # We skip the parameter seperator
            parser.advance(TokenTypes.COMMA)

            ct = parser.currentTokenType

        # we skip )
        parser.expect(TokenTypes.ROUNDCLOSE)

        result = ProcesureCallExpression(functionName,parameters)
        cbas.log("end:parseProcedureCallExpression", "debug" )
        return result




    ##
    #
    #
    @staticmethod
    def parseFNExpression(parser):
        cbas.log("start:parseFNExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        parameters = []

        # we skip "FN"
        parser.expect(TokenTypes.FN)

        functionName = ExpressionParser.parsePrimaryExpression(parser)
        
        parser.expect(TokenTypes.ROUNDOPEN)
        
        parameters.append( ExpressionParser.parsePrimaryExpression(parser))
        
        parser.expect(TokenTypes.ROUNDCLOSE)
        
        result = FunctionCallExpression(functionName,parameters)
        cbas.log("end:parseFNExpression", "debug" )
        return result




    ##
    #
    #
    @staticmethod
    def parseONExpression(parser):
        cbas.log("start:parseONExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # We skip "on"
        parser.expect(TokenTypes.ON)

        index = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)

        # We expect goto or gosub
        if not parser.currentTokenType in [TokenTypes.GOTO, TokenTypes.GOSUB]:
            raise ValueError("Expecting goto or gosub!")
        
        jumpMethode = ExpressionParser.parsePrimaryExpression(parser)

        lineNumbers = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)
            lineNumbers.append(right)
            
            # we skip ,
            parser.advance(TokenTypes.COMMA)

        result = OnExpression(index,jumpMethode,lineNumbers)
        cbas.log("end:parseGroupingExpression", "debug" )
        return result
    


  


  





##
#
#
class Expression(TreeNode):

    def __init__(self):
        super().__init__()
        self._basicGenerated = False

    def _getNodes(self):
        return []

    
##
#
#
class PrimaryExpression(Expression):
    
    def __init__(self, value = None, token = None):
        super().__init__()
        self.value = value
        self.__token = token
        self._isLeaf = True

    @property
    def token(self):
        return self.__token
    
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
        #cbas.log( "{:<4}:{}tag:'{}' value:'{}' type:{} @{}:{}".format(self.id, " "*level*self.indentation, self.tag, self.value,  TokenTypes.toString(self.__token),self.line,self.pos), "debug" )
        cbas.log( "{:<4}:{} value:'{}' type:{} @{}:{}".format(self.id, " "*level*self.indentation, self.value,  TokenTypes.toString(self.__token),self.line,self.pos), "debug" )

    def __str__(self):
        return "{}".format( self.value)
    
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
        super().__init__()
        self.value = expression
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

    def __init__(self,left, right):
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
class ProcesureCallExpression(Expression):

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
    

 