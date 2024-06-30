class Event:
    def __init__(self, sql):
        self.requests = {'HelloWorld': self.helloWorld}
        self.sql = sql
        print(f'"{self.getName()}" Event Loaded')

    def getName(self) -> str:
        return self.__class__.__name__

    def helloWorld(self, device:str, *args: list[str]) -> str:
        return f'HelloWorld, device: {device} | args: {args}'

    def firstRun(self):
        return None

    def run(self, device: str, request: str, target: str, *args):
        v = self.requests.get(request)
        if v:
            if type(v) == type(tuple): v, target = v
            if target is None:
                return v(device, *args)
            else: return (v(device, *args), target)

        return None
