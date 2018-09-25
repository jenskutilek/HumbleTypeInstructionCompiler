Humble Type Instruction Compiler
================================

TrueType, as defined by [Microsoft] and [Apple], provides
the most powerful mechanism to hint a font. Yet, hardly any
open source tool supports the creation of TrueType programs.
Consequently, I have implemented my own tool.

The *Humble Type Instruction Compiler* translates humble type
instructions into TrueType instructions, while taking care of
cumbersome tasks like optimized stack pushes and index mapping.

Importantly, humble type instructions are not intended to form
a new language, but rather provide a simplified arrangement of
instruction names, flags, and arguments in a plain-text format.

The compiler is implemented in Python. Currently, it supports
the instruction of [FontForge] and [FontTools] font objects.
With thanks to Jens Kutilek for adding FontTools support.

Further documentation is available in the [doc](doc) directory:

- [instructions.md](doc/instructions.md): Introduction to the instruction format
- [blocks.md](doc/blocks.md): The blocks that contain the instructions
- [example.md](doc/example.md): An exemplary instruction of the letter H
- [usage.md](doc/usage.md): How to compile the instructions with Python
- [grammar.md](doc/grammar.md): The grammar for the blocks and instructions


[Microsoft]: https://microsoft.com/en-us/Typography/SpecificationsOverview.aspx
[Apple]:     https://developer.apple.com/fonts/TrueType-Reference-Manual/
[FontForge]: https://fontforge.github.io
[FontTools]: https://github.com/fonttools/fonttools
