import io


class Writer:

	def writeInstruction(name, opCode, flags, maxFlag):
		"""string, int, int, int"""
		raise NotImplementedError

	def writeByte(byte):
		"""0..255"""
		raise NotImplementedError

	def writeWord(word):
		"""-32768..32767"""
		raise NotImplementedError


class BytesWriter(Writer):

	def __init__(self):
		self.array = bytearray()

	def __bytes__(self):
		return bytes(self.array)

	def writeInstruction(self, name, opCode, flag, maxFlag):
		self.array.append(opCode + flag)

	def writeByte(self, byte):
		self.array.append(byte)

	def writeWord(self, word):
		value = word if word >= 0 else word + 2**16
		self.array.append((value & 0xFF00) >> 8)
		self.array.append(value & 0xFF)


class StringWriter(Writer):

	def __init__(self):
		self.stream = io.StringIO()

	def __str__(self):
		return self.stream.getvalue()

	def writeInstruction(self, name, opCode, flag, maxFlag):
		if maxFlag > 0:
			bits = maxFlag.bit_length()
			self.stream.write("{0}[{1:0>{2}b}]\n".format(name, flag, bits))
		else:
			self.stream.write("{}\n".format(name))

	def writeByte(self, byte):
		self.stream.write(" {}\n".format(byte))

	def writeWord(self, word):
		self.stream.write(" {}\n".format(word))
