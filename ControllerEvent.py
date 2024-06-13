from Event import Event

class ControllerEvent(Event):
    def __init__(self):
        super().__init__()
        self.requests = {'info': self.infoGet}
    def infoGet(self):
        pass