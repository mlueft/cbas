import cbas.Ast.Expressions
import cbas.Parser.BindingPower
import cbas.Parser.Lookups
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList
import cbas.DataStructures.TreeNode

Lookups = cbas.Parser.Lookups.Lookups
BindingPower = cbas.Parser.BindingPower.BindingPower
Lookups = cbas.Parser.Lookups.Lookups
ExpressionParser = cbas.Ast.Expressions.ExpressionParser
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event
LinkedList = cbas.DataStructures.LinkedList.LinkedList
TreeNode = cbas.DataStructures.TreeNode.TreeNode

class StatementParser():
    
    ##
    #
    #
    @staticmethod
    def registerHandlers():
        pass
        
    ##
    #
    #
    @staticmethod
    def parseStatement(parser):
        parser.log("start:parseStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        tokenType = parser.currentTokenType

        if tokenType in Lookups.statement:
            statementFunction = Lookups.Lookups.statement[tokenType]
            parser.log("end:parseStatement", "debug" )
            return statementFunction()

        expression = ExpressionParser.parseExpression( parser, 0)
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

        expression = ExpressionParser.parseExpression( parser, 0)

        parser.log("end:parseCommentStatement", "debug" )
        return CommentStatement(token.code)
    
        
##
#
#
class Statement(TreeNode):
    
    def __init__(self):
        super().__init__()

##
#
#
class BlockStatement(Statement):

    def __init__(self, first):
        super().__init__()
        self.addNode(first)
    
    def debug(self, indentation=0):
        print((" "*indentation)+"Blockstatement:")
        t = self.first
        while t:
            t.debug(indentation+4)
            t = t.next

##
#
#    
class ExpressionStatement(Statement):

    def __init__(self, expression):
        super().__init__()
        self.addNode(expression)
        
    def debug(self, indentation=0):
        print ((" "*indentation)+"ExpressionStatement:")
        self.expression.debug(indentation+4)

##
#
#
class CommentStatement(Statement):

    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def debug(self, indentation=0):
        print ((" "*indentation)+"CommentStatement:")
        self.value.debug(indentation+4)