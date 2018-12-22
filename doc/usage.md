Usage
=====

The compiler is implemented in Python 3, to integrate
it directly into existing Python-based build scripts.


Interface
---------

Install the `htic` package via pip, or use the provided `setup.py`.
Then import `htic` and call the appropriate `to*()` function:

```
import fontforge
import htic

# Open font with FontForge
font = fontforge.open("myfont.sfd")

# Compile instructions and insert them into font
htic.toFontforge("instructions.hti", font)

# Save font with FontForge
font.generate("myfont.ttf")
```

The following `to*()` functions are available:

```
htic.toConsole(sourceFile)
htic.toFontforge(sourceFile, font)
htic.toFontTools(sourceFile, font)
```


Extending
---------

The compiler can be extended to support other font object types.
Search for the `EXTEND` keyword in the code to find the relevant
extension points.

The main task is to add a custom `to*()` function. Check the
existing functions for reference. These functions first pass
the sourcefile name to `parser.parseFile()`, which returns a
`Data` object. This object contains all parsed data in a neutral
format, which can then be written into the font object.

Parsed instruction blocks (`fpgm`, `prep`, or glyph instructions)
are represented by `Block` objects. Blocks can be converted to
human-readable strings with `str(block)` for debugging, or to
binary TrueType code with `bytes(block)`.
