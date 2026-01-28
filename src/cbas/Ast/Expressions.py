import cbas.Lexer.TokenTypes
import cbas.Parser.Lookups
import cbas.Parser.BindingPower
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
Lookups = cbas.Parser.Lookups.Lookups
BindingPower = cbas.Parser.BindingPower.BindingPower
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event
LinkedList = cbas.DataStructures.LinkedList.LinkedList

class ExpressionParser():
    
    ##
    #
    #
    @staticmethod
    def parsePrimaryExpression(parser):
        parser.log("start:parsePrimaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )

        type = parser.currentTokenType
        
        if type == TokenTypes.INTEGER:
            result = NumberExpression(int(parser.advance().code))
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.FLOAT:
            result = NumberExpression(float(parser.advance().code))
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.SIENTIFIC:
            result = StringExpression(parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.STRING:
            result = StringExpression(parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            
        elif type == TokenTypes.IDENTIFIER:
            result = SymbolExpression(parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result

        elif type == TokenTypes.LINENUMBER:
            result = LabelExpression(parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.COMMENT:
            result = CommentExpression(parser.advance().code)
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

        while parser.hasTokens and Lookups.bp[parser.currentTokenType] > bp:
            tokenType = parser.currentTokenType
            if tokenType not in Lookups.led:
                raise ValueError("Led handler expected for token type ({})".format(TokenTypes.getString(tokenType)) )
            ledFunction = Lookups.led[tokenType]
            left = ledFunction(parser,left,Lookups.bp[parser.currentTokenType])
            parser.log("left =  '{}'".format(parser.currentToken.code) )

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
        right = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)

        result = BinaryExpression(
            left,
            operatorToken.code,
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
            operatorToken,
            right
        )
        parser.log("end:parsePrefixExpression", "debug" )
        return result



##
#
#
class Expression(LinkedList):

    def __init__(self):
        super().__init__()


##
#
#
class NumberExpression(Expression):
    
    def __init__(self, value):
        super().__init__()
        self.value = value

    def debug(self, indentation=0):
        print ((" "*indentation)+"Number({})".format( str(self.value)))

##
#
#   
class StringExpression(Expression):
    
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def debug(self, indentation=0):
        print ((" "*indentation)+"String({})".format( str(self.value)))

##
# 
#    
class SymbolExpression(Expression):
    
    def __init__(self, value):
        super().__init__()
        self.value = value

    def debug(self, indentation=0):
        print ((" "*indentation)+"Symbol({})".format( str(self.value)))

##
# 
#   
class LabelExpression(Expression):
    
    def __init__(self, value):
        super().__init__()
        self.value = value

    def debug(self, indentation=0):
        print ((" "*indentation)+"Label({})".format( str(self.value)))

##
#
#
class CommentExpression(Expression):
    
    def __init__(self, value):
        super().__init__()
        # if the value starts with 'REM' we remove it
        if value.upper().startswith("REM"):
            value = value[3:].strip()
        
        self.value = value

    def debug(self, indentation=0):
        print ((" "*indentation)+"Comment({})".format( str(self.value)))

##
#
# 
class BinaryExpression(Expression):

    def __init__(self,left,operator,right):
        super().__init__()
        self.left     = left
        self.operator = operator
        self.right    = right

    def debug(self, indentation=0):
        print ((" "*indentation)+" => {}".format(self.operator))
        
        print ((" "*indentation)+"left:")
        if self.left is not None:
            self.left.debug(indentation+4)
        else:
            print ((" "*(indentation+4))+"None!!!!!!!")
        
        print ((" "*indentation)+"right:")
        if self.right is not None:
            self.right.debug(indentation+4)
        else:
            print ((" "*(indentation+4))+"None!!!!!!!")

        return "left:(left)operator:(operator)right:(right)".format( left=self.left, operator=self.operator, right=self.right )

##
#
#
class PrefixExpression(Expression):

    def __init__(self, operator, right):
        super().__init__()
        self.operator = operator
        self.right    = right

    def debug(self, indentation=0):
        print ((" "*indentation)+" => {}".format(self.operator))
        
        print ((" "*indentation)+"right:")
        self.right.debug(indentation+4)

        return "operator:(operator)right:(right)".format( operator=self.operator, right=self.right )
