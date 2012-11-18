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
    def __init__(self):
        self.queues = outputQueues
        self.transactions = transactionQueues
        self.start_flag = startQueue

    def on_ready(self):
        # Set start_flag to non-empty to notify Blue
        self.start_flag.put(1)
        
        # Flag acknowledged by Blue and start consuming
        while self.start_flag.empty():
            for oq in outputQueues:
                try:
                    data = self.outputQueues[i].get() 
                    if self.target == i:
                        self.emit("data", json.dumps(data))
                except:
                    pass # Queue is currently empty

        self.emit("complete") 

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"

if __name__ == '__main__':
    blue = Blue(outputQueues, startQueue, transactionQueues)
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
