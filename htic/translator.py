from __future__ import absolute_import

import io
from math import ceil
from math import log

from .writer import Writer


class BinaryTranslator(Writer):
	"""Translate Block object to binary TrueType code"""

	def __init__(self):
		self.array = None

	def translate(self, block):
		self.array = bytearray()
		block.write(self)
		return self.array

	def writeInstruction(self, name, opCode, flag, maxFlag):
		self.array.append(opCode + flag)

	def writeByte(self, byte):
		self.array.append(byte)

	def writeWord(self, word):
		value = word if word >= 0 else word + 2**16
		self.array.append((value & 0xFF00) >> 8)
		self.array.append(value & 0xFF)


class StringTranslator(Writer):
	"""Translate Block object to plain-text string"""

	def __init__(self):
		self.stream = None

	def translate(self, block):
		self.stream = io.BytesIO() # Instead of StringIO.StringIO
		block.write(self)
		return self.stream.getvalue()

	def writeInstruction(self, name, opCode, flag, maxFlag):
		if maxFlag > 0:
			width = int(ceil(log(maxFlag + 1, 2)))
			self.stream.write("{0}[{1:0>{2}b}]\n".format(name, flag, width))
		else:
			self.stream.write("{}\n".format(name))

	def writeByte(self, byte):
		self.stream.write(" {}\n".format(byte))

	def writeWord(self, word):
		self.stream.write(" {}\n".format(word))


# EXTEND Add new Translator class if necessary
