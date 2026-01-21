import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

class Lookups():
    bp         = {}
    nud        = {}
    led        = {}
    statement  = {}
    default_bp = 0
    handler    = {}

    @staticmethod
    def reset():
        Lookups.bp        = {}
        Lookups.nud       = {}
        Lookups.led       = {}
        Lookups.statement = {}
        Lookups.default_bp = 0
        Lookups.handler    = {}
        
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
    def registerHandler(type, handler):
        print(type)
        Lookups.handler[type] = handler

    @staticmethod
    def getHandler(type):
        Lookups.registerHandlers()
        return Lookups.handler[type]
        #raise ValueError("No handler found for {}!".format( type ))

    __initialized = False

    ##
    #
    #
    @staticmethod
    def registerHandlers():
        import cbas.Ast.Expressions
        #import cbas.Ast.Statements

        if Lookups.__initialized:
            return
        
        Lookups.__initialized = True
        
        Lookups.registerHandler( TokenTypes.AND         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.OR          , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.NOT         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        
        Lookups.registerHandler( TokenTypes.EQ          , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.NEQ         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.LE          , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.GE          , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.LESS        , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.MORE        , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        
        Lookups.registerHandler( TokenTypes.ADD         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.MINUS       , cbas.Ast.Expressions.ExpressionParser.parsePrefixExpression )
        
        Lookups.registerHandler( TokenTypes.MUL         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.DIV         , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        
        Lookups.registerHandler( TokenTypes.EXPONENTIAL , cbas.Ast.Expressions.ExpressionParser.parseBinaryExpression )
        Lookups.registerHandler( TokenTypes.EOF         , cbas.Ast.Expressions.ExpressionParser.parseEOFExpression )
        
        Lookups.registerHandler( TokenTypes.INTEGER     , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        Lookups.registerHandler( TokenTypes.FLOAT       , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        Lookups.registerHandler( TokenTypes.SIENTIFIC   , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        Lookups.registerHandler( TokenTypes.STRING      , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        Lookups.registerHandler( TokenTypes.IDENTIFIER  , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        
        Lookups.registerHandler( TokenTypes.LINENUMBER  , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
        Lookups.registerHandler( TokenTypes.COMMENT     , cbas.Ast.Expressions.ExpressionParser.parsePrimaryExpression )
    