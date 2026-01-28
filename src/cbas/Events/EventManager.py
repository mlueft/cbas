# distutils: language = c++

##
#
#
class EventManager():

    ##
    #
    #
    def __init__(self):
        self.__handlers =  []

    ##
    #
    #
    def __del__(self):
        self.__handlers.clear()

    ## Adds a function handler.
    #
    #
    def add(self, handler):
        self.__handlers.append(handler)

    ## Removes a function handler.
    #
    #
    def remove(self, handler):
        if handler not in self.__handlers:
            return
        self.__handlers.remove(handler)

    ## Checks if a handler has been added.
    #
    #
    def has(self,handler):
        return handler in self.__handlers

    ## Calls all added handlers.
    #
    # TODO: provoke and stopPropergation? :-/
    def provoke(self, event):
        for handler in self.__handlers:
            handler(event)
