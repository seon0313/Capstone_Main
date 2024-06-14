import asyncio
import websockets
import sqlite3
import uuid
import threading
import time
import json
import hashlib

con = sqlite3.connect('./data.db')

cur = con.cursor()
cur.execute('create table if not exists pids (id real, p real, i real, d real, time real)')
cur.execute('create table if not exists pid (id real)')
cur.close()
con.close()

server_cool = 1 / 12

events = {}
connection = {}


def setEvent(name: str, func) -> bool:
    global events
    try:
        events[name] = func
        return True
    except Exception as e:
        print('setEvent Error:\t', e)
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
    print('Connected : ', path)
    target = None
    while True:
        try:
            data = await websocket.recv()
            data: dict = json.loads(data)
            device = data['device']
            request = data['device']
            if data.get('target') != None: request = data['target']
            type_ = data['type']

            if target == None:
                target = request
                connection[target] = websocket

            eventVar: str = events[request].run(device, type_, *data['arg'])
            if eventVar != None:
                sendTarget = None
                msg = eventVar
                if type(eventVar) == tuple:
                    v = connection.get(eventVar[1])
                    if v != None:
                        sendTarget = v
                        msg = eventVar[0]
                else: sendTarget = websocket

                if type(msg) == dict:
                    await sendTarget.send(json.dumps(msg))
                else: await sendTarget.send(msg)

        except Exception as e:
            connection.pop(device)
            print('Disconnect - Error', e)
            break


if __name__ == '__main__':
    print(uuid.uuid4().hex)
    print(hashlib.sha256(b'seon1234SEORO_By_Seon').hexdigest())

    from ControllerEvent import ControllerEvent
    from Event import Event

    setEvent('test', Event())
    setEvent('controller', ControllerEvent())

    start_server = websockets.serve(client, "0.0.0.0", 9875)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
