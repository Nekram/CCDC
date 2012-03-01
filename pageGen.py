#!/usr/bin/python
'''
Page Generator for CCDC at large 2012
(c) Kevin Galloway kpgalloway@gmail.com
    Brandon Marken brandon.marken@gmail.com

This software is licensed under the MIT license. 
    
'''
import re
import os
import sys
import socket
import MySQLdb as mdb
import time
import datetime

def initDB():
	conn=mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	with conn:
  	cur = conn.cursor()
  	cur.execute("CREATE TABLE IF NOT EXISTS\
    	  Teams(ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
		for i in range(1,6):
  		cur.execute("INSERT INTO Teams(Name) VALUES('Team"+str(i)+ "')")


#this takes a team number then makes a bunch of sql queries
#then returns a string giving us the services for the team
def getWeb(teamNum):
	try:
		conn = mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	except:
		print("could not connect to the database")
	return ""

def getDNS(teamNum):
	try:
		conn = mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	except:
		print("could not connect to the database")

	return ""

def getSSH(teamNum):
	try:
		conn = mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	except:
		print("Could not connect to the database")
	return ""

def getMail(teamNum):
	try:
		conn = mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	except:
		print("Could not connect to the database")	
	return ""

#the pageGen function
#writes an to /var/www/index.html
#generates our page which tells people whether their last 3 services
#are up. Takes no parameters and returns nothing
def pageGen():
	try:
		handle=open("/var/www/index.html",'w')
	except:
		print("Cannot open /var/www/index.html")
		print("Probably a permission issue")
		sys.exit(0)

	theTime=str(datetime.datetime.now())

	#The base of the page
	base="<html><head><title> Services available as of "
	base+=theTime
	base+="</title></head><body><center>Service status as of " +theTime
	#adding our table 
	base+="<center><table border=\"1\"><tr>"

	base+="<td>team\services </td><td>DNS</td><td>Web</td><td>Mail</td><td>SSH</td></tr>"
	for i in range(5):
		base+="<tr><td>"+str(i+1)+"</td><td>"+getDNS(i+1)+"</td><td>"+getWeb(i+1)+"</td><td>"
		base+=getMail(i+1)+"</td><td>"+getSSH(i+1)+"</td></tr>"

	base+="</table>	</center></body></html>"
	handle.writelines(base)

if __name__=='__main__':

	if sys.argv[1] is "init":
		initDB()

		pageGen()
