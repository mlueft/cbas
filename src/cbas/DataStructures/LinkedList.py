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
            print(result)
            result = result.next
        return result

    @property
    def length(self):
        i = 1
        f = self.first
        while f:
            i = i +1
            f = f.next
        return i

    ##
    #
    #
    def insertAfter(self,node):
        node.prev = self
        node.next = self.next

        if self.next is not None:
            self.next.prev = node

        self.next = node
        self._onInsertedAfter()

    ##
    #
    #
    def insertBefore(self, node):
        node.next = self
        node.pref = self.prev

        if self.prev is not None:
            self.prev.next = node

        self.pref = node
        self._onInsertedBefore()

    ##
    #
    #
    def remove(self):
        if self.prev is not None:
            self.prev.next = self.next

        if self.next is not None:
            self.next.prev = self.prev

        self._onRemoved()

    def _onRemoved(self,ev=None):
        self.onRemoved.provoke( Event(self) )
    
    def _onInsertedBefore(self,ev=None):
        self.onInsertedBefore.provoke( Event(self) )
        
    def _onInsertedAfter(self,ev=None):
        self.onInsertedAfter.provoke( Event(self) )


