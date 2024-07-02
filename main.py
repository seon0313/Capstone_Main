import asyncio
import websockets
import sqlite3
import uuid
import json
import hashlib

con = sqlite3.connect('./data.db')

cur = con.cursor()
cur.execute('create table if not exists pid (id text)')
cur.execute('create table if not exists pids (id text, p real, i real, d real, time real)')
cur.execute('create table if not exists offset (id text)')
cur.execute('create table if not exists offsets (id text, left real, right real, time real)')
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
    for i in events.values():
        msg = i.firstRun()
        if msg != None:
            await websocket.send(msg)
    while True:
        try:
            data = await websocket.recv()
            data: dict = json.loads(data)
            device = data['device']
            request = data['request']
            #if data.get('target') != None: request = data['target']
            type_ = data['type']

            if target == None:
                target = device
                connection[target] = websocket

            args = data.get('args')
            if args == None: args = []
            func = events.get(request)
            if func != None:
                eventVar: str = func.run(device, type_, data.get('target'), *args)
                if eventVar != None:
                    sendTarget = None
                    msg = eventVar
                    if type(eventVar) == tuple:
                        v = connection.get(eventVar[1])
                        if v != None:
                            sendTarget = v
                            msg = eventVar[0]
                    else:
                        sendTarget = websocket
                    if sendTarget:
                        if type(msg) == dict:
                            await sendTarget.send(json.dumps(msg))
                        else:
                            await sendTarget.send(msg)

        except Exception as e:
            connection.pop(device)
            print('Disconnect - Error', e)
            break


if __name__ == '__main__':
    print(uuid.uuid4().hex)

    from ControllerEvent import ControllerEvent
    from Event import Event
    from SystemEvent import SystemEvent

    setEvent('test', Event(getData))
    setEvent('controller', ControllerEvent(getData))
    setEvent('system', SystemEvent(getData, events))

    start_server = websockets.serve(client, "0.0.0.0", 9875)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
