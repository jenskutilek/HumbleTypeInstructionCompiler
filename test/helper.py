import io
import htic


def getData(code):
	parser = htic.parser.Parser()
	stream = io.StringIO(code)
	return parser.parse(stream)


def toBytes(instructions, precode="", name="A"):
	data = getData(precode + name + "{" + instructions + "\n}")
	if name == "prep":
		return bytes(data.prep)
	elif name == "fpgm":
		return bytes(data.fpgm)
	else:
		return bytes(data.glyphs[name])
