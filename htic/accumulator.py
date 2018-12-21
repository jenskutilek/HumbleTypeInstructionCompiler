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
		length = len(self.cache)
		current = 0
		while current < length:
			# Look for sequence of bytes or words
			writingBytes = isByte(self.cache[current])
			peek = current + 1
			while peek < min(length, current+255):
				if isByte(self.cache[peek]) == writingBytes:
					peek += 1
				else:
					break

			# Add correct instruction
			count = peek - current
			if count <= 8:
				if writingBytes:
					self.writer.writeInstruction("PUSHB", 0xB0, count-1, 7)
				else:
					self.writer.writeInstruction("PUSHW", 0xB8, count-1, 7)
			else:
				if writingBytes:
					self.writer.writeInstruction("NPUSHB", 0x40, 0, 0)
				else:
					self.writer.writeInstruction("NPUSHW", 0x41, 0, 0)
				self.writer.writeByte(count)

			# Add values
			while current < peek:
				if writingBytes:
					self.writer.writeByte(self.cache[current])
				else:
					self.writer.writeWord(self.cache[current])
				current += 1
		self.cache = []


def isByte(value):
	return value >= 0 and value < 256
