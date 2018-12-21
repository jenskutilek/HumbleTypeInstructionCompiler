class Argument:

	def canChain(self):
		return False

	def chain(self, other):
		raise TypeError


class IntegerArgument(Argument):

	def __init__(self, value):
		self.value = value

	def write(self, accumulator):
		accumulator.writeArgument(self.value)


class DeltaArgument(Argument):

	def __init__(self, ppem, steps):
		self.ppem = ppem
		self.steps = steps
		self.target = None
		self.base = None

	def __lt__(self, other):
		if self.ppem == other.ppem:
			return self.steps < other.steps
		else:
			return self.ppem < other.ppem

	def write(self, accumulator):
		offset = self.ppem - self.base
		magnitude = self.steps + 8 if self.steps < 0 else self.steps + 7
		delta = (offset * 16) + magnitude
		accumulator.writeArgument(delta)
		accumulator.writeArgument(self.target)
