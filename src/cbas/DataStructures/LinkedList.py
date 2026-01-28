import cbas.Events.EventManager
import cbas.Events.Event

EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event

class LinkedList():

    def __init__(self):
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
        result = self
        while result:
            result = result.prev
        return result
    
    @property
    def last(self):
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
