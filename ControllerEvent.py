from Event import Event
from main import send as ss

class ControllerEvent(Event):
    def __init__(self, send:ss):
        super.__init__(send)
        self.requests = {'info':self.infoGet}
    def infoGet(self):
        pass