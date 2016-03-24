from __future__ import absolute_import
from . import helper

from htic.error import HumbleError

import unittest



class ParserError(unittest.TestCase):

	# maxp
	def testUnknownMaxpIdentifier(self):
		with self.assertRaises(HumbleError):
			helper.getData("maxp{ 16 maxInstructionDefs \n}")

	# uint
	def testInvalidUnsignedIntLow(self):
		with self.assertRaises(HumbleError):
			helper.getData("maxp{ -1 maxStackElements \n}")

	def testInvalidUnsignedIntHeigh(self):
		with self.assertRaises(HumbleError):
			helper.getData("maxp{ 65536 maxStackElements \n}")

	def testInvalidUnsignedIntToken(self):
		with self.assertRaises(HumbleError):
			helper.getData("maxp{ maxStackElements 1 \n}")

	# num
	def testInvalidNumBinToken(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 0b2")

	def testInvalidNumHexToken(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 0xG")

	def testInvalidNumHexHigh(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 0x10000")

	def testInvalidNumF26d6Token(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 0.A")

	def testInvalidNumF2d14Token(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 0..A")

	def testInvalidNumIntLow(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push -32769")

	def testInvalidNumIntHigh(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push 32768")

	def testInvalidNumIntToken(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("push foo")

	# delta
	def testInvalidDeltaModifierPpemLow(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 -1-8")

	def testInvalidDeltaModifierPpemHigh(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 32768-8")

	def testInvalidDeltaModifierPpemToken(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 foo-8")

	def testInvalidDeltaModifierSign(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 12u8")

	def testInvalidDeltaModifierStepZero(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 12-0")

	def testInvalidDeltaModifierStepLow(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 12-9")

	def testInvalidDeltaModifierStepHeigh(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 12+9")

	def testInvalidDeltaModifierStepToken(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("DELTAP 8 12+foo")

	# bits
	def testInvalidBitValue(self):
		with self.assertRaises(HumbleError):
			helper.getData("flags{ foo 2 \n}")

	# id
	def testInvalidId(self):
		with self.assertRaises(HumbleError):
			helper.getData("cvt{ 0 a-b \n}")

	# skip
	def testMissingToken(self):
		with self.assertRaises(HumbleError):
			helper.getData("cvt  0 6ar \n}")



class RegistryError(unittest.TestCase):

	def testDuplicateCvt(self):
		with self.assertRaises(HumbleError):
			helper.getData("cvt{ 0 foo \n 1 foo \n}")

	def testDuplicateFunction(self):
		with self.assertRaises(HumbleError):
			helper.getData("fpgm{ FDEF foo \n POP \n ENDF \n FDEF foo \n POP \n ENDF \n}")

	def testUndeclaredCvt(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("MIAP 8 foo")

	def testUndeclaredFunction(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("CALL foo")

	def testUndeclaredStorage(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("RS foo")

	def testUndeclaredFlag(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("IUP+foo")



class InstructionError(unittest.TestCase):

	def testUnsupportedInstruction(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("IDEF 0")

	def testInvalidOperatorSymbol(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("IF (2 % 3) \n EIF")

	def testInvalidFlagValue(self):
		with self.assertRaises(HumbleError):
			helper.toBytes("IUP+10")

