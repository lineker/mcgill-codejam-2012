#!/usr/bin/env python
 
import time
import socket
import sys
import gevent
from averages import Simple 
from strategyman import StrategyMan
from gevent import monkey; monkey.patch_all()
from time import time
from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

app = Bottle()

class Blue(BaseNamespace, BroadcastMixin):

    def on_ready(self):
        def generate_data():
            # Get connection to the MS exchange on exchange_sock
            stratMan = StrategyMan()
            HOST = 'localhost'
            PORT = 3000

            try:
              exchange_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
              sys.stderr.write("[ERROR] %s\n" % msg[1])
              sys.exit(1)
             
            try:
              exchange_sock.connect((self.HOST, self.PORT))
            except socket.error, msg:
              sys.stderr.write("[ERROR] %s\n" % msg[1])
              sys.exit(2)

            exchange_sock.send("H\n") # start the feed
            while True:
                data = exchange_sock.recv(46)
                string = ""
                string_del = ""
                buff = []
                stor = []
                index = -1
                last_string = ""
                while len(data):
                    string_del = ""
                    if last_string != "" and last_string != "C":
                        data = last_string + data
                        last_string = ""
                        
                    string_del = data.split("|")
                    index = data.rfind("|")

                    if index != -1 & (index + 1) < len(data):
                        last_string = string_del.pop()
                    
                    #print string_del
                    stor[len(stor):] = string_del

                    if len(string_del) > 0:
                        try:
                            string_del.remove("")
                            #detect half-read values
                            #cut = string_del.

                        except ValueError:
                            print ""
                        buff[0:] = map(float, string_del)
                    print buff
                    for point in buff:
                        # pass point to strategyman
                        self.stratMan.process(point)
                        # get point and averages and send it
                        self.emit('data', { "time": time() * 1000, "value": random() })
                        gevent.sleep(0.5) # why?

                    data = sock.recv(46)    

        self.spawn(generate_data)
        sock.close()
        print "closing socket"


@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"

if __name__ == '__main__':
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
    
    

