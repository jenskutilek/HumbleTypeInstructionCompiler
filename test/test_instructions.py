from __future__ import absolute_import
from . import helper

import unittest



class FlagTest(unittest.TestCase):

	EXPECTED = bytearray([0xB0,8,0xDE,0x31])

	def testZero(self):
		code = helper.toBytes("MDRP 8 \n IUP")
		self.assertEqual(code, bytearray([0xB0,8,0xC0,0x30]))

	def testBinaryBrackets(self):
		code = helper.toBytes("MDRP[11110] 8 \n IUP[1]")
		self.assertEqual(code, FlagTest.EXPECTED)

	def testBinaryPlus(self):
		code = helper.toBytes("MDRP+11110 8 \n IUP+1")
		self.assertEqual(code, FlagTest.EXPECTED)

	def testAliasBrackets(self):
		code = helper.toBytes("MDRP[m] 8 \n IUP[x]", helper.FLAGS)
		self.assertEqual(code, FlagTest.EXPECTED)

	def testAliasPlus(self):
		code = helper.toBytes("MDRP+m 8 \n IUP+x", helper.FLAGS)
		self.assertEqual(code, FlagTest.EXPECTED)



class ArgumentTest(unittest.TestCase):

	def testConsolidation2(self):
		code = helper.toBytes("ISECT 1 2 3 4 5 \n ALIGNPTS 6 7")
		self.assertEqual(code, bytearray([0xB6,6,7,1,2,3,4,5,0x0F,0x27]))

	def testConsolidation3(self):
		code = helper.toBytes("ISECT 1 2 3 4 5 \n MDAP 6 \n MDAP 7")
		self.assertEqual(code, bytearray([0xB6,7,6,1,2,3,4,5,0x0F,0x2E,0x2E]))

	def testConsolidationBreak(self):
		code = helper.toBytes("ISECT 1 2 3 4 5 \n MPPEM \n ALIGNPTS 6 7")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,5,0x0F,0x4B,0xB1,6,7,0x27]))

	def testPushConsolidation(self):
		code = helper.toBytes("push 1 2 \n push 3 4 \n push 5 6")
		self.assertEqual(code, bytearray([0xB5,1,2,3,4,5,6]))

	def testPushConsolidationBreak(self):
		code = helper.toBytes("push 1 \n SWAP \n push 2 3")
		self.assertEqual(code, bytearray([0xB0,1,0x23,0xB1,2,3]))



class LoopTest(unittest.TestCase):

	def testALIGNRP1(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 \n RTG")
		self.assertEqual(code, bytearray([0xB0,1,0x18,0x3C,0x18]))

	def testALIGNRP2(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 2 \n RTG")
		self.assertEqual(code, bytearray([0xB1,1,2,0x18,0x3C,0x3C,0x18]))

	def testALIGNRP3(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 2 3 \n RTG")
		self.assertEqual(code, bytearray([0xB2,1,2,3,0x18,0x3C,0x3C,0x3C,0x18]))

	def testALIGNRP4(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 2 3 4 \n RTG")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,4,0x18,0x17,0x3C,0x18]))

	def testALIGNRPMerge(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 2 \n ALIGNRP 3 4 \n RTG")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,4,0x18,0x17,0x3C,0x18]))

	def testALIGNRPMergeLoops(self):
		code = helper.toBytes("RTG \n ALIGNRP 1 2 3 \n ALIGNRP 4 5 6 \n RTG")
		self.assertEqual(code, bytearray([0xB6,1,2,3,4,5,6,6,0x18,0x17,0x3C,0x18]))

	def testFLIPPT3(self):
		code = helper.toBytes("FLIPPT 1 2 3 4")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,4,0x17,0x80]))

	def testIP3(self):
		code = helper.toBytes("IP 1 2 3 4")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,4,0x17,0x39]))

	def testSHP3(self):
		code = helper.toBytes("SHP 1 2 3 4")
		self.assertEqual(code, bytearray([0xB4,1,2,3,4,4,0x17,0x32]))



