import cbas.Lexer.TokenTypes as TokenTypes
import cbas.Parser.Lookups as Lookups
import cbas.Parser.BindingPower as BindingPower

class ExpressionParser():
    
    ##
    #
    #
    @staticmethod
    def parsePrimaryExpression(parser):
        parser.log("start:parsePrimaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        type = parser.currentTokenType
        
        if type == TokenTypes.NUMBER:
            result = NumberExpression(float(parser.advance().code))
            parser.log("end:parsePrimaryExpression", "debug" )
            return result
        
        elif type == TokenTypes.STRING:
            result = StringExpression(parser.advance().code)
            parser.log("end:parsePrimaryExpression", "debug" )
            
        elif type == TokenTypes.IDENTIFIER:
            result = SymbolExpression(parser.advance().code)
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
        
        if tokenType not in Lookups.Lookups.nud:
            raise ValueError("Nud handler expected for token type ({})".format(TokenTypes.getString(tokenType)) )
        
        nudFunction = Lookups.Lookups.nud[tokenType]

        left = nudFunction(parser)
         
        while Lookups.Lookups.bp[parser.currentTokenType] > bp and parser.hasTokens:
            tokenType = parser.currentTokenType
            if tokenType not in Lookups.Lookups.led:
                raise ValueError("Led handler expected for token type ({})".format(TokenTypes.getString(tokenType)) )
            ledFunction = Lookups.Lookups.led[tokenType]
            left = ledFunction(parser,left,bp)
            parser.log("left =  '{}'".format(parser.currentToken.code) )

        parser.log("end:parseExpression ... ", "debug" )
        return left
    
    ##
    #
    #
    @staticmethod
    def parseBinaryExpression(parser, left, bp ):
        parser.log("start:parseBinaryExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        operatorToken = parser.advance()
        right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        result = BinaryExpression(
            left,
            operatorToken.code,
            right
        )
        parser.log("end:parseBinaryExpression", "debug" )
        return result
   


class Expression():
    
    def __init__(self, value):
        self.value = value
        
class NumberExpression(Expression):
    
    def __init__(self, value):
        super().__init__(value)

    def debug(self, indentation=0):
        print ((" "*indentation)+"Number({})".format( str(self.value)))
    
class StringExpression(Expression):
    
    def __init__(self, value):
        super().__init__(value)
    
    def debug(self, indentation=0):
        print ((" "*indentation)+"String({})".format( str(self.value)))
    
class SymbolExpression(Expression):
    
    def __init__(self, value):
        super().__init__(value)

    def debug(self, indentation=0):
        print ((" "*indentation)+"Symbol({})".format( str(self.value)))
    
class BinaryExpression():
    
    def __init__(self,left,operator,right):
        super().__init__()
        self.left     = left
        self.operator = operator
        self.right    = right

    def debug(self, indentation=0):
        print ((" "*indentation)+" => {}".format(self.operator))
        
        print ((" "*indentation)+"left:")
        self.left.debug(indentation+4)
        
        
        print ((" "*indentation)+"right:")
        self.right.debug(indentation+4)
        
        return "left:(left)operator:(operator)right:(right)".format( left=self.left, operator=self.operator, right=self.right )