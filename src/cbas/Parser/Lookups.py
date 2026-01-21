import cbas.Ast.Statements as STS
import cbas.Ast.Expressions as EXP
import cbas.Lexer.TokenTypes as TT

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
    def registerNud(type, handler):
        Lookups.nud[type] = handler

    @staticmethod
    def registerStatement(type, handler):
        Lookups.bp[type]        = 0 #Lookups.default_bp
        Lookups.statement[type] = handler

    @staticmethod
    def getHandler(type):
        if type == TT.TokenTypes.AND:         return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.OR:          return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.NOT:         return EXP.ExpressionParser.parseBinaryExpression

        if type == TT.TokenTypes.EQ:          return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.NEQ:         return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.LE:          return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.GE:          return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.LESS:        return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.MORE:        return EXP.ExpressionParser.parseBinaryExpression
        
        if type == TT.TokenTypes.ADD:         return EXP.ExpressionParser.parseBinaryExpression
        #if type == TokenTypes.TokenTypes.MINUS:       return Expressions.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.MINUS:       return EXP.ExpressionParser.parsePrefixExpression
        
        if type == TT.TokenTypes.MUL:         return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.DIV:         return EXP.ExpressionParser.parseBinaryExpression
        if type == TT.TokenTypes.EXPONENTIAL: return EXP.ExpressionParser.parseBinaryExpression
        
        if type == TT.TokenTypes.EOF:         return EXP.ExpressionParser.parseEOFExpression
        
        if type == TT.TokenTypes.INTEGER:     return EXP.ExpressionParser.parsePrimaryExpression
        if type == TT.TokenTypes.FLOAT:       return EXP.ExpressionParser.parsePrimaryExpression
        if type == TT.TokenTypes.SIENTIFIC:   return EXP.ExpressionParser.parsePrimaryExpression
        if type == TT.TokenTypes.STRING:      return EXP.ExpressionParser.parsePrimaryExpression
        if type == TT.TokenTypes.IDENTIFIER:  return EXP.ExpressionParser.parsePrimaryExpression
        
        if type == TT.TokenTypes.LINENUMBER:  return EXP.ExpressionParser.parsePrimaryExpression

        if type == TT.TokenTypes.COMMENT:     return EXP.ExpressionParser.parsePrimaryExpression


        raise ValueError("No handler found for {}!".format( type ))
    