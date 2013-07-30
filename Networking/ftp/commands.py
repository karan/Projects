from IO import *
from constants import *
import sys
class CommandHandler(object):
	"""Commands that shell can execute"""

	def __init__(self):
		pass

	def exit(self,client,args):
		if messages.has_key('exit'):
			try:
				client.close()
				IO.output(messages['exit'])
			except Exception, e:
				IO.output(e)	
			finally:
				sys.exit()
		

	def help(self,client,args=None):
		if messages.has_key('help'):
			IO.output(messages['help'])
			if not args:
				for key in command_desc:
					IO.output('%s:\t%s' % (key,command_desc[key]))				
			else:
				for key in args:
					if command_desc.has_key(key):
						IO.output('%s:\t%s' % (key,command_desc[key]))
					else:
						IO.output('No entry for `%s` found' % key)
		
	def search(self,client,args):
		if not args:
			IO.output('Invalid')
			return
		p = client.getCon().pwd()
		if args[0] != '-R':
			IO.output('Current Directory:\t%s' % client.getCon().pwd())
			for key in client.getCon().nlst():
				if args[0] in key:
					IO.output(key)
		else:
			if not args[1:]:
				pass
			else:
				self.__searchrec(client,args[1:])
				self.cd(client,[p])


	def __searchrec(self,client,args):
		if not args:
			IO.output('Invalid')
			return
		search_key = args[0]
		for key in client.getCon().nlst():
			try:
				client.getCon().cwd(key)
				self.__searchrec(client,args)
			except Exception, e:
				return
			finally:
				if search_key in key:
					IO.output('%s/%s'% (client.getCon().pwd(),key))

	def cd(self,client,args):
		if not args:
			IO.output('Invalid')
			return
		try:
			client.getCon().cwd(args[0])
		except Exception,e:
			IO.output(e)
		

	def ls(self,client,args):
		if not args:
			par = ''
		else:
			par = args[0]
		try:
			client.getCon().dir(par)
		except Exception, e:
			IO.output(e);

	def pwd(self,client,args=None):
		try:
			IO.output(client.getCon().pwd())
		except Exception, e:
			IO.output(e)
		

		