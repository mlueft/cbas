import cbas.Events.Event

Event = cbas.Events.Event.Event

class TreeEvent(Event):

    def __init__(self,eventSource, replacement=None):
        super().__init__(eventSource)
        self.replacement = replacement

