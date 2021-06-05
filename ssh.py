import subprocess
import socket
import select
import threading
import random
import time
import sys,os
import platform

# colors
bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'

class sshRunn:
	def __init__(self,inject_host,inject_port):
		self.inject_host = inject_host
		self.inject_port = inject_port

	def ssh_client(self,socks5_port,host,port,user,password):
			try:
				
				dynamic_port_forwarding = '-CND {}'.format(socks5_port)
				host = host 
				port = port
				
				username = user 
				password = password 
				inject_host= self.inject_host
				inject_port= self.inject_port
				payload=f'CONNECT {host}:{port} HTTP/1.1\r\n\r\n'.encode()
				try:
				    soc.send(payload)   
				except Exception as e:
				    while e == '[Errno 9] Bad file descriptor':
				           soc.sendall(payload)
				    else:
				    	logs(e)
				
				response = subprocess.Popen(
	                (
	                   f'sshpass -p {password} ssh -o "ProxyCommand=nc --proxy {inject_host}:{inject_port} %h %p" {username}@{host} -p {port} -v {dynamic_port_forwarding} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
	                   
	                
	                ),
	                shell=True,
	                stdout=subprocess.PIPE,
	                stderr=subprocess.STDOUT
	            )
				
				for line in response.stdout:
					line = line.decode('utf-8',errors='ignore').lstrip(r'(debug1|Warning):').strip() + '\r'
					logs(line)
					if 'pledge: proc' in line:logs(G+'CONNECTED SUCCESSFULLY'+GR)
					elif 'Permission denied' in line:logs(R+'Access Denied'+GR)
					elif 'Connection closed' in line:logs(R+'Connection closed'+GR)
					elif 'Could not request local forwarding' in line:logs(R+'Port used by another programs'+GR)
			
			except KeyboardInterrupt:
				sys.exit('stoping ..')


	def create_connection(self,host,port,user,password):
		global soc , payload
		try:    								
		    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		    soc.connect((self.inject_host,int(self.inject_port)))
		    thread=threading.Thread(target=self.ssh_client,args=('1080',host,port,user,password))
		    thread.start()
		except ConnectionRefusedError:            
		    logs(R+' <!> Run client.py first in a new tab\n\tthen try again'+GR)
		    soc.close()
		      
		except KeyboardInterrupt:
				logs(R+'ssh stopped'+GR)

	def logs(self,log):
		logfile = open('sshlogs.txt','a')
		logfile.write(str(log)+'\n')
if __name__=='__main__':		        
	import configparser
	config = configparser.ConfigParser()
	try:
		config.read_file(open('settings.ini'))
	except Exception as e:
		logs(f'{R}ERROR {e}')
		sys.exit()
	host = config['ssh']['host']
	port = config['ssh']['port']
	user = config['ssh']['username']
	password = config['ssh']['password']
	
	start = sshRunn('127.0.0.1','9092')
	start.create_connection(host,port,user,password)    