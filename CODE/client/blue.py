#!/usr/bin/env python
 
import time
import socket
import sys
import Queue
import threading
from strategyman import StrategyMan
from time import time



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


startFlag = False

# intialize input and output Q's for each of the 4 strategy managers
inputQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}
outputQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}
transactionQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}


# start manager threads
threads = {'sma': smaManager(1, 'sma', inputQueues['sma'], outputQueues['sma'], transactionQueues['sma']), 'lwma': lwmaManager(2, 'lwma', inputQueues['lwma'], outputQueues['lwma'], transactionQueues['lwma']), 'ema': emaManager(3, 'ema', inputQueues['ema'], outputQueues['ema'], transactionQueues['ema']), 'tma': tmaManager(4, 'tma', inputQueues['tma'], outputQueues['tma'], transactionQueues['tma'])}

for key in threads:
    threads[key].start()

# start sock HEREEEEE, pass the transaction queues and output queues and the flag(?)


# poll until startFlag is True
while not startFlag:
    # do blah



# now we start processing

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
        for q in inputQueues:
            inputQueues[q].put(point)
            print point

    time.sleep()

