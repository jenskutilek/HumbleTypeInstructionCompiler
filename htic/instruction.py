from __future__ import absolute_import

from .argument import IntegerArgument
from .block import Block
from .error import HumbleError


class Instruction(object):

	@staticmethod
	def newInstruction(name):
		if   name == "ABS":       return Instruction(name, 0x64, 0, ('getVAL',), True)
		elif name == "ADD":       return Instruction(name, 0x60, 0, ('getVAL', 'getVAL'), True)
		elif name == "ALIGNPTS":  return Instruction(name, 0x27, 0, ('getVAL', 'getVAL'), False)
		elif name == "ALIGNRP":   return LoopInstruction(name, 0x3C, 0, ('getVAL', 'getVALS'), False)
		elif name == "AND":       return Instruction(name, 0x5A, 0, ('getVAL', 'getVAL'), True)
		elif name == "CALL":      return CallInstruction(name, 0x2B, 0, ('CALL',), True, 1)
		elif name == "CEILING":   return Instruction(name, 0x67, 0, ('getVAL',), True)
		elif name == "CINDEX":    return Instruction(name, 0x25, 0, ('getVAL',), True)
		elif name == "CLEAR":     return Instruction(name, 0x22, 0, (), True) # special case for mightPush
		elif name == "DEBUG":     return Instruction(name, 0x4F, 0, ('getVAL',), False)
		elif name == "deltac":    return DeltaInstruction(name.upper(), None, 0, ('getCVT', 'getDELTA', 'getDELTAS'), False)
		elif name == "deltap":    return DeltaInstruction(name.upper(), None, 0, ('getVAL', 'getDELTA', 'getDELTAS'), False)
		elif name == "DEPTH":     return Instruction(name, 0x24, 0, (), True)
		elif name == "DUP":       return Instruction(name, 0x20, 0, (), True)
		elif name == "DIV":       return Instruction(name, 0x62, 0, ('getVAL', 'getVAL'), True)
		elif name == "EIF":       return Instruction(name, 0x59, 0, (), False)
		elif name == "ELSE":      return BlockInstruction(name, 0x1B, 0, (), False, ("EIF",))
		elif name == "ENDF":      return Instruction(name, 0x2D, 0, (), False)
		elif name == "EQ":        return Instruction(name, 0x54, 0, ('getVAL', 'getVAL'), True)
		elif name == "EVEN":      return Instruction(name, 0x57, 0, ('getVAL',), True)
		elif name == "FDEF":      return BlockInstruction(name, 0x2C, 0, ('setFUNC',), False, ("ENDF",))
		elif name == "FLIPOFF":   return Instruction(name, 0x4E, 0, (), False)
		elif name == "FLIPON":    return Instruction(name, 0x4D, 0, (), False)
		elif name == "FLIPPT":    return LoopInstruction(name, 0x80, 0, ('getVAL', 'getVALS'), False)
		elif name == "FLIPRGOFF": return Instruction(name, 0x82, 0, ('getVAL', 'getVAL'), False)
		elif name == "FLIPRGON":  return Instruction(name, 0x81, 0, ('getVAL', 'getVAL'), False)
		elif name == "FLOOR":     return Instruction(name, 0x66, 0, ('getVAL',), True)
		elif name == "GC":        return Instruction(name, 0x46, 1, ('getVAL',), True)
		elif name == "GETINFO":   return Instruction(name, 0x88, 0, ('getVAL',), True)
		elif name == "GFV":       return Instruction(name, 0x0D, 0, (), True)
		elif name == "GPV":       return Instruction(name, 0x0C, 0, (), True)
		elif name == "GT":        return Instruction(name, 0x52, 0, ('getVAL', 'getVAL'), True)
		elif name == "GTEQ":      return Instruction(name, 0x53, 0, ('getVAL', 'getVAL'), True)
		elif name == "IF":        return BlockInstruction(name, 0x58, 0, ('getVAL',), False, ("ELSE", "EIF"))
		elif name == "INSTCTRL":  return Instruction(name, 0x8E, 0, ('getVAL', 'getVAL'), False)
		elif name == "IP":        return LoopInstruction(name, 0x39, 0, ('getVAL', 'getVALS'), False)
		elif name == "ISECT":     return Instruction(name, 0x0F, 0, ('getVAL', 'getVAL', 'getVAL', 'getVAL', 'getVAL'), False)
		elif name == "IUP":       return Instruction(name, 0x30, 1, (), False)
		elif name == "JMPR":      return Instruction(name, 0x1C, 0, ('getVAL',), False)
		elif name == "JROF":      return Instruction(name, 0x79, 0, ('getVAL', 'getVAL'), False)
		elif name == "JROT":      return Instruction(name, 0x78, 0, ('getVAL', 'getVAL'), False)
		elif name == "LOOPCALL":  return CallInstruction(name, 0x2A, 0, ('getVAL', 'CALL'), True, 2)
		elif name == "LT":        return Instruction(name, 0x50, 0, ('getVAL', 'getVAL'), True)
		elif name == "LTEQ":      return Instruction(name, 0x51, 0, ('getVAL', 'getVAL'), True)
		elif name == "MAX":       return Instruction(name, 0x8B, 0, ('getVAL', 'getVAL'), True)
		elif name == "MD":        return Instruction(name, 0x49, 1, ('getVAL', 'getVAL'), True)
		elif name == "MDAP":      return Instruction(name, 0x2E, 1, ('getVAL',), False)
		elif name == "MDRP":      return Instruction(name, 0xC0, 31, ('getVAL',), False)
		elif name == "MIAP":      return Instruction(name, 0x3E, 1, ('getVAL', 'getCVT'), False)
		elif name == "MIN":       return Instruction(name, 0x8C, 0, ('getVAL', 'getVAL'), True)
		elif name == "MINDEX":    return Instruction(name, 0x26, 0, ('getVAL',), True)
		elif name == "MIRP":      return Instruction(name, 0xE0, 31, ('getVAL', 'getCVT'), False)
		elif name == "MPPEM":     return Instruction(name, 0x4B, 0, (), True)
		elif name == "MPS":       return Instruction(name, 0x4C, 0, (), True)
		elif name == "MSIRP":     return Instruction(name, 0x3A, 1, ('getVAL', 'getVAL'), False)
		elif name == "MUL":       return Instruction(name, 0x63, 0, ('getVAL', 'getVAL'), True)
		elif name == "NEG":       return Instruction(name, 0x65, 0, ('getVAL',), True)
		elif name == "NEQ":       return Instruction(name, 0x55, 0, ('getVAL', 'getVAL'), True)
		elif name == "NOT":       return Instruction(name, 0x5C, 0, ('getVAL',), True)
		elif name == "NROUND":    return Instruction(name, 0x6C, 3, ('getVAL',), True)
		elif name == "ODD":       return Instruction(name, 0x56, 0, ('getVAL',), True)
		elif name == "OR":        return Instruction(name, 0x5B, 0, ('getVAL', 'getVAL'), True)
		elif name == "POP":       return Instruction(name, 0x21, 0, (), True) # special case for mightPush
		elif name == "push":      return Instruction(None, None, 0, ('getVALS',), True)
		elif name == "RCVT":      return Instruction(name, 0x45, 0, ('getCVT',), True)
		elif name == "RDTG":      return Instruction(name, 0x7D, 0, (), False)
		elif name == "ROFF":      return Instruction(name, 0x7A, 0, (), False)
		elif name == "ROLL":      return Instruction(name, 0x8A, 0, (), True)
		elif name == "ROUND":     return Instruction(name, 0x68, 3, ('getVAL',), True)
		elif name == "RS":        return Instruction(name, 0x43, 0, ('getSTOR',), True)
		elif name == "RTDG":      return Instruction(name, 0x3D, 0, (), False)
		elif name == "RTG":       return Instruction(name, 0x18, 0, (), False)
		elif name == "RTHG":      return Instruction(name, 0x19, 0, (), False)
		elif name == "RUTG":      return Instruction(name, 0x7C, 0, (), False)
		elif name == "S45ROUND":  return Instruction(name, 0x77, 0, ('getVAL',), False)
		elif name == "SCANCTRL":  return Instruction(name, 0x85, 0, ('getVAL',), False)
		elif name == "SCANTYPE":  return Instruction(name, 0x8D, 0, ('getVAL',), False)
		elif name == "SCFS":      return Instruction(name, 0x48, 0, ('getVAL', 'getVAL'), False)
		elif name == "SCVTCI":    return Instruction(name, 0x1D, 0, ('getVAL',), False)
		elif name == "SDB":       return Instruction(name, 0x5E, 0, ('getVAL',), False)
		elif name == "SDPVTL":    return Instruction(name, 0x86, 1, ('getVAL', 'getVAL'), False)
		elif name == "SDS":       return Instruction(name, 0x5F, 0, ('getVAL',), False)
		elif name == "SFVFS":     return Instruction(name, 0x0B, 0, ('getVAL', 'getVAL'), False)
		elif name == "SFVTCA":    return Instruction(name, 0x04, 1, (), False)
		elif name == "SFVTL":     return Instruction(name, 0x08, 1, ('getVAL', 'getVAL'), False)
		elif name == "SFVTPV":    return Instruction(name, 0x0E, 0, (), False)
		elif name == "SHC":       return Instruction(name, 0x34, 1, ('getVAL',), False)
		elif name == "SHP":       return LoopInstruction(name, 0x32, 1, ('getVAL', 'getVALS'), False)
		elif name == "SHPIX":     return Instruction(name, 0x38, 0, ('getVAL', 'getVAL', 'getVALS'), False)
		elif name == "SHZ":       return Instruction(name, 0x36, 1, ('getVAL',), False)
		elif name == "SLOOP":     return Instruction(name, 0x17, 0, ('getVAL',), False)
		elif name == "SMD":       return Instruction(name, 0x1A, 0, ('getVAL',), False)
		elif name == "SPVFS":     return Instruction(name, 0x0A, 0, ('getVAL', 'getVAL'), False)
		elif name == "SPVTCA":    return Instruction(name, 0x02, 1, (), False)
		elif name == "SPVTL":     return Instruction(name, 0x06, 1, ('getVAL', 'getVAL'), False)
		elif name == "SROUND":    return Instruction(name, 0x76, 0, ('getVAL',), False)
		elif name == "SRP0":      return Instruction(name, 0x10, 0, ('getVAL',), False)
		elif name == "SRP1":      return Instruction(name, 0x11, 0, ('getVAL',), False)
		elif name == "SRP2":      return Instruction(name, 0x12, 0, ('getVAL',), False)
		elif name == "SSW":       return Instruction(name, 0x1F, 0, ('getVAL',), False)
		elif name == "SSWCI":     return Instruction(name, 0x1E, 0, ('getVAL',), False)
		elif name == "SUB":       return Instruction(name, 0x61, 0, ('getVAL', 'getVAL'), True)
		elif name == "SVTCA":     return Instruction(name, 0x00, 1, (), False)
		elif name == "SWAP":      return Instruction(name, 0x23, 0, (), True)
		elif name == "SZP0":      return Instruction(name, 0x13, 0, ('getVAL',), False)
		elif name == "SZP1":      return Instruction(name, 0x14, 0, ('getVAL',), False)
		elif name == "SZP2":      return Instruction(name, 0x15, 0, ('getVAL',), False)
		elif name == "SZPS":      return Instruction(name, 0x16, 0, ('getVAL',), False)
		elif name == "UTP":       return Instruction(name, 0x29, 0, ('getVAL',), False)
		elif name == "void":      return BlockInstruction("FDEF", 0x2C, 0, ('setVOID',), False, ("ENDF",))
		elif name == "WCVTF":     return Instruction(name, 0x70, 0, ('getCVT', 'getVAL'), False)
		elif name == "WCVTP":     return Instruction(name, 0x44, 0, ('getCVT', 'getVAL'), False)
		elif name == "WS":        return Instruction(name, 0x42, 0, ('setSTOR', 'getVAL'), False)
		else:
			raise HumbleError("Unsupported instruction: {}".format(name))

	@staticmethod
	def newSubBlockInstruction(block):
		instruction = SubBlockInstruction()
		instruction.block = block
		return instruction

	@staticmethod
	def newOperationInstruction(symbol):
		if   symbol == "==": return Instruction.newInstruction("EQ")
		elif symbol == "!=": return Instruction.newInstruction("NEQ")
		elif symbol == ">=": return Instruction.newInstruction("GTEQ")
		elif symbol == ">" : return Instruction.newInstruction("GT")
		elif symbol == "<=": return Instruction.newInstruction("LTEQ")
		elif symbol == "<" : return Instruction.newInstruction("LT")
		elif symbol == "+" : return Instruction.newInstruction("ADD")
		elif symbol == "-" : return Instruction.newInstruction("SUB")
		elif symbol == "*" : return Instruction.newInstruction("MUL")
		elif symbol == "/" : return Instruction.newInstruction("DIV")
		elif symbol == "or": return Instruction.newInstruction("OR")
		elif symbol == "and": return Instruction.newInstruction("AND")
		else:
			raise HumbleError("Invalid operator symbol: {}".format(symbol))

	@staticmethod
	def _newDeltaInstruction(name):
		if   name == "DELTAC1": return Instruction(name, 0x73, 0, None, False)
		elif name == "DELTAC2": return Instruction(name, 0x74, 0, None, False)
		elif name == "DELTAC3": return Instruction(name, 0x75, 0, None, False)
		elif name == "DELTAP1": return Instruction(name, 0x5D, 0, None, False)
		elif name == "DELTAP2": return Instruction(name, 0x71, 0, None, False)
		elif name == "DELTAP3": return Instruction(name, 0x72, 0, None, False)
		else:
			raise NameError(name)

	def __init__(self, name, opCode, maxFlag, recipe, mightPush):
		self.name = name
		self.opCode = opCode
		self.flag = 0
		self.maxFlag = maxFlag
		self.recipe = recipe
		self.mightPush = mightPush

		self.pre = None
		self.arguments = []
		self.post = None

	def setFlag(self, flag):
		if flag <= self.maxFlag:
			self.flag = flag
		else:
			raise HumbleError("Invalid flag value for {}: {}".format(self.name, flag))

	def add(self, argument):
		self.arguments.append(argument)

	def canMerge(self, other):
		return False

	def merge(self, other):
		raise TypeError

	def canChain(self):
		return True

	def canPush(self):
		return self.mightPush or self.pre or (self.post and self.post.canPush())

	def chain(self, other):
		if self.pre:
			self.pre.chain(other)
		else:
			for argument in self.arguments:
				if argument.canChain():
					argument.chain(other)
					return
			if other.canPush():
				self.pre = other
			elif self.post:
				self.post.chain(other)
			else:
				self.post = other

	def write(self, accumulator):
		if self.pre:
			self.pre.write(accumulator)
		for argument in self.arguments:
			argument.write(accumulator)
		if self.post:
			self.post.write(accumulator)
		if self.name:
			self._writeName(accumulator)

	def _writeName(self, accumulator):
		accumulator.writeInstruction(self.name, self.opCode, self.flag, self.maxFlag)


