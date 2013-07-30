from commands import *
import re
class Shell:
	def __init__(self,client):
		self.client = client
		self.__ch = CommandHandler()
		self.__loopback()

	def execute(self,command,args):
		try:
			result = getattr(CommandHandler,command)(self.__ch,self.client,args)
		except AttributeError, e:
			print '`%s` is not a valid command' % command
		else:
			pass

	def parseRawCommand(self,comstring):
		return re.split(' ',comstring.strip())

	def __loopback(self):
		inp = IO.input('PyFTP:%s>'%self.client.getCon().pwd())
		com = self.parseRawCommand(inp)
		if not com[0]:
			pass
		else:
			self.execute(com[0],com[1:])
		self.__loopback()



