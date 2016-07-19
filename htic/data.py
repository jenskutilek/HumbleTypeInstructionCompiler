from __future__ import absolute_import
from .error import HumbleError



class Data(object):
	"""Manage parsed data"""

	def __init__(self):

		# Public

		self.gasp = []
		"""[(int size, bool doGridfit, bool doGray)]"""

		self.maxp = {}
		"""{string name : int value}"""

		self.cvt = []
		"""[int]"""

		self.fpgm = None
		"""Block"""

		self.prep = None
		"""Block"""

		self.glyphs = {}
		"""{string name : Block block}"""

		# Private

		self.__cvtLookup = {}
		self.__functionLookup = {}
		self.__voidFunctionList = []
		self.__storageLookup = {}
		self.__flagLookup = {}


	def addGasp(self, size, doGridFit, doGray):
		self.gasp.append((size, doGridFit, doGray))


	def addMaxp(self, name, value):
		self.maxp[name] = value


	def setFpgm(self, block):
		self.fpgm = block


	def setPrep(self, block):
		self.prep = block


	def addGlyph(self, name, block):
		self.glyphs[name] = block


	def addCvt(self, name, value):
		if name not in self.__cvtLookup:
			index = len(self.cvt)
			self.cvt.append(value)
			self.__cvtLookup[name] = index
		else:
			raise HumbleError("Duplicate CVT identifier: {}".format(name))


	def addFunction(self, name):
		if name not in self.__functionLookup:
			index = len(self.__functionLookup)
			self.__functionLookup[name] = index
		else:
			raise HumbleError("Duplicate function identifier: {}".format(name))


	def addVoidFunction(self, name):
		self.addFunction(name)
		self.__voidFunctionList.append(name)


	def addStorage(self, name):
		if name not in self.__storageLookup:
			index = len(self.__storageLookup)
			self.__storageLookup[name] = index


	def addFlag(self, name, value):
		self.__flagLookup[name] = value


	def getCvt(self, name):
		try:
			return self.__cvtLookup[name]
		except KeyError:
			raise HumbleError("Undeclared CVT identifier: {}".format(name))


	def getFunction(self, name):
		try:
			return self.__functionLookup[name]
		except KeyError:
			raise HumbleError("Undeclared function identifier: {}".format(name))


	def isVoidFunction(self, name):
		return name in self.__voidFunctionList


	def getStorage(self, name):
		try:
			return self.__storageLookup[name]
		except KeyError:
			raise HumbleError("Undeclared storage identifier: {}".format(name))


	def getFlag(self, name):
		try:
			return self.__flagLookup[name]
		except KeyError:
			raise HumbleError("Undeclared flag alias: {}".format(name))
