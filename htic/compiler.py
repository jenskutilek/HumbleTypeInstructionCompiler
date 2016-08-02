from __future__ import absolute_import
from __future__ import print_function

from .parser import parseFile
from .translator import BinaryTranslator
from .translator import StringTranslator



def toConsole(sourceFile):
	data = parseFile(sourceFile)
	translator = StringTranslator()

	print("-------- gasp --------")
	for size, doGridfit, doGray in data.gasp:
		line = "{:5d}".format(size)
		if doGridfit: line += " gridfit"
		if doGray   : line += " gray"
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
		for size, doGridfit, doGray in data.gasp:
			flags = []
			if doGridfit:
				flags.append("gridfit")
			if doGray:
				flags.append("antialias")
			gasp.append((size, tuple(flags)))
		font.gasp = tuple(gasp)

	for name, value in data.maxp.items():
		if name == "maxStackElements":
			font.maxp_maxStackDepth = value
		if name == "maxFunctionDefs":
			font.maxp_FDEFs = value
		if name == "maxStorage":
			font.maxp_storageCnt = value
		if name == "maxZones":
			font.maxp_zones = value
		if name == "maxTwilightPoints":
			font.maxp_twilightPtCnt = value

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



# EXTEND Add to* function for new target type
