'''
Scoring Engine for CCDC at large 2012
(c) Kevin Galloway kpgalloway@gmail.com
		Brandon Marken brandon.marken@gmail.com

This software is licensed under the MIT license. 
		
'''
import smtplib
import sys
import socket
import MySQLdb
import time
from scapy.all import *

class Team:

	#our base constructor sets our score to 0
	def __init__(self,num):
		self.score=0
		self.teamNum=str(num)

	def send_email(self,from_address,to_address):
		header = "From: " + from_address + "\r\nTo: " + to_address + "\r\n\r\n"
		message = "This is a test message\nFrom Scoring Engine\n"
		email_body = header + message
		server = smtplib.SMTP('localhost')
		server.set_debuglevel(1)
		server.sendmail(from_address,to_address,email_body)
		server.quit()
	
	def check_mysql(self,db_user, password, server, database):
		db = MySQLdb.connect(host=server,user=db_user, passwd=password,db=database)
		cur_cursor = db.cursor()
		cur_cursor.execute("""SELECT * FROM test""")
		row_list = cur_cursor.fetchall()
		for i in row_list:
			print i

	def add_score(self,column,team):
		db = MySQLdb.connect(host='localhost',user='kevin',passwd='kevinpass',db='testdb')
		cur_cursor = db.cursor()
		query = """UPDATE team_score SET """
		query = query + column + " =" + column + " +1 WHERE id=" + team
		cur_cursor.execute(query)

	def connect_smpt_server(self,host,port,user,password):
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		try:
			login_value = server.login(user,password)
			print login_value
		except smtplib.SMTPAuthenticationError:
			print "Argh"
		server.close()

	def find_dhcp_servers(self):
		conf.checkIPaddr = False
		fam,hw = get_if_raw_hwaddr(conf.iface)
		dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),"end"])
		ans, unans = srp(dhcp_discover, multi=True, timeout=3)			# Press CTRL-C after several seconds
		dhcp_ip = []
		for i in ans:
			print i[1][Ether].src
			dhcp_ip.append(i[1][IP].src)
		print "DHCP IPs"
		for i in dhcp_ip:
			print i


	'''
		This checks whether they can send web out from the work stations
		writes to the relevant database
	'''
	def checkWebIn(self):
		HOST = 'daring.cwi.nl'    # The remote host
		PORT = 80              # The same port as used by the server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		s.sendall('ping?')
		data = s.recv(1024)
		s.close()
		#do stuff


	'''
		The check_dns function
		takes no parameters and returns nothing
		increments the score it can resolve the domain server
	'''
	def check_dns(self):
		hostname="www.ccdc" + self.teamNum+".lab"
		try:
			socket.gethostbyname(hostName)
			self.score+=1
		except:	
			return



if __name__=='__main__':
	teams=[]
	for i in range(0,5):
		teams.append(Team(i))
	
	while True:
		for i in range(5):
			#do stuff
			teams[i].check_dns()
			#do other
		time.sleep(300)			#wait 5 minutes	

#check_mysql('kevin','kevinpass','localhost','testdb')
#add_score('dhcp','1')
#find_dhcp_servers()


	

	
