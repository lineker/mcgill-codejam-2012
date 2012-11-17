#!/usr/bin/env python
 
 
import socket
import sys
 
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



data = sock.recv(36)
string = ""
while len(data):
  data = sock.recv(36)
  print data
sock.close()

 
sys.exit(0)