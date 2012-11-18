import stackless
import socket
from multiprocessing import Process, Queue, Value
from simpleGenericStrategyManager import simpleEmaManager,simpleTmaManager, simpleSmaManager,simpleLwmaManager
import sys
HOST = "localhost"
PORT = 3000
clock = 0
#start stacklets
def sma(brain, channel):
    for item in channel:
		#print "sma receiving"
		#print item
		result = brain.process(item)

def tma(brain, channel):
	for item in channel:
		#print "tma receiving"
		#print item
		brain.process(item)

def lwma(brain, channel):
	for item in channel:
		#print "lmwa receiving"
		#print item
		brain.process(item)

def ema(brain, channel):
	for item in channel:
		#print "ema receiving"
		#print item
		brain.process(item)

#might delete
def transac_processing(brain, channel, ch_web):
		trans_done = 0
		trans_lost = 0
		try:
			#transaction connection
			HOST = 'localhost'
			PORT = 3001
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((HOST, PORT))
			n = 0
			for item in channel:
				#print "process transaction"
				#print item
				cmd = item[0]
				if cmd == "T":
					sock.send(item[1] + "\n")
					response = sock.recv(100)
					#check if is a ERROR , maybe market is already closed
					if(str(response).rfind("E") != -1):
						#print "market ERROR"
						trans_lost= trans_lost +1 
					else:
						#channel to someone that will send to Web
						#print item
						#print "cmd response: "+response
						trans_done= trans_done +1
						#send web
						item[len(item):] = [num.value]
						ch_web.send(item)
				elif cmd == "A":
					#send to web
					item[len(item):] = [num.value]
					if n == 10:
						ch_web.send(item)
						n = 0
					else:
						n = n+1
					pass
				else:
					print "trans done " + str(trans_done)
					print "trans lost " + str(trans_lost)
					#send to web that is done
					ch_web.send(['C'])
					break

						

		except socket.error, msg:
			sys.stderr.write("[ERROR] %s\n" % msg[1])
			sys.exit(2)
		
		# for item in channel:
		# 	print "adding"
		# 	brain.put(item)
def send_transaction(channel):
	n = 0
	try:
		# #sma
		sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock1.connect((HOST, 9001))
		# #lwma
		# sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock2.connect((HOST, 9002))
		# #ema
		# sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock3.connect((HOST, 9003))
		# #tma
		# sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock4.connect((HOST, 9004))

		for item in channel:
			n = n+1
			#"T|"+str(time)+"|"+str(cmd)+"|"+str(response.strip())+"|"+str(manager)+"|"+str(sType)+"*"
			#['T', 'B', 'lwma', 98.27, time]
			
			if item[0] == "T":
				sock_type = item[2]
			#"A|"+str(point)+"|"+str(self.averages['slow'])+"|"+str(self.averages['fast'])+"*"
			#['A', 98.27, 97.79382499999979, 97.6471999999995, 'tma', time]
			elif item[0] == "A":
				sock_type = item[4]
			elif item[0] == "C":
				#sock1.send("C")
				break

			item[len(item):] = ['*']
			message = "|".join(map(str, item))
			#print n
			
			if len(message) > 0:
				print message
				sock1.send(message)

			# if sock_type == 'sma':
			# 	if len(message) > 0:
			# 		sock1.send(message)
			# 		pass
			# elif sock_type == 'lwma':
			# 	if len(message) > 0:
			# 		#sock1.send(message)
			# 		pass
			# elif sock_type == 'ema':
			# 	if len(message) > 0:
			# 		#sock1.send(message)
			# 		pass
			# elif sock_type == 'tma':
			# 	if len(message) > 0:
			# 		#sock1.send(message)
			# 		pass

	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(2)



#possible multiprocessing, not being used now
def send_trans(queue):
	HOST = 'localhost'
	PORT = 3001

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		while 1:
			
			item = queue.get()
			sock.send(result[0] + "\n")
			#check if is a ERROR , maybe market is already closed
			cmd = item[0]
			if cmd == "T":
				sock.send(item[1] + "\n")
				response = sock.recv(100)
				#check if is a ERROR , maybe market is already closed
				if(str(response).rfind("E") != -1):
					#print "market ERROR"
					trans_lost= trans_lost +1 

				else:
					#channel to someone that will send to Web
					#print item
					#print "cmd response: "+response
					trans_done= trans_done +1
			else:
				#send to web
				print item
			
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(2)


def read_feed(channels, t_channel,num):
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

	print "waiting to start"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, 3333))
	s.listen(1)
	conn, addr = s.accept()
	print 'Connected by', addr

	start = conn.recv(1)
	while start != "H":
	    start = conn.recv(1)
	conn.close()

	exchange_sock.send("H\n") # start the feed
	byteSize = 1
	data = exchange_sock.recv(byteSize)
	string_del = []

	from time import time
	start_time = time()
	while len(data):
	    #print "data read --> "+data
	    if(data.rfind("C") != -1):
	        print "market closed"
	        t_channel.send(['C'])
	        break
	    if(data.rfind("|") != -1):
	        point = float(''.join(string_del))
	        #print "read point: " + str(point)
	        num.value = num.value+1
	        for ch in channels:
    			ch.send(point)
	        #for q in inputQueues:
	            #inputQueues[q].put(point)
	            
	        string_del = []
	        #clock.add(1)
	    else:
	        string_del.append(data)

	    data = exchange_sock.recv(byteSize)

	end_time = time()
	print "elapsed : " + str(start_time-end_time) 

if __name__ == '__main__':
	num = Value('i', 0)

	ch_sma = stackless.channel()
	ch_tma = stackless.channel()
	ch_lwma = stackless.channel()
	ch_ema = stackless.channel()
	ch_transac = stackless.channel()
	ch_web = stackless.channel()

	#transaction queue
	#q = Queue()

	task1 = stackless.tasklet(sma)(simpleSmaManager(ch_transac),ch_sma)
	task2 = stackless.tasklet(tma)(simpleTmaManager(ch_transac),ch_tma)
	task3 = stackless.tasklet(lwma)(simpleLwmaManager(ch_transac),ch_lwma)
	task4 = stackless.tasklet(ema)(simpleEmaManager(ch_transac),ch_ema)
	#task4 = stackless.tasklet(transac_processing)(q,ch_transac)
	task4 = stackless.tasklet(transac_processing)(None,ch_transac,ch_web)
	task5 = stackless.tasklet(send_transaction)(ch_web)



# def SendingSequence(channel, sequence):
#     print "sending"
#     for item in sequence:
#     	for ch in channel:
#     		ch.send_sequence(item)

#task = stackless.tasklet(SendingSequence)([ch_sma,ch_tma], ['a','b','c'])

	stackless.run()

	p = Process(target=read_feed, args=([ch_sma, ch_tma,ch_lwma, ch_ema],ch_transac,num,))
	#t = Process(target=send_trans, args=(q,))
	#t.start()
	p.start()
	p.join()
