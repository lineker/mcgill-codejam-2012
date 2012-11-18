from gevent import monkey; monkey.patch_all()

import gevent
import Queue

from blue import Blue
from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

app = Bottle()

startQueue = Queue.Queue(1)
outputQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}
transactionQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}

class Data(BaseNamespace, BroadcastMixin):
    def on_ready(self):
        def generate_data():
            while True:
                self.emit('data', { "time": time() * 1000, "value": random() })
                gevent.sleep(0.5)

        self.spawn(generate_data)

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"

if __name__ == '__main__':
    blue = Blue(outputQueues, startQueue, transactionQueues)
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
