from gevent import monkey; monkey.patch_all()

import gevent

from time import time
from random import random
from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import socket

app = Bottle()
s = socket.socket()
class Data(BaseNamespace, BroadcastMixin):

    def on_start(self):
        self.on_ready()

    def on_ready(self):

        # As server
        s = socket.socket()
        HOST = "localhost"
        PORT = 9001
        s.bind((HOST, PORT))
        s.listen(1)
        print "waiting for blue"
        conn, addr = s.accept()
        gevent.sleep(3)
        # As client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 3333))
        s.send("H\n")
        s.close()
        fulldata = ""
        while 1:
            data = conn.recv(1)
            if not data:
                continue
            else:
                if data == "*":
                    print "raw : "+fulldata
                    parsed_data = fulldata.split("|")
                    print parsed_data
                    if parsed_data[0] == "T":
                        print "T added"
                        self.emit("transaction", {"time": parsed_data[1], "type": parsed_data[2], "price": parsed_data[3], "manager": parsed_data[4], "strategy": parsed_data[5]})
                    elif parsed_data[0] == "A":
                        print "A added"
                        #self.emit("average", {"price": parsed_data[1], "slow": parsed_data[2], "fast": parsed_data[3]})
                        self.emit('data', { "time": time() * 1000, "value": random()})
                    #self.emit('data', { "time": time() * 1000, "value": random()})
                    fulldata = ""
                    #gevent.sleep(0.5)
                else:
                    fulldata = fulldata + data
        conn.close()
        

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"

if __name__ == '__main__':
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
