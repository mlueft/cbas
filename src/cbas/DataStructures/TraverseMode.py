
class TraverseMode():

    BOTTOM_UP = 0
    TOP_DOWN = 1
    OUTLINE = 2

    
    __matchTable = {
        "bottomUp":   BOTTOM_UP,
        "topDown":   TOP_DOWN,
        "outline":   OUTLINE,
    }
    
    @staticmethod
    def toType(value):
        if value in TraverseMode.__matchTable:
            return TraverseMode.__matchTable[value]
        raise ValueError("TraverseMode '{}' not recognized!".format(value))

    @staticmethod
    def toString(value):
        for e in TraverseMode.__matchTable:
            if TraverseMode.__matchTable[e] == value:
                return e
        #raise ValueError("TraverseMode'{}' not recognized!".format(value))