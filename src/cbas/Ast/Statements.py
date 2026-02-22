import cbas.Ast.Expressions
import cbas.Parser.BindingPower
import cbas.Parser.Lookups
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList
import cbas.DataStructures.TreeNode

Lookups = cbas.Parser.Lookups.Lookups
BindingPower = cbas.Parser.BindingPower.BindingPower
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

        result = expression

        parser.log("end:parseStatement", "debug" )
        return result
        
        
















##
#
#
class Statement(TreeNode):
    
    def __init__(self, value = None):
        super().__init__()
        self.value = value


##
# {
#  statement0
#  statement1
#  ...
# }
#
class BlockStatement(Statement):

    def __init__(self, statements):
        super().__init__()
        self.statements = statements
        for s in self.statements:
            s.onReplace.add(self._hndReplaceLeft)

    def _hndReplaceLeft(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.statements):
            if ev.eventSource == v:
                self.statements[i].onReplace.remove(self._hndReplaceLeft)
                self.statements[i] = ev.replacement
                self.statements[i].onReplace.add(self._hndReplaceLeft)
                return


    def _getNodes(self):
        return self.statements


## expression 
# 4+6
# 4-6
# ...
class ExpressionStatement(Statement):

    def __init__(self, statement):
        super().__init__()
        self.statement = statement
        
        self.statement.onReplace.add(self._hndReplace)

    def _hndReplace(self,ev):
        #print("ExpressionStatement::_hndReplace")
        self.statement.onReplace.remove(self._hndReplace)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplace)

    def _getNodes(self):
        return self.statement
