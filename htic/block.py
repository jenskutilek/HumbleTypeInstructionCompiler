from __future__ import absolute_import
from .accumulator import Accumulator



class Block(object):

	def __init__(self):
		self.last = None


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
