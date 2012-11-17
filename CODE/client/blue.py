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

min = 0
max = 0

data = sock.recv(1024)
string = ""
string_del = ""
buff = []
while len(data):
  data = sock.recv(1024)
  string += data
  string_del = string.split("|")
sock.close()


map(float, buff)
max = buff.size

# send buff

sys.exit(0)