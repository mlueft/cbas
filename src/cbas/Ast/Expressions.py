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
            result = PrimaryExpression( "int", int(parser.advance().code) )
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.FLOAT:
            result = PrimaryExpression( "float", float(parser.advance().code))
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.SIENTIFIC:
            result = PrimaryExpression( "string", parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.STRING:
            result = PrimaryExpression( "string", parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.BOOLEAN:
            literal = parser.advance().code
            result = PrimaryExpression( "boolean", literal.lower() == 'true')
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
            
        elif type == TokenTypes.IDENTIFIER:
            result = PrimaryExpression( "symbol", parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LINENUMBER:
            result = PrimaryExpression( "linenumber", parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COMMENT:
            result = PrimaryExpression( "comment", parser.advance().code)
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
    def parseEOFExpression(parser, left, bp ):
        pass
        
    ##
    #
    #
    @staticmethod
    def parseBinaryExpression(parser, left, bp ):
        parser.log("start:parseBinaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        operatorToken = parser.advance()
        right = ExpressionParser.parseExpression(parser, bp)

        result = BinaryExpression(
            left,
            PrimaryExpression("op",operatorToken.code),
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

        operatorToken = parser.advance()
        right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = PrefixExpression(
            PrimaryExpression("op", operatorToken.code),
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
    
    def __init__(self, tag=None, value = None):
        super().__init__(value)
        self.tag = tag
        self._isLeaf = True

    def _getNodes(self):
        return []

    def _debug(self,level=0):
        print( "{:<4}:{}{} {}".format(self.id, " "*level*self.indentation, self.tag, self.value) )

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
