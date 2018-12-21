class Accumulator:

	def __init__(self, writer):
		self.writer = writer
		self.cache = []

	def writeInstruction(self, name, opCode, flag, maxFlag):
		self.flush()
		self.writer.writeInstruction(name, opCode, flag, maxFlag)

	def writeArgument(self, argument):
		self.cache.append(argument)

	def flush(self):
		def getArgSize(arg):
			return 1 if 0 <= arg <= 255 else 2

		while self.cache:
			count = 1
			limit = min(len(self.cache), 255)
			argSize = getArgSize(self.cache[0])

			# Accumulate as many same-sized arguments as possible
			while count < limit and getArgSize(self.cache[count]) == argSize:
				count += 1

			# Write instruction
			if count <= 8:
				if argSize == 1:
					self.writer.writeInstruction("PUSHB", 0xB0, count-1, 7)
				else:
					self.writer.writeInstruction("PUSHW", 0xB8, count-1, 7)
			else:
				if argSize == 1:
					self.writer.writeInstruction("NPUSHB", 0x40, 0, 0)
				else:
					self.writer.writeInstruction("NPUSHW", 0x41, 0, 0)
				self.writer.writeByte(count)

			# Write arguments
			for arg in self.cache[:count]:
				if argSize == 1:
					self.writer.writeByte(arg)
				else:
					self.writer.writeWord(arg)

			self.cache = self.cache[count:]
