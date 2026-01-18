
class ConfigToken():
    def __init__(self, type="", expression="", order=0, name=None, description=None ):
        self.type        = type
        self.expression  = expression
        self.order       = order
        self.name        = name
        self.description = description
        
    def __str__(self):
        return "{} ({}) - {}".format(self.order,self.expression,self.type)
