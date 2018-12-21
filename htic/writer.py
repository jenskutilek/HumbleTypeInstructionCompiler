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
