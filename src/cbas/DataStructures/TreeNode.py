import cbas.DataStructures.LinkedList

LinkedList = cbas.DataStructures.LinkedList.LinkedList

class TreeNode(LinkedList):

    def __init__(self):
        super().__init__()
        self.__parent = None
        self.__firstChild = None

    def bottomUp(self):

        # We traverse all nodes first.
        # So the tree is traversed bottom up.
        # Arithmetic is resolved this way.
        t = self.__first
        while t:
            if not t.isLeaf:
                t.bottomUp()
            t = t.next

        #
        # Call the optimizer
        #

        # then we traverse all leafs.
        t = self.__first
        while t:
            if t.isLeaf:
                t.bottomUp()
            t = t.next

    def topDown(self):

        #
        # Call the optimizer
        #

        # We traverse all leafs first.
        t = self.__first
        while t:
            if t.isLeaf:
                t.topDown()
            t = t.next

        # then we traverse all nodes.
        t = self.__first
        while t:
            if not t.isLeaf:
                t.topDown()
            t = t.next

    def outline(self):

        #
        # Call the optimizer
        #

        # We traverse all leafs first.
        t = self.__first
        while t:
            t.outline()
            t = t.next

    def addNode(self,node):
        if self.__firstChild == None:
            self.__firstChild = node
            last = self.__firstChild.last
            if last != None:
                last.insertAfter(node)
            self.__firstChild.onRemoved.add(self._handleFirstRemoved)
            return
        
        self.__firstChild.onInsertedBefore.add(self._handleFirstInsertedBefore)

    ##
    #
    #
    def _handleFirstRemoved(self,ev):
        node = ev.eventSource
        node.onRemoved.remove(self._handleFirstRemoved)
        node.onInsertedBefore.remove(self._handleFirstInsertedBefore)

        self.__first = node.next
        self.__first.onRemoved.add(self._handleFirstRemoved)
        self.__first.onInsertedBefore.add(self._handleFirstInsertedBefore)

    ##
    #
    #
    def _handleFirstInsertedBefore(self, ev):
        if ev.eventSource == self.__first:
            self.__first.onRemoved.remove(self._handleFirstRemoved)
            self.__first.onInsertedBefore.remove(self._handleFirstInsertedBefore)

            self.__first = self.__first.prev
            self.__first.onRemoved.add(self._handleFirstRemoved)
            self.__first.onInsertedBefore.add(self._handleFirstInsertedBefore)

    @property
    def parent(self):
        return self.__parent
    
    @parent.setter
    def parent(self, value):
        if self.__parent == value:
            return
        self.__parent = value
    
    @property
    def isLeaf(self):
        return self.__firstChild