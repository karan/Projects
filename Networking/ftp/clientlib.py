from ftplib import *
from IO import *
import sys

class CLIENT:

	def __init__(self,hostname,port=21,username='anonymous',password='anonymous@'):
		self.__ftp = FTP()
		self.__ftp.connect(hostname,port)
		self.__ftp.login(username,password)
		IO.output('Connection Established to %s on port %s' % (hostname,str(port)))

	def close(self):
		self.__ftp.quit()
		sys.exit()

