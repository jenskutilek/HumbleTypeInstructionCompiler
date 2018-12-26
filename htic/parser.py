import re

from .argument import IntegerArgument
from .argument import DeltaArgument
from .block import Block
from .data import Data
from .error import HumbleError
from .instruction import Instruction
from .tokenizer import Tokenizer


def parseFile(sourceFile):
	with open(sourceFile) as stream:
		parser = Parser()
		return parser.parse(stream)


class Parser:

	def __init__(self):
		self.tokenizer = None
		self.data = None

	def parse(self, stream):
		self.tokenizer = Tokenizer(stream)
		self.data = Data()
		try:
			self.__root()
		except HumbleError as e:
			e.position = self.tokenizer.position
			raise
		return self.data

	# The following methods mirror the
	# grammar from doc/grammar.md

	def __root(self):
		self.__ws()
		name = self.tokenizer.peek()
		while name:
			if   name == "gasp" : self.__gasp()
			elif name == "maxp" : self.__maxp()
			elif name == "cvt"  : self.__cvt()
			elif name == "flags": self.__flags()
			elif name == "fpgm" : self.__fpgm()
			elif name == "prep" : self.__prep()
			else: self.__glyph()
			name = self.tokenizer.peek()

	def __gasp(self):
		self.__skip("gasp")
		self.__open()
		while self.tokenizer.peek() != "}":
			self.__ws()
			size = self.__uint()
			doGridFit = False
			doGray = False
			symSmoothing = False
			symGridfit = False
			while self.tokenizer.peek() != "\n":
				flag = self.tokenizer.get()
				if   flag == "doGridfit"   : doGridFit = True
				elif flag == "doGray"      : doGray = True
				elif flag == "symSmoothing": symSmoothing = True
				elif flag == "symGridfit"  : symGridfit = True
				else:
					raise HumbleError("Unknown gasp flag: {}".format(flag))
			self.data.addGasp(size, doGridFit, doGray, symSmoothing, symGridfit)
			self.__nl()
		self.__close()

	def __maxp(self):
		self.__skip("maxp")
		self.__open()
		while self.tokenizer.peek() != "}":
			self.__ws()
			value = self.__uint()
			name = self.__maxpname()
			self.data.addMaxp(name, value)
			self.__nl()
		self.__close()

	def __maxpname(self):
		token = self.tokenizer.get()
		if token == "maxStackElements" or \
		   token == "maxFunctionDefs" or \
		   token == "maxStorage" or \
		   token == "maxZones" or \
		   token == "maxTwilightPoints":
			return token
		else:
			raise HumbleError("Unknown maxp identifier: {}".format(token))

	def __cvt(self):
		self.__skip("cvt")
		self.__open()
		while self.tokenizer.peek() != "}":
			self.__ws()
			value = self.__num().value
			name = self.__id()
			self.data.addCvt(name, value)
			self.__nl()
		self.__close()

	def __flags(self):
		self.__skip("flags")
		self.__open()
		while self.tokenizer.peek() != "}":
			self.__ws()
			name = self.__id()
			value = self.__bits()
			self.data.addFlag(name, value)
			self.__nl()
		self.__close()

	def __fpgm(self):
		self.__skip("fpgm")
		self.data.setFpgm(self.__block())

	def __prep(self):
		self.__skip("prep")
		self.data.setPrep(self.__block())

	def __glyph(self):
		name = self.__id()
		block = self.__block()
		self.data.addGlyph(name, block)

	def __block(self):
		block = Block()
		self.__open()
		while self.tokenizer.peek() != "}":
			self.__ws()
			block.add(self.__instr())
			self.__nl()
		self.__close()
		return block

	def __open(self):
		self.__ws()
		self.__skip("{")
		self.__ws()

	def __close(self):
		self.__ws()
		self.__skip("}")
		self.__ws()

	def __instr(self):
		instr = self.tokenizer.get()
		instruction = Instruction.newInstruction(instr)
		instruction.setFlag(self.__flag())
		self.__recipe(instruction)
		return instruction

	def __flag(self):
		flag = 0
		if self.tokenizer.peek() == "[":
			self.__skip("[")
			flag = self.__flagval()
			self.__skip("]")
		return flag

	def __flagval(self):
		try:
			self.tokenizer.mark()
			return self.__bits()
		except HumbleError:
			self.tokenizer.rewind()
			name = self.__id()
			return self.data.getFlagValue(name)
		finally:
			self.tokenizer.unmark()

	def __val(self):
		if self.tokenizer.peek() == "(":
			self.__skip("(")
			try:
				self.tokenizer.mark()
				val = self.__instr()
			except HumbleError:
				self.tokenizer.rewind()
				val = self.__operation()
			finally:
				self.tokenizer.unmark()
			self.__skip(")")
			return val
		else:
			return self.__num()

	def __operation(self):
		argument = self.__val()
		instruction = Instruction.newOperationInstruction(self.tokenizer.get())
		instruction.add(argument)
		argument = self.__val()
		instruction.add(argument)
		return instruction

	def __nl(self):
		self.__skip("\n")
		self.__ws()

	def __ws(self):
		while self.tokenizer.peek() == "\n":
			self.tokenizer.get()

	def __id(self):
		token = self.tokenizer.get()
		if re.match("[0-9A-Za-z_\.]+$", token):
			return token
		else:
			raise HumbleError("Invalid identifier: {}".format(token))

	def __num(self):
		token = self.tokenizer.get()
		if token == "+" or token == "-":
			token += self.tokenizer.get()
		try:
			if token.find("0x") == 0 or token.find("0b") == 0:
				value = int(token, 0)
				if value >= 2**15 and value < 2**16:
					value -= 2**16
			elif token.find(":") >= 0:
				value = int(round(float(token.replace(":", ".")) * 2**14))
			elif token.find(".") >= 0:
				value = int(round(float(token) * 2**6))
			else:
				value = int(token)

			if value >= -2**15 and value < 2**15:
				return IntegerArgument(value)
		except ValueError:
			pass
		raise HumbleError("Invalid numeric argument: {}".format(token))

	def __uint(self):
		token = self.tokenizer.get()
		try:
			value = int(token)
			if value >= 0 and value < 2**16:
				return value
		except ValueError:
			pass
		raise HumbleError("Invalid unsigned integer: {}".format(token))

	def __bits(self):
		token = self.tokenizer.get()
		try:
			return int(token, 2)
		except ValueError:
			raise HumbleError("Invalid bit value: {}".format(token))

	def __delta(self):
		ppemToken = self.tokenizer.get()
		signToken = self.tokenizer.get()
		stepsToken = self.tokenizer.get()
		try:
			ppem = int(ppemToken)
			steps = int(signToken + stepsToken)
			if ppem >= 0 and ppem < 2**15 and steps != 0 and abs(steps) <= 8:
				return DeltaArgument(ppem, steps)
		except ValueError:
			pass
		raise HumbleError("Invalid delta modifier: {}{}{}".format(ppemToken, signToken, stepsToken))

	# Helper methods

	def __recipe(self, instruction):
		if self.tokenizer.peek() == "\n" or \
		   self.tokenizer.peek() == ")":
			return
		for item in instruction.recipe:
			if item == 'getCVT':
				name = self.__id()
				index = self.data.getCvtIndex(name)
				instruction.add(IntegerArgument(index))
			elif item == 'setSTOR':
				name = self.__id()
				self.data.addStorage(name)
				index = self.data.getStorageIndex(name)
				instruction.add(IntegerArgument(index))
			elif item == 'getSTOR':
				name = self.__id()
				index = self.data.getStorageIndex(name)
				instruction.add(IntegerArgument(index))
			elif item == 'setFUNC' or \
			     item == 'setVOID':
				index = self.__uint()
				name = self.__id()
				recipe = self.__parameters()
				self.data.addFunction(index, name, recipe, item == 'setVOID')
				instruction.add(IntegerArgument(index))
			elif item == 'getFUNC':
				name = self.__id()
				index = self.data.getFunctionIndex(name)
				instruction.add(IntegerArgument(index))
			elif item == 'CALL':
				name = self.__id()
				index = self.data.getFunctionIndex(name)
				recipe = self.data.getFunctionRecipe(name)
				instruction.add(IntegerArgument(index))
				instruction.recipe = recipe
				if instruction.name == "LOOPCALL":
					instruction.recipe *= instruction.arguments[-2].value
				if self.data.isVoidFunction(name):
					instruction.spoilsStack = False
				# Parse new recipe
				self.__recipe(instruction)
				return
			elif item == 'getVAL':
				value = self.__val()
				instruction.add(value)
			elif item == 'getVALS':
				while self.tokenizer.peek() != "\n" and \
				      self.tokenizer.peek() != ")":
					argument = self.__val()
					instruction.add(argument)
			elif item == 'getDELTA':
				delta = self.__delta()
				instruction.add(delta)
			elif item == 'getDELTAS':
				while self.tokenizer.peek() != "\n" and \
				      self.tokenizer.peek() != ")":
					delta = self.__delta()
					instruction.add(delta)
			else:
				raise ValueError("Invalid recipe item: {}".format(item))

	def __parameters(self):
		parameters = []
		while self.tokenizer.peek() != "\n" and \
		      self.tokenizer.peek() != ")":
			parameters.append(self.__parameter())
		return tuple(parameters)

	def __parameter(self):
		token = self.tokenizer.get()
		if   token.startswith("val"):  return 'getVAL'
		elif token.startswith("pt"):   return 'getVAL'
		elif token.startswith("cvt"):  return 'getCVT'
		elif token.startswith("func"): return 'getFUNC'
		elif token.startswith("stor"): return 'getSTOR'
		else:
			raise HumbleError("Invalid parameter: {}".format(token))

	def __skip(self, string):
		token = self.tokenizer.get()
		if token != string:
			raise HumbleError("Expected: {} Got: {}".format(string, token))
