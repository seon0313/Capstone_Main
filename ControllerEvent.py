from Event import Event

class ControllerEvent(Event):
    def __init__(self, sql):
        super().__init__(sql)
        self.requests['getPID'] = self.getPID
        self.requests['getOffset'] = self.getOffset
        self.requests['addOffset'] = self.addOffset
        self.requests['getPIDs'] = self.getPIDs
        self.requests['getOffsets'] = self.getOffsets
        self.requests['setOffset'] = self.setOffset
        self.requests['setPID'] = self.setPID
        self.requests['delPID'] = self.delPID
        self.requests['getServo'] = self.getServo
        self.leftAngle = 0
        self.rightAngle = 0

    def firstRun(self):
        return self.getPID('',())
    def getPID(self, device: str, *args: list[str]):
        pid = self.sql('select p,i,d from pids where id=(select id from pid)')[0]
        try:
            if args[0] == 'non':
                return pid
        except:
            pass
        from json import dumps
        return dumps({'request': self.getName(),'type':'getPID', 'p': pid[0], 'i': pid[1], 'd': pid[2]})
    def getPIDs(self, device: str, *args: list[str]):
        from json import dumps
        pids = self.sql('select id, p, i, d from pids')
        return dumps({'request': self.getName(), 'type':'getPIDs','data':pids})

    def addPID(self, device: str, *args: list[str]):
        from json import dumps
        from time import time
        from uuid import uuid4
        import sqlite3
        args = args[0]
        p = args.get('p')
        i = args.get('i')
        d = args.get('d')
        if p is None or i is None or d is None:
            return dumps({'request': 'ERROR', 'type': 'addOffset', 'msg': 'missing'})
        m = f'insert into pids values ("{uuid4().hex}", {p}, {i}, {d}, {time()})'
        print(m)
        con = sqlite3.connect('./data.db', isolation_level=None)
        cur = con.cursor()
        cur.execute(m)
        con.commit()
        cur.close()
        con.close()


    def getServo(self, device: str, *args: list[str]):
        from json import dumps
        msg = {
            'request': self.getName(),
            'type': 'getServo',
            'left': self.leftAngle,
            'right': self.rightAngle,
            'Loffset': 0,
            'Roffset': 0,
        }
        return dumps(msg)

    def addOffset(self, device: str, *args: list):
        from json import dumps
        from time import time
        from uuid import uuid4
        import sqlite3
        args = args[0]
        l = args.get('Loffset')
        r = args.get('Roffset')
        if l is None or r is None:
            return dumps({'request':'ERROR', 'type':'addOffset', 'msg':'missing'})
        m = f'insert into offsets values ("{uuid4().hex}", {l}, {r}, {time()})'
        print(m)
        con = sqlite3.connect('./data.db', isolation_level=None)
        cur = con.cursor()
        cur.execute(m)
        con.commit()
        cur.close()
        con.close()


    def getOffset(self, device: str, *args: list[str]):
        l,r = self.sql('select left, right from offsets where id=(select id from offset)')[0]
        print(l,r)
        try:
            if args[0] == 'non':
                return l, r
        except: pass
        from json import dumps
        return dumps({'request':self.getName(), 'type':'getOffset', 'l':l,'r':r})

    def getOffsets(self, device: str, *args: list[str]):
        from json import dumps
        d = self.sql('select id, left, right from offsets')
        print('!', d)
        return dumps({'request':self.getName(), 'type':'getOffsets', 'data':d})

    def setOffset(self, device: str, *args: list[str]):
        from json import dumps
        import sqlite3
        id = args[0]
        r = self.sql(f'select id from offsets where id="{id}"')
        if r is None or r == () or r[0] is None:
            return dumps({'request':'ERROR', 'type':'setOffset', 'msg':'missing'})
        con = sqlite3.connect('./data.db', isolation_level=None)
        cur = con.cursor()
        msg = cur.execute(f'update offset set id="{id}"')
        con.commit()
        cur.close()
        con.close()

        return dumps({'request':self.getName(), 'type': 'changeOffset', 'data':self.getOffset('','non')})
    def setPID(self, device: str, *args: list[str]):
        from json import dumps
        import sqlite3
        id = args[0]
        r = self.sql(f'select id from pids where id="{id}"')
        if r is None or r == () or r[0] is None:
            return dumps({'request':'ERROR', 'type':'setOffset', 'msg':'missing'})
        con = sqlite3.connect('./data.db', isolation_level=None)
        cur = con.cursor()
        msg = cur.execute(f'update pid set id="{id}"')
        con.commit()
        cur.close()
        con.close()
        pid = self.getPID('','non')
        return dumps({'request':self.getName(), 'type': 'getPID', 'p': pid[0], 'i':pid[1], 'd':pid[2]})

    def delPID(self, device: str, *args: list[str]):
        from json import dumps
        import sqlite3
        id = args[0]
        if self.sql('select id from pid')[0][0] == id: return None
        print(id)
        con = sqlite3.connect('./data.db', isolation_level=None)
        cur = con.cursor()
        msg = cur.execute(f'delete from pids where id="{id}"')
        con.commit()
        cur.close()
        con.close()