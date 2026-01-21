import cbas.Ast.Expressions
import cbas.Parser.BindingPower
import cbas.Parser.Lookups

class StatementParser():
    
    ##
    #
    #
    @staticmethod
    def parseStatement(parser):
        parser.log("start:parseStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        tokenType = parser.currentTokenType

        if tokenType in cbas.Parser.Lookups.statement:
            statementFunction = cbas.Parser.Lookups.statement[tokenType]
            parser.log("end:parseStatement", "debug" )
            return statementFunction()

        expression = cbas.Ast.Expressions.ExpressionParser.parseExpression( parser, 0)
        #p.expect(TokenTypes.SEMICOLON)

        parser.log("end:parseStatement", "debug" )
        return ExpressionStatement(expression)
        
    ##
    #
    #
    @staticmethod
    def parseCommentStatement(parser):
        parser.log("start:parseCommentStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        token = parser.currentToken

        expression = cbas.Ast.Expressions.ExpressionParser.parseExpression( parser, 0)

        parser.log("end:parseCommentStatement", "debug" )
        return CommentStatement(token.code)
    
        

class Statement():
    pass

class BlockStatement(Statement):

    def __init__(self, body):
        super().__init__()
        self.body = body

    def debug(self, indentation=0):
        print((" "*indentation)+"Blockstatement:")
        for b in self.body:
            b.debug(indentation+4)
    
class ExpressionStatement(Statement):

    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        
    def debug(self, indentation=0):
        print ((" "*indentation)+"ExpressionStatement:")
        self.expression.debug(indentation+4)

class CommentStatement(Statement):

    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def debug(self, indentation=0):
        print ((" "*indentation)+"CommentStatement:")
        self.value.debug(indentation+4)