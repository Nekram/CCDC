#!/usr/bin/python
'''
This is a program to randomly change the static IP on a machine ever so often
Brandon Marken
This software is licensed under the MIT license

'''

import time
import random
import os

def changeIP():
	comm = "ifconfig eth0 192.168.122."+str(random.randint(0,256))+" netmask 255.255.255.0 up"
	os.system(comm)

if __name__=='__main__':
	while True:
		time.sleep(random.randint(250,350))
		changeIP()
