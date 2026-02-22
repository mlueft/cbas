
class ConfigToken():
    def __init__(self,handler):
        self.handler      = handler

    def __str__(self):
        return "{}{}{}".format(self.bindingpower,self.type,self.category)