class BlockInstruction(Instruction):

	def __init__(self, name, opCode, maxFlag, recipe, mightPush, stops):
		Instruction.__init__(self, name, opCode, maxFlag, recipe, mightPush)
		self.stops = stops
		self.block = Block()

	def canMerge(self, other):
		if isinstance(self.block.last, BlockInstruction):
			return True
		elif self.stops:
			return other.name not in self.stops
		else:
			return False

	def merge(self, other):
		self.block.add(other)

	def write(self, accumulator):
		Instruction.write(self, accumulator)
		self.block.write(accumulator.writer)


class CallInstruction(Instruction):

	def __init__(self, name, opCode, maxFlag, recipe, mightPush, insertIndex):
		Instruction.__init__(self, name, opCode, maxFlag, recipe, mightPush)
		self.insertIndex = insertIndex

	def add(self, argument):
		if len(self.arguments) >= self.insertIndex:
			self.arguments.insert(-self.insertIndex, argument)
		else:
			self.arguments.append(argument)


class DeltaInstruction(Instruction):

	def __init__(self, name, opCode, maxFlag, recipe, mightPush):
		Instruction.__init__(self, name, opCode, maxFlag, recipe, mightPush)
		self.target = None

	def add(self, argument):
		if self.target is not None:
			argument.target = self.target
			self.arguments.append(argument)
		else:
			self.target = argument.value

	def canMerge(self, other):
		return other.name == self.name

	def merge(self, other):
		self.arguments += other.arguments

	def write(self, accumulator):
		self.arguments.sort()

		deltaBase = self.arguments[0].ppem
		variant = 1
		variantBase = deltaBase
		count = 0

		block = Block()
		block.add(self.__makeSDB(deltaBase))
		delta = self.__makeDELTA(variant)

		for argument in self.arguments:
			if argument.ppem > variantBase + 15:
				delta.add(IntegerArgument(count))
				block.add(delta)
				count = 0

				if argument.ppem > deltaBase + 47:
					deltaBase = argument.ppem
					variant = 1
					variantBase = deltaBase
					block.add(self.__makeSDB(deltaBase))
				else:
					variant = ((argument.ppem - deltaBase) >> 4) + 1
					variantBase = deltaBase + ((variant-1) << 4)

				delta = self.__makeDELTA(variant)

			argument.base = variantBase
			delta.add(argument)
			count += 1

		delta.add(IntegerArgument(count))
		block.add(delta)

		if self.pre:
			self.pre.write(accumulator)
		elif self.post:
			block.last.chain(self.post)
		block.last.write(accumulator)

	def __makeDELTA(self, variant):
		return Instruction._newDeltaInstruction(self.name + str(variant))

	def __makeSDB(self, base):
		sdb = Instruction.newInstruction("SDB")
		sdb.add(IntegerArgument(base))
		return sdb


class LoopInstruction(Instruction):

	LIMIT = 4

	def __init__(self, name, opCode, maxFlag, recipe, mightPush):
		Instruction.__init__(self, name, opCode, maxFlag, recipe, mightPush)

	def canMerge(self, other):
		return other.name == self.name and other.flag == self.flag and \
			self.arguments and other.arguments

	def merge(self, other):
		self.arguments += other.arguments

	def write(self, accumulator):
		block = Block()

		if len(self.arguments) >= self.LIMIT:
			sloop = Instruction.newInstruction("SLOOP")
			sloop.add(IntegerArgument(len(self.arguments)))
			block.add(sloop)

		push = Instruction.newInstruction("push")
		push.arguments = self.arguments
		block.add(push)

		if self.pre:
			self.pre.write(accumulator)
		elif self.post:
			block.last.chain(self.post)
		block.last.write(accumulator)

		args = len(self.arguments)
		for _ in range(args if args and args < self.LIMIT else 1):
			Instruction._writeName(self, accumulator)


class SubBlockInstruction(Instruction):

	def __init__(self):
		Instruction.__init__(self, None, None, None, (), False)
		self.block = Block()

	def write(self, accumulator):
		Instruction.write(self, accumulator)
		self.block.write(accumulator.writer)
