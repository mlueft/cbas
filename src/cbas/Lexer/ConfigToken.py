
class ConfigToken():
    def __init__(self, type="", expression="", order=0):
        self.type        = type
        self.expression  = expression
        self.order       = order
        
    def __str__(self):
        return "{} ({}) - {}".format(self.order,self.expression,self.type)
