import cbas.Events.EventManager
import cbas.Events.TreeEvent
import cbas.DataStructures.TraverseMode

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
EventManager = cbas.Events.EventManager.EventManager
TreeEvent = cbas.Events.TreeEvent.TreeEvent

class TreeNode():
    id = 0

    def __init__(self):
        super().__init__()
        
        self.id = str(TreeNode.id)
        TreeNode.id = TreeNode.id +1

        self._isLeaf = False
        self.indentation = 4

        self.onReplace = EventManager()

    ##
    #
    #
    def __str__(self):
        return "{}".format( type(self))

    ##
    #
    #
    def _getNodes(self):
        return []
    
    ##
    #
    #
    @property
    def isLeaf(self):
        return self._isLeaf
    
    ##
    #
    #
    def debug(self,level=0):
        print( "{:<4}:{}{}".format(self.id, " "*level*self.indentation, self) )
        nodes = self._getNodes()
        for t in nodes:
            t.debug(level+1)

    ##
    #
    #
    def outline(self, handler):

        #
        # Call the optimizer
        #
        handler(self,TraverseMode.OUTLINE)

        # We traverse all leafs first.
        nodes = self._getNodes()
        for t in nodes:
            t.outline(handler)

    ##
    #
    #
    def bottomUp(self, handler):

        # We traverse all leafs first.
        nodes = self._getNodes()
        for t in nodes:
            if not t.isLeaf:
                t.bottomUp(handler)

        # then we traverse all nodes.
        nodes = self._getNodes()
        for t in nodes:
            if t.isLeaf:
                t.bottomUp(handler)

        #
        # Call the optimizer
        #
        handler(self,TraverseMode.BOTTOM_UP)

    ##
    #
    #
    def topDown(self, handler):

        #
        # Call the optimizer
        #
        handler(self,TraverseMode.TOP_DOWN)

        # We traverse all leafs first.
        nodes = self._getNodes()
        for t in nodes:
            if t.isLeaf:
                t.topDown(handler)

        # then we traverse all nodes.
        nodes = self._getNodes()
        for t in nodes:
            if not t.isLeaf:
                t.topDown(handler)

    ##
    #
    #
    def replace(self,replacement):
        event = TreeEvent(self,replacement)
        self.__onReplace(event)

    ##
    #
    #
    def __onReplace(self,event=None):
        if event is None:
            event = TreeEvent(self)
        self.onReplace.provoke(event)