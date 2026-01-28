# distutils: language = c++

## Base class for event objects
#
#
class Event():

    ##
    #
    #
    def __init__(self, eventSource):
        self.__eventSource = eventSource

    ## Returns the event source object.
    #
    # TODO: Should this be source?
    @property
    def eventSource(self):
        return self.__eventSource

    ## Just use the setter if your know what you are doing!
    #
    #
    @eventSource.setter
    def eventSource(self,value):
        self.__eventSource = value
