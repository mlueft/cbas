import cbas.Ast.Statements as Statements
import cbas.Ast.Expressions as Expressions
import cbas.Lexer.TokenTypes as TokenTypes

#from cbas.Lexer ..Lexer import TokenTypes
from ..Parser import BindingPower

#from cbas.Ast.Expressions import Expression

class Lookups():
    bp         = {}
    nud        = {}
    led        = {}
    statement  = {}
    default_bp = 0

    @staticmethod
    def reset():
        Lookups.bp        = {}
        Lookups.nud       = {}
        Lookups.led       = {}
        Lookups.statement = {}
        Lookups.default_bp = 0
        
    @staticmethod
    def registerLed(type, bp, handler):
        Lookups.bp[type]  = bp
        Lookups.led[type] = handler

    @staticmethod
    def registerNud(type, bp, handler):
        Lookups.bp[type]  = bp
        Lookups.nud[type] = handler

    @staticmethod
    def registerStatement(type, handler):
        Lookups.bp[type]        = 0 #Lookups.default_bp
        Lookups.statement[type] = handler

    @staticmethod
    def getHandler(type):
        if type == TokenTypes.AND:         return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.OR:          return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.NOT:         return Expressions.ExpressionParser.parseBinaryExpression 

        if type == TokenTypes.EQ:          return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.NEQ:         return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.LE:          return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.GE:          return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.LESS:        return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.MORE:        return Expressions.ExpressionParser.parseBinaryExpression 
        
        if type == TokenTypes.ADD:         return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.MINUS:       return Expressions.ExpressionParser.parseBinaryExpression 
        
        if type == TokenTypes.MUL:         return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.DIV:         return Expressions.ExpressionParser.parseBinaryExpression 
        if type == TokenTypes.EXPONENTIAL: return Expressions.ExpressionParser.parseBinaryExpression 
        
        if type == TokenTypes.EOF:         return Expressions.ExpressionParser.parseBinaryExpression 
        
        if type == TokenTypes.NUMBER:      return Expressions.ExpressionParser.parsePrimaryExpression 
        if type == TokenTypes.STRING:      return Expressions.ExpressionParser.parsePrimaryExpression 
        if type == TokenTypes.IDENTIFIER:  return Expressions.ExpressionParser.parsePrimaryExpression 
        
        if type == TokenTypes.LINENUMBER:  return Expressions.ExpressionParser.parsePrimaryExpression 

        if type == TokenTypes.COMMENT:     return Statements.StatementParser.parseCommentStatement 
        if type == TokenTypes.LINENUMMER:  return Statements.StatementParser.parseCommentStatement 

        raise ValueError("No handler found for {}!".format( type ))
    