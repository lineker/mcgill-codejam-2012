#!/usr/bin/env python
 
import time
import socket
import sys
import threading



HOST = 'localhost'
GET = '/rss.xml'
PORT = 3000

 
try:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(1)
 
try:
  sock.connect((HOST, PORT))
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(2)

sock.send("H\n")
count = 0

data = sock.recv(48)
string = ""
string_del = ""
buff = []

class MyThread ( threading.Thread ):

   def run ( self ):
   		min = 0
   		max = 0
   		while True:
	   		if len(buff) > 0:
	   			# min = max
	   			# max += len(buff)
	   			# subset = []
	   			# subset = buff[min:max]
	   			print min
	   			print max
	   			print buff
	   			print "\n"
	   		else:
	   			time.sleep(1)

#MyThread().start()
stor = []
min = 0
max = 0

while len(data):
	string_del = ""
	data = sock.recv(48)
	string_del = data.split("|")
	string_del.pop()
	#print string_del
	stor[len(stor):] = string_del

  	if len(string_del) > 0:
  		try:
  	  		string_del.remove("")
  	  	except ValueError:
  	  		print ""
	  	buff[0:] = map(float, string_del)
  	print buff

  	# send buff to average calculator here

sock.close()


def avg(buff):
	val = buff[0]
	# calculate avg
	if buff.size < 5:
		val = 1.000
	elif buff.size < 20:
		val = 2.000
	else:
		val = 3.000

	# url = "http://localhost:8080"
 #    data = {'x': data[min], 'y': data[max]}
 #    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
 #    req = urllib2.Request('http://localhost:3000')
 #    req.add_header('Content-Type', 'application/json')
 #    r = requests.post(url, data=json.dumps(data), headers=headers)


sys.exit(0)