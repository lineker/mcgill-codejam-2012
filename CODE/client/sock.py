from gevent import monkey; monkey.patch_all()
from json import tool
import gevent
import commands
from time import time
from random import random
from bottle import Bottle, request
from socketio import server, socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import socket

app = Bottle()
s = socket.socket()
s1 = socket.socket()
s2 = socket.socket()
s3 = socket.socket()


'''
    Use this dictionary to do generate report. Example of transactions dictionary:
    'lwma': [{'price': '64.670', 'strategy': 'lwma', 'type': 'S', 'manager': '4', 'time': '2'}], 
    'ema': [{'price': '64.770', 'strategy': 'ema', 'type': 'S', 'manager': '3', 'time': '2'}], 
    'sma': [{'price': '64.810', 'strategy': 'sma', 'type': 'S', 'manager': '3', 'time': '2'}], 
    'tma': [{'price': '64.670', 'strategy': 'tma', 'type': 'S', 'manager': '4', 'time': '2'}]}
'''
transactions = []

hasStarted = False
class Data(BaseNamespace, BroadcastMixin):

    def on_start(self):
        self.on_ready()

    def on_ready(self):

        gevent.sleep(3)
        # As client
        if hasStarted == False:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 3333))
            s.send('H\n')
            s.close()
        fulldata = ''
        count = 0
        while 1:
            data = conn.recv(1)
            # if count == 0:
            #     data = conn.recv(1)
            # elif count == 1:
            #     data = conn1.recv(1)
            # elif count == 2:
            #     data = conn2.recv(1)
            # else:
            #     data = conn3.recv(1)
            if not data:
                print transactions
                continue
            else:
                if data == '*':
                    print fulldata
                    parsed_data = fulldata.split('|')
                    if parsed_data[0] == 'T':
                        #dic = {'time': parsed_data[1], 'type': parsed_data[2], 'price': parsed_data[3], 'manager': parsed_data[4], 'strategy': parsed_data[5]}
                        dic = {'time': parsed_data[4], 'type': parsed_data[1], 'price': parsed_data[3], 'manager': parsed_data[4], 'strategy': parsed_data[2].upper()}
                        #transactions[parsed_data[5]] = []
                        transactions.append(dic)
                        self.emit('transaction', dic)
                    elif parsed_data[0] == 'A':
                        '''use this value to decide if should sent to UI based on the tab chose by user
                        count = 0 --> SMA
                        count = 1 --> LWMA
                        count = 2 --> EMA
                        count = 2 --> TMA'''
                        
                        #parsed_data[4] -->  strategy type
                        #parsed_data[4] --> clock
                        if parsed_data[4] == 'sma': 
                            self.emit('average', { 'time': time() * 1000, 'price': float(parsed_data[1]), 'slow': float(parsed_data[2]), 'fast': float(parsed_data[3])})
                    #self.emit('data', { 'time': time() * 1000, 'value': random()})
                    fulldata = ''
                    gevent.sleep(0.1)
                else:
                    fulldata = fulldata + data
    
            def on_report(self):
                # all transactions as json
                fo = open("trans.json", "w")
                fo.write('  { "team" : "team-X",\n')
                fo.write('      "destination" : "ysbecca@gmail.com",\n')
                fo.write('      "transactions" : [')
                contents = '{\n           "time": "8004",\n          "type" : "buy",\n          "price" : 120,\n          "manager" : "Manager1",\n          "strategy" : "EMA"\n      }]}\n'
                for trans in transactions:
                    for i in range(len(transactions[trans])):
                        contents.replace("8004", transactions[trans][i]["time"])
                        contents.replace("buy", transactions[trans][i]["type"])
                        contents.replace("120", transactions[trans][i]["price"])
                        contents.replace("Manager1", transactions[trans][i]["manager"])
                        contents.replace("EMA", transactions[trans][i]["strategy"])


                print "Generated JSON data for curl to e-signlive: "
                fo.write(contents)
                fo.close()

                cmd = 'curl -X "POST" -H "Authorization: Basic Y29kZWphbTpBRkxpdGw0TEEyQWQx" -H "Content-Type:application/json" --data-binary @trans.json "https://stage-api.e-signlive.com/aws/rest/services/codejam"'
                re = commands.getstatusoutput(cmd)
                temp = re[1]
                print temp
                data = ""
                for i in range(len(temp)):
                    if temp[i] == "{":
                        while i != len(temp):
                            data += temp[i]
                            print data
                            i += 1

                print data + "<---- final"

                self.emit('ceremony', eval(data)) # format {{'ceremonyId':'T5ZWzanNFprSdKlcnG2m8wmIvNoV'}}

                conn.close()
        

@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    socketio_manage(request.environ, {'': Data}, request=request)
    return 'out'

if __name__ == '__main__':
    # As server 1
    s = socket.socket()
    HOST = 'localhost'
    PORT = 9001
    s.bind((HOST, PORT))
    s.listen(1)
    # As server 2
    s1 = socket.socket()
    # HOST = 'localhost'
    # PORT = 9002
    # s1.bind((HOST, PORT))
    # s1.listen(1)
    # # As server 3
    # s2 = socket.socket()
    # HOST = 'localhost'
    # PORT = 9003
    # s2.bind((HOST, PORT))
    # s2.listen(1)

    # # As server 4
    # s3 = socket.socket()
    # HOST = 'localhost'
    # PORT = 9004
    # s3.bind((HOST, PORT))
    # s3.listen(1)

    print 'waiting for blue'
    conn, addr = s.accept()
    # conn1, addr = s1.accept()
    # conn2, addr = s2.accept()
    # conn3, addr = s3.accept()
    print 'all connection accepted'
    server.SocketIOServer(
        ('localhost', 9090), app, policy_server=False).serve_forever()
