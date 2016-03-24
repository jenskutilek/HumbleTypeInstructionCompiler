import io
import htic



CVT = "cvt{ \n 0 cvt0 \n 10 cvt1 \n 20 cvt2 \n}"
FLAGS = "flags{ x 1 \n m 11110 \n}"
FPGM = "fpgm{ FDEF func0 \n POP \n ENDF \n FDEF func1 \n POP \n ENDF \n}"



def getData(code):
	parser = htic.parser.Parser()
	return parser.parse(io.BytesIO(code))



def toBytes(instructions, precode="", name="A"):
	data = getData(precode + name + "{" + instructions + "\n}")
	translator = htic.translator.BinaryTranslator()
	if name == "prep":
		return translator.translate(data.prep)
	elif name == "fpgm":
		return translator.translate(data.fpgm)
	else:
		return translator.translate(data.glyphs[name])
