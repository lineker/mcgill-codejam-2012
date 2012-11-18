#!/usr/bin/env python
 
import time
import socket
import sys
import Queue
import threading
from smaManager import smaManager
from tmaManager import tmaManager
from lwmaManager import lwmaManager
from emaManager import emaManager 
from sock import Sock
import genericStrategyMan
import signal
HOST = 'localhost'
PORT = 3000


# #hack ctrl+D
# signal.signal(signal.SIGINT, signal_handler)

# def signal_handler(signal, frame):
#     print 'Ctrl+C detected, killing threads'
#     for i in range(len(threads)):
#         threads[i].exitFlag = True
#     sys.exit(0)

class Blue:

    def __init__(self, outQueues, startQueue):

        self.flagQueue = startQueue
        self.clock = 0


        try:
            exchange_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

        try:
            exchange_sock.connect((HOST, PORT))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(2)


        # intialize input and output Q's for each of the 4 strategy managers
        inputQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}
        outputQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}
        transactionQueues = {'sma': Queue.Queue(), 'lwma': Queue.Queue(), 'ema': Queue.Queue(), 'tma': Queue.Queue()}


        sma = smaManager(1, 'sma', inputQueues['sma'], clock, outputQueues['sma'], transactionQueues['sma'])
        lwma = lwmaManager(2, 'lwma', inputQueues['lwma'], clock, outputQueues['lwma'], transactionQueues['lwma'])
        ema = emaManager(3, 'ema', inputQueues['ema'], clock, outputQueues['ema'], transactionQueues['ema'])
        tma = tmaManager(4, 'tma', inputQueues['tma'], clock, outputQueues['tma'], transactionQueues['tma'])

        # start manager threads
        threads = []
        threads.append(sma)
        threads.append(lwma)
        threads.append(ema)
        threads.append(tma)

        for i in range(len(threads)):
            threads[i].start()
            #pass

        # poll until startFlag is True
        while self.flagQueue.isEmpty():
            # do blah
            print ""


        # now we start processing
        exchange_sock.send("H\n") # start the feed
        byteSize = 1
        data = exchange_sock.recv(byteSize)
        string_del = []

        while len(data):
            #print "data read --> "+data
            if(data.rfind("C") != -1):
                print "market closed"
                break
            if(data.rfind("|") != -1):
                point = float(''.join(string_del))
                print "read point: " + str(point)
                for q in inputQueues:
                    inputQueues[q].put(point)
                  
                string_del = []
                clock += 1
            else:
                string_del.append(data)

            data = exchange_sock.recv(byteSize)

      

