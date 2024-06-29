class Event:
    def __init__(self, sql):
        self.requests = {'HelloWorld': self.helloWorld}
        self.sql = sql
        print(f'"{self.getName()}" Event Loaded')

    def getName(self) -> str:
        return self.__class__.__name__

    def helloWorld(self, device, *args) -> str:
        return f'HelloWorld, device: {device} | args: {args}'

    def firstRun(self):
        return None

    def run(self, device, request,target, *args):
        v = self.requests.get(request)
        if v:
            if target==None:
                return v(device, *args)
            else: return (v(device, *args), target)

        return None
