from gevent import monkey; monkey.patch_all()

import gevent

from time import time
from random import random
from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

app = Bottle()

class Data(BaseNamespace, BroadcastMixin):
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
            print "started ms exchange socket"
            while True:
                self.emit('data', { "time": time() * 1000, "value": random() })
                gevent.sleep(0.5)

        self.spawn(generate_data)

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"

if __name__ == '__main__':
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