class ConversionTest(unittest.TestCase):

	EXPECTED = bytearray([0xB2,0x00,0xff,0x40,0xBB,0xff,0xc0,0x7f,0xff,0x80,0x00,0xff,0xff])

	def testInt(self):
		code = helper.toBytes("push 0 255 +64 -64 32767 -32768 -1")
		self.assertEqual(code, ConversionTest.EXPECTED)

	def testF26d6(self):
		code = helper.toBytes("push 0.0 3.984375 +1.0 -1.0 511.984375 -512.0 -0.015625")
		self.assertEqual(code, ConversionTest.EXPECTED)

	def testF2d14(self):
		code = helper.toBytes("push 0..0 0..015563965 +0..00390625 -0..00390625 1..999938965 -2..0 -0..000061035")
		self.assertEqual(code, ConversionTest.EXPECTED)

	def testHex(self):
		code = helper.toBytes("push 0x0 0xff 0x40 0xffc0 0x7fff 0x8000 0xffff")
		self.assertEqual(code, ConversionTest.EXPECTED)

	def testBin(self):
		code = helper.toBytes("push 0b0 0b11111111 0b1000000 0b1111111111000000 0b0111111111111111 0b1000000000000000 0b1111111111111111")
		self.assertEqual(code, ConversionTest.EXPECTED)



class CommentTest(unittest.TestCase):

	def testComment(self):
		code = helper.toBytes("MPPEM#SDB 8 \n#SDS 2")
		self.assertEqual(code, bytearray([0x4B]))



class IdentifierTest(unittest.TestCase):

	def testCvt(self):
		code = helper.toBytes("MIAP 8 cvt1 \n MIAP 8 cvt2", helper.CVT)
		self.assertEqual(code, bytearray([0xB3,8,2,8,1,0x3E,0x3E]))

	def testFunction(self):
		code = helper.toBytes("CALL func0 \n CALL func1", helper.FPGM)
		self.assertEqual(code, bytearray([0xB0,0,0x2B,0xB0,1,0x2B]))

	def testStorageNew(self):
		code = helper.toBytes("WS stor0 7 \n WS stor1 8 \n RS stor0 \n RS stor1")
		self.assertEqual(code, bytearray([0xB4,0,1,8,0,7,0x42,0x42,0x43,0xB0,1,0x43]))

	def testStorageExisting(self):
		code = helper.toBytes("WS stor0 7 \n WS stor0 8 \n RS stor0")
		self.assertEqual(code, bytearray([0xB4,0,0,8,0,7,0x42,0x42,0x43]))



class NestingTest(unittest.TestCase):

	def testNestedLeft(self):
		code = helper.toBytes("IF ((NEG 7) == 8) \n EIF")
		self.assertEqual(code, bytearray([0xB0,7,0x65,0xB0,8,0x54,0x58,0x59]))

	def testNestedRight(self):
		code = helper.toBytes("IF (8 == (NEG 7)) \n EIF")
		self.assertEqual(code, bytearray([0xB1,8,7,0x65,0x54,0x58,0x59]))

	def testNestedBoth(self):
		code = helper.toBytes("IF ((NEG 7) == (NEG 8)) \n EIF")
		self.assertEqual(code, bytearray([0xB0,7,0x65,0xB0,8,0x65,0x54,0x58,0x59]))



