from commands import *
class Shell:
	def __init__(self,client):
		self.client = client
		self.__ch = CommandHandler()
		self.loopback()

	def execute(self,command,args):
		try:
			result = getattr(CommandHandler,command)(self.__ch,self.client)
		except AttributeError, e:
			print '`%s` is not a valid command' % command
		else:
			pass

	def commandParse(self,comstring):
		pass

	def loopback(self):
		inp = raw_input('PyFTP>')
		self.execute(inp,self.commandParse(inp))
		self.loopback()



