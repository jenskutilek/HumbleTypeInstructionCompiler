Compilation
===========

The compiler is implemented in Python, to integrate it directly into
existing build scripts. It is intended to work with Python 2.7 and 3.


Interface
---------

Add the `htic` directory to `PYTHONPATH`, so that python can find it.
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

Parsed instruction blocks are represented by `Block` objects.
These objects can be converted to the desired format with a
`Translator`. Currently, two translator types are available:
`BinaryTranslator` converts blocks to binary TrueType code,
while `StringTranslator` converts blocks to plain-text strings.
