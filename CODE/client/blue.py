#!/usr/bin/env python
 
import time
import socket
import sys
import threading
import re



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

p = re.compile('\d{1, 3}' + '.' + '\d', re.IGNORECASE)

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
  	  		# detect half-read values
  			#cut = string_del.

  	  	except ValueError:
  	  		print ""
	  	buff[0:] = map(float, string_del)
  	print buff

  	# send buff to average calculator here

sock.close()


	# url = "http://localhost:8080"
 #    data = {'x': data[min], 'y': data[max]}
 #    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
 #    req = urllib2.Request('http://localhost:3000')
 #    req.add_header('Content-Type', 'application/json')
 #    r = requests.post(url, data=json.dumps(data), headers=headers)


sys.exit(0)