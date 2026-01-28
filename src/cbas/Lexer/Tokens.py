import cbas.Lexer.TokenTypes
import cbas.Events.EventManager
import cbas.Events.Event

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event

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
class ChainToken(ListToken):

    def __init__(self,code="",line=0,pos=0,type=None):
        super().__init__(code,line,pos,type)
        self.__next = None
        self.__prev = None
        
        self.onInsertedBefore = EventManager()
        self.onInsertedAfter = EventManager()
        self.onRemoved = EventManager()

    @property
    def next(self):
        return self.__next
    
    @next.setter
    def next(self, value):
        if self.__next == value:
            return
        self.__next = value
        
    @property
    def prev(self):
        return self.__prev
    
    @prev.setter
    def prev(self, value):
        if self.__prev == value:
            return
        self.__prev = value
        
    @property
    def first(self):
        result = None
        result = self
        while result:
            result = result.prev
        return result
    
    @property
    def last(self):
        result = None
        result = self
        while result:
            result = result.next
        return result
    
    def _onRemoved(self,ev=None):
        self.onRemoved.provoke( Event(self) )
    
    def _onInsertedBefore(self,ev=None):
        self.onInsertedBefore.provoke( Event(self) )
        
    def _onInsertedAfter(self,ev=None):
        self.onInsertedAfter.provoke( Event(self) )
        

    def insertAfter(self, token):
        
        token.prev = self
        token.next = self.next
        
        if self.next != None:
            self.next.pref = token
        
        self.next = token
        
        self._onInsertedAfter()

        return token
    
    def insertBefore(self, token):
        token.prev = self.prev
        token.next = self

        if self.prev != None:
            self.pref.next = token
        
        self.prev = token
        
        self._onInsertedBefore()

        return self
    
    def remove(self):

        if self.prev != None:
            self.prev.next = self.next

        if self.next != None:
            self.next.prev = self.prev

        self._onRemoved()

        self.prev = None
        self.next = None

    def generateListToken(self):
        result      = ListToken()
        result.line = self.line
        result.pos  = self.pos
        result.code = self.code
        result.type = self.type
        return result
    