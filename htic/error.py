class HumbleError(Exception):

	def __init__(self, message):
		self.message = message.replace("\n", r"\n")
		self.position = None

	def __str__(self):
		if self.position:
			return "Line {}: {}".format(self.position, self.message)
		else:
			return self.message
