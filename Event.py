from main import send as ss
from main import Type

class Event:
    def __init__(self, send:ss):
        self.type = Type.HelloWorld
        self.requests = {'HelloWorld':self.helloWorld}
        self.send = send
    def helloWorld(self, *args) -> str:
        return f'HelloWorld, args: {args}'

    def run(self, request, *args):
        v = self.requests.get(request)
        if v:
            return v(*args)

        return None