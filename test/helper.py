import io
import htic


CVT = "cvt{ \n 0 cvt0 \n 10 cvt1 \n 20 cvt2 \n}"
FLAGS = "flags{ x 1 \n m 11110 \n}"
FPGM = "fpgm{ FDEF 0 func0 val \n POP \n ENDF \n FDEF 1 func1 val \n POP \n ENDF \n}"
FPGMPARAMS = "fpgm{ FDEF 0 func0 val pt cvt func stor \n POP \n POP \n POP \n POP \n POP \n ENDF \n}"


def getData(code):
	parser = htic.parser.Parser()
	stream = io.StringIO(code)
	return parser.parse(stream)


def toBytes(instructions, precode="", name="A"):
	data = getData(precode + name + "{" + instructions + "\n}")
	translator = htic.translator.BinaryTranslator()
	if name == "prep":
		return translator.translate(data.prep)
	elif name == "fpgm":
		return translator.translate(data.fpgm)
	else:
		return translator.translate(data.glyphs[name])
