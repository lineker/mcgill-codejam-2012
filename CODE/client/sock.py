import gevent
import threading

from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

app = Bottle()

class Sock(threading.Thread, BaseNamespace, BroadcastMixin):
    
    def __init__(self, thread_id, SMA, LWMA, EMA, TMA, start_flag):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queues = [SMA, LWMA, EMA, TMA]
        self.target = 0
        self.start_flag = start_flag

    def run(self):
        pass
        server.SocketIOServer(
            ('localhost', 9090), app, policy_server=False).serve_forever()

    def on_ready(self):
        # Set start_flag to non-empty to notify Blue
        self.start_flag.put(1)
        
        # Flag acknowledged by Blue and start consuming
        while self.start_flag.empty():
            for i in xrange(4):
                try:
                    data = self.queues[i].get() 
                    if self.target == i:
                        self.emit("data", json.dumps(data))
                except:
                    pass # Queue is currently empty

        self.emit("complete")

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return "out"
