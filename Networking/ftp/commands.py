from IO import *
from constants import *
class CommandHandler(object):
	"""Commands that shell can execute"""

	def __init__(self):
		pass

	def exit(self,client):
		if messages.has_key('exit'):
			IO.output(messages['exit'])
		client.close()

	def help(self,client):
		if messages.has_key('help'):
			IO.output(messages['help'])
		#Loop through dict and display shit



		