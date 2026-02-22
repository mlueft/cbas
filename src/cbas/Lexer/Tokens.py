import cbas.Lexer.TokenTypes
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event
LinkedList = cbas.DataStructures.LinkedList.LinkedList

##
#
#
class ListToken():

    def __init__(self,code="",line=0,pos=0,type=None):
        self.line = line
        self.pos  = pos
        self.code = code
        self.type = type

    def __str__(self):
        return "{}:{} - '{}' '{}'".format( self.line, self.pos, self.code, TokenTypes.getString(self.type) )

    def __repr__(self):
        if self.isString:
            return "'{}'".format(self.code)
        else:
            return "{}".format(self.code)

##
#
#
class ChainToken(ListToken,LinkedList):

    def __init__(self,code="",line=0,pos=0,type=None):
        ListToken.__init__(self,code,line,pos,type)
        LinkedList.__init__(self)
        
    def generateListToken(self):
        result      = ListToken()
        result.line = self.line
        result.pos  = self.pos
        result.code = self.code
        result.type = self.type
        return result
    
