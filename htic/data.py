from __future__ import absolute_import
from .error import HumbleError


class Data(object):
	"""Manage parsed data"""

	def __init__(self):

		self.gasp = []
		"""[(int size, bool doGridfit, bool doGray, bool symSmoothing, bool symGridfit)]"""

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

		self.__cvtLookup = {}
		self.__functionLookup = {}
		self.__functionRecipeLookup = {}
		self.__voidFunctionList = []
		self.__storageLookup = {}
		self.__flagLookup = {}

	def addGasp(self, size, doGridFit, doGray, symSmoothing, symGridfit):
		self.gasp.append((size, doGridFit, doGray, symSmoothing, symGridfit))

	def addMaxp(self, name, value):
		self.maxp[name] = value

	def setFpgm(self, block):
		self.fpgm = block

	def setPrep(self, block):
		self.prep = block

	def addGlyph(self, name, block):
		self.glyphs[name] = block

	def addCvt(self, name, value):
		if name in self.__cvtLookup:
			raise HumbleError("Duplicate CVT identifier: {}".format(name))
		index = len(self.cvt)
		self.cvt.append(value)
		self.__cvtLookup[name] = index

	def addFunction(self, index, name, recipe, isVoid):
		if name in self.__functionLookup:
			raise HumbleError("Duplicate function identifier: {}".format(name))
		if index in self.__functionLookup.values():
			raise HumbleError("Duplicate function index: {} {}".format(index, name))
		self.__functionLookup[name] = index
		self.__functionRecipeLookup[name] = recipe
		if isVoid:
			self.__voidFunctionList.append(name)

	def addStorage(self, name):
		if name not in self.__storageLookup:
			index = len(self.__storageLookup)
			self.__storageLookup[name] = index

	def addFlag(self, name, value):
		self.__flagLookup[name] = value

	def getCvtIndex(self, name):
		try:
			return self.__cvtLookup[name]
		except KeyError:
			raise HumbleError("Undeclared CVT identifier: {}".format(name))

	def getFunctionIndex(self, name):
		try:
			return self.__functionLookup[name]
		except KeyError:
			raise HumbleError("Undeclared function identifier: {}".format(name))

	def getFunctionRecipe(self, name):
		try:
			return self.__functionRecipeLookup[name]
		except KeyError:
			return ()

	def isVoidFunction(self, name):
		return name in self.__voidFunctionList

	def getStorageIndex(self, name):
		try:
			return self.__storageLookup[name]
		except KeyError:
			raise HumbleError("Undeclared storage identifier: {}".format(name))

	def getFlagValue(self, name):
		try:
			return self.__flagLookup[name]
		except KeyError:
			raise HumbleError("Undeclared flag alias: {}".format(name))
