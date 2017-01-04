class FTPException(Exception):
	'''Base Exception class for FTPClient'''
	pass

class InvalidPortNumberError(FTPException):
	'''Exception raised when port number is invalid'''
	def __init__(self,message):
		super(FTPException,self).__init__(self,message)
		self.message = message

