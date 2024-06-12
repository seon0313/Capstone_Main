import asyncio
import time

import websockets
import sqlite3
import uuid
import threading
import time
import json
import hashlib

con = sqlite3.connect('./data.db')

print(uuid.uuid4().hex)
print(hashlib.sha256(b'seon1234SEORO_By_Seon').hexdigest())

cur = con.cursor()
cur.execute('create table if not exists pids (id real, p real, i real, d real, time real)')
cur.execute('create table if not exists pid (id real)')
cur.close()
con.close()

server_cool = 1 / 12

events = {}


class Type:
    HelloWorld: int = 0
    Control: int = 1
    Display: int = 2

def send(target, msg):
    pass


def setEvent(name: str, func) -> bool:
    global events
    try:
        events[name] = func
        return True
    except Exception as e:
        print(e)
        return False


def getData(msg: str, all=False):
    con = sqlite3.connect('./data.db')
    cur = con.cursor()
    data = None
    try:
        if all:
            data = cur.execute(msg).fetchall()
        elif type(all) == int:
            data = cur.execute(msg).fetchmany(all)
        else:
            data = cur.execute(msg).fetchall()
    except Exception as e:
        print('SQL ERROR :', e)
    cur.close()
    con.close()
    if data == None or len(data) <= 0: return None
    return data


async def client(websocket, path):
    user = None
    print('Connected : ', path)
    msg = {'result': 'login', 'type': 'string', 'data': 'need'}
    await websocket.send(json.dumps(msg))
    while True:
        try:
            data = await websocket.recv()
            data = json.loads(data)
            request = data['request']
            type = data['type']

            eventVar: str = events[type].run(request, *data['arg'])
            if eventVar != None:
                await websocket.send(json.dumps(eventVar))
        except Exception as e:
            print('Disconnect - Error', e)
            break


if __name__ == '__main__':

    from ControllerEvent import ControllerEvent

    setEvent('controller', ControllerEvent)

    start_server = websockets.serve(client, "0.0.0.0", 9875)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
