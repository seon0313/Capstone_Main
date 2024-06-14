class Event:
    def __init__(self):
        self.requests = {'HelloWorld': self.helloWorld}
        print(f'"{self.__class__.__name__}" Event Loaded')

    def helloWorld(self, device, *args) -> str:
        return f'HelloWorld, device: {device} | args: {args}'

    def run(self, device, request, *args):
        print(device, request, args)
        v = self.requests.get(request)
        if v:
            return v(device, *args)

        return None
