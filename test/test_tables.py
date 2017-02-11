from __future__ import absolute_import

from . import helper

import unittest


class GaspTest(unittest.TestCase):

	def testGaspEmpty(self):
		data = helper.getData("""gasp{
			}""")
		self.assertEqual(len(data.gasp), 0)

	def testGasp(self):
		data = helper.getData("""gasp{
			    7
			   12           doGray symSmoothing
			  128 doGridfit                     symGridfit
			65535 doGridfit doGray symSmoothing symGridfit
			}""")
		self.assertEqual(data.gasp[0], (7, False, False, False, False))
		self.assertEqual(data.gasp[1], (12, False, True, True, False))
		self.assertEqual(data.gasp[2], (128, True, False, False, True))
		self.assertEqual(data.gasp[3], (65535, True, True, True, True))


class MaxpTest(unittest.TestCase):

	def testMaxpEmpty(self):
		data = helper.getData("""maxp{
			}""")
		self.assertEqual(len(data.maxp), 0)

	def testMaxpPart(self):
		data = helper.getData("""maxp{
			256 maxStackElements
			 64 maxFunctionDefs
			}""")
		self.assertEqual(len(data.maxp), 2)
		self.assertEqual(data.maxp['maxStackElements'], 256)
		self.assertEqual(data.maxp['maxFunctionDefs'], 64)

	def testMaxpFull(self):
		data = helper.getData("""maxp{
			256 maxStackElements
			 64 maxFunctionDefs
			 32 maxStorage
			  2 maxZones
			 16 maxTwilightPoints
			}""")
		self.assertEqual(len(data.maxp), 5)
		self.assertEqual(data.maxp['maxStackElements'], 256)
		self.assertEqual(data.maxp['maxFunctionDefs'], 64)
		self.assertEqual(data.maxp['maxStorage'], 32)
		self.assertEqual(data.maxp['maxZones'], 2)
		self.assertEqual(data.maxp['maxTwilightPoints'], 16)


class CvtTest(unittest.TestCase):

	def testCvtEmpty(self):
		data = helper.getData("""cvt{
			}""")
		self.assertEqual(len(data.cvt), 0)

	def testCvtBoundary(self):
		data = helper.getData("""cvt{
			 0 c0
			-0 c1
			 64 c2
			-64 c3
			 32767 c4
			-32768 c5
			-1 c6
			}""")
		self.assertEqual(len(data.cvt), 7)
		self.assertEqual(data.cvt, [0, 0, 64, -64, 32767, -32768, -1])


class FpgmPrepTest(unittest.TestCase):

	def testFpgmEmpty(self):
		code = helper.toBytes("", "", "fpgm")
		self.assertEqual(code, "")

	def testPrepEmpty(self):
		code = helper.toBytes("", "", "prep")
		self.assertEqual(code, "")
