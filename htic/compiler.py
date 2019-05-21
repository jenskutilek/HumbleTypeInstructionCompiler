from __future__ import absolute_import
from __future__ import print_function

from .parser import parseFile
from .translator import BinaryTranslator
from .translator import StringTranslator


def toConsole(sourceFile):
	data = parseFile(sourceFile)
	translator = StringTranslator()

	print("-------- gasp --------")
	for size, doGridfit, doGray, symSmoothing, symGridfit in data.gasp:
		line = "{:5d}".format(size)
		if doGridfit    : line += " doGridfit"
		if doGray       : line += " doGray"
		if symSmoothing : line += " symSmoothing"
		if symGridfit   : line += " symGridfit"
		print(line)

	print("-------- maxp --------")
	for name, value in data.maxp.items():
		print("{} {}".format(name, value))

	print("-------- cvt ---------")
	if data.cvt:
		print(data.cvt)

	print("-------- fpgm --------")
	if data.fpgm:
		print(translator.translate(data.fpgm))

	print("-------- prep --------")
	if data.prep:
		print(translator.translate(data.prep))

	for name, block in data.glyphs.items():
		print("--------", name, "--------")
		print(translator.translate(block))


def toFontforge(sourceFile, font):
	data = parseFile(sourceFile)
	translator = BinaryTranslator()

	if data.gasp:
		gasp = []
		for size, doGridfit, doGray, symSmoothing, symGridfit in data.gasp:
			flags = []
			if doGridfit    : flags.append("gridfit")
			if doGray       : flags.append("antialias")
			if symSmoothing : flags.append("symmetric-smoothing")
			if symGridfit   : flags.append("gridfit+smoothing")
			gasp.append((size, tuple(flags)))
		font.gasp_version = 1
		font.gasp = tuple(gasp)

	for name, value in data.maxp.items():
		if name == "maxStackElements" : font.maxp_maxStackDepth = value
		if name == "maxFunctionDefs"  : font.maxp_FDEFs = value
		if name == "maxStorage"       : font.maxp_storageCnt = value
		if name == "maxZones"         : font.maxp_zones = value
		if name == "maxTwilightPoints": font.maxp_twilightPtCnt = value

	if data.cvt:
		font.cvt = data.cvt

	if data.fpgm:
		font.setTableData("fpgm", translator.translate(data.fpgm))

	if data.prep:
		font.setTableData("prep", translator.translate(data.prep))

	for name, block in data.glyphs.items():
		try:
			font[str(name)].ttinstrs = translator.translate(block)
		except Exception:
			print("Error with glyph: " + name)
			raise


def toFontTools(sourceFile, font):
	import array
	from fontTools import ttLib
	from fontTools.ttLib.tables._g_a_s_p import GASP_SYMMETRIC_GRIDFIT, GASP_SYMMETRIC_SMOOTHING, GASP_DOGRAY, GASP_GRIDFIT
	data = parseFile(sourceFile)
	translator = BinaryTranslator()

	if data.gasp:
		gasp = ttLib.newTable("gasp")
		gasp.gaspRange = {}
		for size, doGridfit, doGray, symSmoothing, symGridfit in data.gasp:
			flags = 0
			if doGridfit    : flags |= GASP_GRIDFIT
			if doGray       : flags |= GASP_DOGRAY
			if symSmoothing : flags |= GASP_SYMMETRIC_SMOOTHING
			if symGridfit   : flags |= GASP_SYMMETRIC_GRIDFIT
			gasp.gaspRange[size] = flags
		gasp.version = 1
		font["gasp"] = gasp

	for name, value in data.maxp.items():
		if name == "maxStackElements" : font["maxp"].maxStackElements = value
		if name == "maxFunctionDefs"  : font["maxp"].maxFunctionDefs = value
		if name == "maxStorage"       : font["maxp"].maxStorage = value
		if name == "maxZones"         : font["maxp"].maxZones = value
		if name == "maxTwilightPoints": font["maxp"].maxTwilightPoints = value

	if data.cvt:
		font["cvt "] = cvt = ttLib.newTable("cvt ")
		cvt.values = array.array("h", data.cvt)

	if data.fpgm:
		fpgm = ttLib.newTable("fpgm")
		font["fpgm"].program.fromBytecode(translator.translate(data.fpgm))

	if data.prep:
		fpgm = ttLib.newTable("prep")
		font["prep"].program.fromBytecode(translator.translate(data.prep))

	for name, block in data.glyphs.items():
		try:
			font["glyf"][str(name)].program.fromBytecode(translator.translate(block))
		except Exception:
			print("Error with glyph: " + name)
			raise


# EXTEND Add to* function for new target type
