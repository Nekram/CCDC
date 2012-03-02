#!/usr/bin/python
'''
	This is a simple server program to run on their work stations
	all it will do is respond with the relevant data to demonstrate that their 
	internet connectivity is open

	ripped off shamelessly from 
	http://docs.python.org/library/socket.html
	
'''

import socket
import time
import re

HOST=''
PORT=80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)

conn.close()
