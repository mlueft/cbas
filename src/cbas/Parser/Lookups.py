import cbas.Lexer.TokenTypes

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

class Lookups():
    bp          = {}
    nud         = {}
    led         = {}
    statement   = {}
    default_bp  = 0
    handler_led = {}
    handler_nud = {}

    @staticmethod
    def reset():
        Lookups.bp          = {}
        Lookups.nud         = {}
        Lookups.led         = {}
        Lookups.statement   = {}
        Lookups.default_bp  = 0
        Lookups.handler_led = {}
        
    @staticmethod
    def registerLed(type, bp, handler):
        Lookups.bp[type]  = bp
        Lookups.led[type] = handler

    @staticmethod
    def registerNud(type, handler):
        Lookups.nud[type] = handler

    @staticmethod
    def registerStatement(type, handler):
        Lookups.bp[type]        = Lookups.default_bp
        Lookups.statement[type] = handler
