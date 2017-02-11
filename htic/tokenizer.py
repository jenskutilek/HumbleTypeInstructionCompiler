import re


class Tokenizer(object):

	def __init__(self, stream):
		self.stream = stream
		self.position = 1
		self.tokens = []
		self.cache = []
		self.doCache = False

	def peek(self):
		self.__refresh()
		if self.tokens:
			return self.tokens[0]
		else:
			return ""

	def get(self):
		self.__refresh()
		if self.tokens:
			if self.doCache:
				self.cache.append(self.tokens[0])
			if self.tokens[0] == "\n":
				self.position += 1
			return self.tokens.pop(0)
		else:
			return ""

	def mark(self):
		self.cache = []
		self.doCache = True

	def unmark(self):
		self.cache = []
		self.doCache = False

	def rewind(self):
		self.tokens = self.cache + self.tokens
		self.position -= self.cache.count("\n")
		self.unmark()

	def __refresh(self):
		if not self.tokens:
			line = self.stream.readline()
			if line:
				self.tokens += [t for t in re.split("([\{\}\(\)\[\]\+\-])|\s+|#.*", line) if t]
				self.tokens += "\n"
