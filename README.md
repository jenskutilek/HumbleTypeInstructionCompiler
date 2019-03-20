Humble Type Instruction Compiler
================================

TrueType, as defined by [Microsoft] and [Apple], provides
the most powerful mechanism to hint a font. Yet, hardly any
open source tool supports the creation of TrueType programs.
Consequently, I have implemented my own tool.

The *Humble Type Instruction Compiler* translates simplified
plain-text instructions into optimized TrueType bytecode, while
taking care of cumbersome tasks like consolidating stack pushes
or mapping indices.

Importantly, humble type instructions are not intended to be a
new language, but rather provide a more convenient arrangement
of instruction names, flags, and arguments.

The compiler is implemented in Python 3. It supports the
instruction of [FontForge] and [FontTools] font objects.
With thanks to Jens Kutilek for adding FontTools support.

Further documentation is available in the [doc](doc) directory:

- [instructions.md](doc/instructions.md): Introduction to the instruction format
- [blocks.md](doc/blocks.md): The blocks that contain the instructions
- [example.md](doc/example.md): An exemplary instruction of the letter H
- [usage.md](doc/usage.md): How to compile the instructions with Python
- [grammar.md](doc/grammar.md): The grammar for the instruction format


[Microsoft]: https://docs.microsoft.com/typography/opentype/spec/
[Apple]:     https://developer.apple.com/fonts/TrueType-Reference-Manual/
[FontForge]: https://fontforge.github.io
[FontTools]: https://github.com/fonttools/fonttools