class OperatorTest(unittest.TestCase):

	def testEq(self):
		code = helper.toBytes("IF (7 == 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x54,0x58,0x59]))

	def testNeq(self):
		code = helper.toBytes("IF (7 != 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x55,0x58,0x59]))

	def testGteq(self):
		code = helper.toBytes("IF (7 >= 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x53,0x58,0x59]))

	def testGt(self):
		code = helper.toBytes("IF (7 > 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x52,0x58,0x59]))

	def testLteq(self):
		code = helper.toBytes("IF (7 <= 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x51,0x58,0x59]))

	def testLt(self):
		code = helper.toBytes("IF (7 < 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x50,0x58,0x59]))

	def testAdd(self):
		code = helper.toBytes("IF (7 + 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x60,0x58,0x59]))

	def testSub(self):
		code = helper.toBytes("IF (7 - 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x61,0x58,0x59]))

	def testOptimizingMul(self):
		code = helper.toBytes("IF (7 * 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x63,0x58,0x59]))

	def testDiv(self):
		code = helper.toBytes("IF (7 / 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x62,0x58,0x59]))

	def testOptimizingOR(self):
		code = helper.toBytes("IF (7 or 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x5B,0x58,0x59]))

	def testOptimizingAND(self):
		code = helper.toBytes("IF (7 and 8) \n EIF")
		self.assertEqual(code, bytearray([0xB1,7,8,0x5A,0x58,0x59]))



class PushTest(unittest.TestCase):

	def testPUSHB1(self):
		code = helper.toBytes("push 1")
		self.assertEqual(code, bytearray([0xB0,1]))

	def testPUSHB8(self):
		code = helper.toBytes("push 1 2 3 4 5 6 7 8")
		self.assertEqual(code, bytearray([0xB7,1,2,3,4,5,6,7,8]))

	def testNPUSHB9(self):
		code = helper.toBytes("push 1 2 3 4 5 6 7 8 9")
		self.assertEqual(code, bytearray([0x40,9,1,2,3,4,5,6,7,8,9]))

	def testNPUSHB256(self):
		code = "push"
		expected = bytearray([0x40, 255])
		for i in range(255):
			code += " 1"
			expected.append(1)
		code += " 2"
		expected.append(0xB0)
		expected.append(2)
		self.assertEqual(helper.toBytes(code), expected)

	def testPUSHW1(self):
		code = helper.toBytes("push -1")
		self.assertEqual(code, bytearray([0xB8,0xff,0xff]))

	def testPUSHW8(self):
		code = helper.toBytes("push -1 -2 -3 -4 -5 -6 -7 -8")
		self.assertEqual(code, bytearray([0xBF,0xff,0xff,0xff,0xfe,0xff,0xfd,0xff,0xfc,0xff,0xfb,0xff,0xfa,0xff,0xf9,0xff,0xf8]))

	def testNPUSHW9(self):
		code = helper.toBytes("push -1 -2 -3 -4 -5 -6 -7 -8 -9")
		self.assertEqual(code, bytearray([0x41,9,0xff,0xff,0xff,0xfe,0xff,0xfd,0xff,0xfc,0xff,0xfb,0xff,0xfa,0xff,0xf9,0xff,0xf8,0xff,0xf7]))

	def testNPUSHW256(self):
		code = "push"
		expected = bytearray([0x41, 255])
		for i in range(255):
			code += " -1"
			expected.append(0xff)
			expected.append(0xff)
		code += " -2"
		expected.append(0xB8)
		expected.append(0xff)
		expected.append(0xfe)
		self.assertEqual(helper.toBytes(code), expected)



class CallTest(unittest.TestCase):

	def testCALL(self):
		code = helper.toBytes("CALL func1 2", helper.FPGM)
		self.assertEqual(code, bytearray([0xB1,2,1,0x2B]))

	def testLOOPCALL(self):
		code = helper.toBytes("LOOPCALL 3 func1 2 4 6", helper.FPGM)
		self.assertEqual(code, bytearray([0xB4,2,4,6,3,1,0x2A]))



class DeltaTest(unittest.TestCase):

	def testDeltapSteps(self):
		code = helper.toBytes("deltap 1 6-8 7-1 8+1 9+8")
		self.assertEqual(code, bytearray([0x40,10,0x00,1,0x17,1,0x28,1,0x3f,1,4,6,0x5E,0x5D]))

	def testDeltacVariants(self):
		code = helper.toBytes("deltac cvt0 6-8 21+8 22-8 37+8 38-8 53+8", helper.CVT)
		self.assertEqual(code, bytearray([0x40,16,0x00,0,0xff,0,2,0x00,0,0xff,0,2,0x00,0,0xff,0,2,6,0x5E,0x73,0x74,0x75]))

	def testDeltapVariants(self):
		code = helper.toBytes("deltap 1 6-8 21+8 22-8 37+8 38-8 53+8")
		self.assertEqual(code, bytearray([0x40,16,0x00,1,0xff,1,2,0x00,1,0xff,1,2,0x00,1,0xff,1,2,6,0x5E,0x5D,0x71,0x72]))

	def testDeltapSort(self):
		code = helper.toBytes("deltap 1 53+8 22-8 38-8 21+8 37+8 6-8")
		self.assertEqual(code, bytearray([0x40,16,0x00,1,0xff,1,2,0x00,1,0xff,1,2,0x00,1,0xff,1,2,6,0x5E,0x5D,0x71,0x72]))

	def testDeltapMerge(self):
		code = helper.toBytes("deltap 1 6-8 21+8 \n deltap 1 22-8 37+8 \n deltap 1 38-8 53+8")
		self.assertEqual(code, bytearray([0x40,16,0x00,1,0xff,1,2,0x00,1,0xff,1,2,0x00,1,0xff,1,2,6,0x5E,0x5D,0x71,0x72]))

	def testDeltapBases(self):
		code = helper.toBytes("deltap 1 6-8 53+8 54-8 101+8 102-8 149+8")
		self.assertEqual(code, bytearray([0x40,21,0xff,1,1,0x00,1,1,102,0xff,1,1,0x00,1,1,54,0xff,1,1,0x00,1,1,6,0x5E,0x5D,0x72,0x5E,0x5D,0x72,0x5E,0x5D,0x72]))

	def testDeltapChain(self):
		code = helper.toBytes("MPPEM \n deltap 1 6-8 7-8 \n RTG")
		self.assertEqual(code, bytearray([0x4B,0xB5,0x00,1,0x10,1,2,6,0x5E,0x5D,0x18]))



class ScopeTest(unittest.TestCase):

	def testIfElseScope(self):
		code = helper.toBytes("MDAP 4 \n IF 1 \n MDAP 5 \n MDAP 6 \n ELSE \n MDAP 7 \n MDAP 8 \n EIF \n MDAP 9")
		self.assertEqual(code, bytearray([0xB2,9,1,4,0x2E,0x58,0xB1,6,5,0x2E,0x2E,0x1B,0xB1,8,7,0x2E,0x2E,0x59,0x2E]))

	def testIfSubScope(self):
		code = helper.toBytes("MDAP 5 \n IF 1 \n MDAP 6 \n IF 2 \n MDAP 7 \n EIF \n MDAP 8 \n EIF \n MDAP 9")
		self.assertEqual(code, bytearray([0xB2,9,1,5,0x2E,0x58,0xB2,8,2,6,0x2E,0x58,0xB0,7,0x2E,0x59,0x2E,0x59,0x2E]))

	def testFunctionScope(self):
		code = helper.toBytes("FDEF f0 \n IF 2 \n MDAP 5 \n MDAP 6 \n EIF \n ENDF \n FDEF f1 \n POP \n ENDF", "", "fpgm")
		self.assertEqual(code, bytearray([0xB1,1,0,0x2C,0xB0,2,0x58,0xB1,6,5,0x2E,0x2E,0x59,0x2D,0x2C,0x21,0x2D]))



class SubBlockTest(unittest.TestCase):

	def testSubBlock(self):
		code = helper.toBytes("MDAP 4 \n { \n MDAP 5 \n }")
		self.assertEqual(code, bytearray([0xB0,4,0x2E,0xB0,5,0x2E]))

	def testSubBlockConsolidation(self):
		code = helper.toBytes("MDAP 3 \n MDAP 4 \n { \n MDAP 5 \n MDAP 6 \n }")
		self.assertEqual(code, bytearray([0xB1,4,3,0x2E,0x2E,0xB1,6,5,0x2E,0x2E]))

	def testSubBlockOuterConsolidation(self):
		code = helper.toBytes("MDAP 4 \n { \n MDAP 5 \n } \n MDAP 6")
		self.assertEqual(code, bytearray([0xB1,6,4,0x2E,0xB0,5,0x2E,0x2E]))

	def testSubBlockSequence(self):
		code = helper.toBytes("MDAP 4 \n { \n MDAP 5 \n } \n { \n MDAP 6 \n }")
		self.assertEqual(code, bytearray([0xB0,4,0x2E,0xB0,5,0x2E,0xB0,6,0x2E]))

	def testSubSubBlock(self):
		code = helper.toBytes("MDAP 3 \n { \n MDAP 4 \n MDAP 5 \n { \n MDAP 6 \n MDAP 7 \n } \n }")
		self.assertEqual(code, bytearray([0xB0,3,0x2E,0xB1,5,4,0x2E,0x2E,0xB1,7,6,0x2E,0x2E]))
