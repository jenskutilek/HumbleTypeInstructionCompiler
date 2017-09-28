Instructions
============

This file showcases the plain-text humble type instruction format,
which simplifies the arrangement of TrueType instruction names,
flags, and arguments. The code examples follow a side-by-side format:

```
Humble type instruction source | Compiled TrueType instructions
```


Comments
--------

Text between `#` and the end of the line is ignored.

```
RTG # Hello | RTG
```


Flags
-----

As established by the standard, instruction flags are enclosed
in square brackets and directly appended to instruction names.
They can be written in binary form, or as an alias from the
`flags` block (see BLOCKS.md). Omitted flags default to zero.

```
SVTCA    | SVTCA[0]
SVTCA[1] | SVTCA[1]
SVTCA[x] | SVTCA[1]
```


Arguments
---------

Instruction arguments are listed after the instruction name,
on the same line, separated by at least one space.
The compiler then creates optimized push instructions.

```
ALIGNPTS 7 8 | PUSHB[010]
FLIPPT   9   |  9 7 8
             | ALIGNPTS
             | FLIPPT
```


Automatic Looping
-----------------

If more than one argument follows an `ALIGNRP`, `FLIPPT`, `IP`,
or `SHP` instruction, the compiler will split them up appropriatly,
either by multiplying the instruction or by inserting `SLOOP`.

```
ALIGNRP 6 7 8 9 | PUSHB[100]
                |  6 7 8 9 4
                | SLOOP
                | ALIGNRP

```


Numeric Conversion
------------------

Numeric arguments can be written in different formats. The compiler
supports the hexadecimal notation with a `0x` prefix, the binary
notation with a `0b` prefix, signed integers, signed decimals
representing f26dot6, or signed decimals with a colon representing
f2dot14. Decimals are rounded when necessary.

```
SMD 0x60        | PUSHB[000]
SMD 0b1100000   |  96
SMD 96          | SMD
SMD 1.5         |
SMD 0:005859375 |
```


Identifiers
-----------

Unique names are used to address control values, storage locations,
or functions. The compiler takes care of mapping each name to an index.
In the following example, the storage id `foo` is mapped to the exemplary
index `17`.

```
WS foo 8 | PUSHB[001]
         |  17 8
         | WS
```


Nested Instructions
-------------------

To use the output of an instruction as an argument,
it is nested in parentheses.

```
MIAP (RS foo) bar | PUSHB[000]
                  |  17
                  | RS
                  | PUSHB[000]
                  |  23
                  | MIAP[0]
```


Operator Symbols
----------------

Instead of writing mathematical instructions in prefix
notation, it is possible to write their symbols
`==` `!=` `<=` `<` `>=` `>` `+` `-` `*` `/` `and` `or`
between their two arguments. When possible, nested instructions
should be placed on the right side, for an optimal push optimization.

```
IF (2 > (1 + 3)) | PUSHB[010]
                 |  2 1 3
                 | ADD
                 | GT
                 | IF
```


Function Definitions
--------------------

The humble version of the `FDEF` instruction is more verbose. Its first
argument is the function index, followed by the function identifier.
Then follows a list of expected parameters, which are used to parse
the arguments of the corresponding `CALL` instructions.

A parameter must begin with `val`, `pt`, `cvt`, `func`, or `stor`
to declare its type, which is either a numerical value, point number,
control value identifier, function identifier, or storage identifier
respectively. Additional characters can be appended to a parameter name
to make it more legible.

```
FDEF 9 interpol pt pt1 pt2 | PUSHB[000]
  SRP2                     |  9
  SRP1                     | FDEF
  DUP                      |  SRP2
  IP                       |  SRP1
  MDAP[rnd]                |  DUP
ENDF                       |  IP
                           |  MDAP[rnd]
                           | ENDF
```


Stack Management
----------------

When arguments are listed after the instruction name, the compiler
creates optimized `PUSH` instructions. However, sometimes it is
desireable to manage the stack manually, for example in function
definitions.

For that case, it is possible to omit arguments after an instruction
and instead push them with the custom `push` instruction. Mixing
automatic and manual pushes within the same scope, e.g. the body
of a function definition, is not recommended.

```
FDEF 31 align pt | PUSHB[000]
  DUP            |  31
  push 1         | FDEF
  ADD            | DUP
  ALIGNPTS       | PUSHB[000]
ENDF             |  1
                 | ADD
                 | ALIGNPTS
                 | ENDF
```


Function Calls
--------------

Function calls are slightly rearranged. The possible loop count and
identifier of the function are listed first, followed by the arguments.

```
CALL align 8         | PUSHB[001]
LOOPCALL 2 align 8 6 |  8 31
                     | CALL
                     | PUSHB[011]
                     |  8 6 2 31
                     | LOOPCALL
```


Void Functions
--------------

Because functions can potentially push values onto the stack,
the compiler normally does not consolidate push instruction accross
`CALL` instructions. However, if a function does not push more values
than it consumes, it can be declared with the `void` instruction
instead of `FDEF`, to enable a more aggressive optimization.

```
void 9 interp pt pt1 pt2
...

```


Delta Instructions
------------------

The standard `DELTA*` instructions are replaced by the custom
`deltac` and `deltap` instructions. Their arguments consist of
a control value identifier or a point number, followed by a
sequence of modifiers.

Each modifier consists of a ppem value and a signed step value.
For example, `29-6` causes a shift of -6 steps at a ppem of 29.
The compiler generates appropriate `SDB` and `DELTA*` instructions.

```
deltap 8 11+2 29-6 | PUSHB[110]
                   |  34 8 1 9 8 1 11
                   | SDB
                   | DELTAP1
                   | DELTAP2

```


Subblocks
---------

A subblock suspends the current argument consolidation and starts
a new one within its scope. It can be used to limit the number of
arguments pushed at once, thus avoiding the infamous stack overflow.
Subblocks are enclosed with `{}`.

```
UTP 1  | PUSHB[010]
UTP 2  |  5 2 1
{      | UTP
  IP 3 | UTP
  IP 4 | PUSHB[001]
}      |  4 3
UTP 5  | IP
       | IP
       | UTP
```
