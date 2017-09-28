Humble Type Instruction Compiler
================================

TrueType, as defined by [Apple] and [Microsoft], provides
the most powerful mechanism to hint a font. Yet, hardly any
open source tool supports the creation of TrueType programs.
Consequently, I have implemented my own tool.

The *Humble Type Instruction Compiler* translates humble type
instructions into TrueType instructions, while taking care of
cumbersome tasks like optimized stack pushes and index mapping.

Importantly, humble type instructions are not intended to form
a new language, but rather provide a simplified arrangement of
instruction names, flags, and arguments in a plain-text format.

The compiler is implemented in Python. Currently, it only
supports the instruction of [FontForge] font objects, but
it can be extended quite easily.

Further documentation is available in the `doc` directory.


[Apple]: https://developer.apple.com/fonts/TrueType-Reference-Manual/
[Microsoft]: https://microsoft.com/en-us/Typography/SpecificationsOverview.aspx
[FontForge]: https://fontforge.github.io
