from .accumulator import Accumulator
from .writer import StringWriter
from .writer import BytesWriter


class Block:

	def __init__(self):
		self.last = None

	def __str__(self):
		writer = StringWriter()
		self.write(writer)
		return str(writer)

	def __bytes__(self):
		writer = BytesWriter()
		self.write(writer)
		return bytes(writer)

	def add(self, instruction):
		if self.last:
			if self.last.canMerge(instruction):
				self.last.merge(instruction)
				return
			else:
				instruction.chain(self.last)
		self.last = instruction

	def write(self, writer):
		if self.last:
			accumulator = Accumulator(writer)
			self.last.write(accumulator)
			accumulator.flush()
