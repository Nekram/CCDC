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

#
#the initDB function
#should only be called once and builds the initial database 
#
#
def initDB():
	conn=mdb.connect('localhost','whiteTeam','CCDC623','CCDC')
	with conn:
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS\
			Teams(ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
		for i in range(1,6):
			cur.execute("INSERT INTO Teams(Name) VALUES('Team"+str(i)+ "')")

		#create a table for SSH, which has an SSH ID (marks each entry as unique), password, team_id (matches a team ID), and status
		#where values >0 are "on", and a value of 0 is "off"
		cur.execute("CREATE TABLE IF NOT EXISTS\
			ssh(ssh_id INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, status TINYINT(1))")

		#create a taable for web going in	
		cur.execute("CREATE TABLE IF NOT EXISTS\
			webIn(webIn INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, status TINYINT(1))")
		#create a table for web outgoing
		cur.execute("CREATE TABLE IF NOT EXISTS\
			webOut(webOut INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, status TINYINT(1))")

		#create a table for mail
		cur.execute("CREATE TABLE IF NOT EXISTS\
			mail(mail INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, status TINYINT(1))")
		
		#create a table for dns
		cur.execute("CREATE TABLE IF NOT EXISTS\
			dns(dns INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, status TINYINT(1))")

		#for i in range(1,6):
		#create a table for service passwords
		cur.execute("CREATE TABLE IF NOT EXISTS\
			passwords(password_id INT PRIMARY KEY AUTO_INCREMENT, password VARCHAR(255), team_id INT, service VARCHAR(255))")

#This grabs the last three results for a service, and returns them
def get_service(teamNum,service):
	try:
		conn = mdb.connect(host='localhost',user='whiteTeam',passwd='CCDC623',db='CCDC')
		cur = conn.cursor()
		query = "SELECT status FROM " + service + " WHERE team_id = '" + teamNum + "' ORDER BY " + service + " DESC;"
		print query
		cur.execute(query)
		results = cur.fetchmany(3)
		status_list = []
		for i in results:
			if i[0] > 0:
				status_list.append('Up')
			else:
				status_list.append('Down')
		status_string = ''
		if len(status_list) < 3:
			status_string = 'Up Up Up'
		else:
			for i in status_list:
				status_string+=i + ' '
		conn.close()
	except:
		print("Could not connect to the database")
	return status_string

#this takes a team number then makes a bunch of sql queries
#then returns a string giving us the services for the team
def getWeb(teamNum):
	try:
		status = get_service(teamNum,'webIn')
	except:
		print("could not connect to the database")
	return status

def getWebOut(teamNum):
	try:
		status = get_service(teamNum,webOut)
	except:
		print("could not connect to the database")
	return status

def getDNS(teamNum):
	try:
		status = get_service(teamNum,'dns')
	except:
		print("could not connect to the database")
	return status

def getSSH(teamNum):
	try:
		status = get_service(teamNum,'ssh')
	except:
		print("Could not connect to the database")
	return status

def getMail(teamNum):
	try:
		status = get_service(teamNum,'mail')
	except:
		print("Could not connect to the database")	
	return status

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

	arg=""
	try:
		arg=sys.argv[1]
	except:
		pass

	#if arg is "init":
	#initDB()

	pageGen()
	#get_service('1','mail')
