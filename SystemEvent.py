from Event import Event


class SystemEvent(Event):
    def __init__(self, sql, module_list):
        super().__init__(sql)
        self.module_list: dict = module_list
        self.requests['module'] = self.moduleList

    def moduleList(self, device: str, *args: list[str]):
        import numpy as np
        import json
        keys = np.array(list(self.module_list.keys())).reshape((-1, 1))
        values = np.array(list(self.module_list.values())).reshape((-1, 1))
        r = np.concatenate((keys, values), axis=1).tolist()
        for i in r:
            i[1] = i[1].getName()
        msg = {'request': 'SystemEvent', 'type': 'moduleList', 'data': r}
        return json.dumps(msg)
