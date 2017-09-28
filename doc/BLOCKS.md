Blocks
======

Humble code is organized in blocks. A block starts with a name
and encloses its content in curly brackets. Depending on the block,
the content consists of humble type instructions, or represents
a related TrueType table.


gasp
----

This block represents the [gasp] table, version 1. Each line starts
with a size, followed by optional flags that apply up to that size.
[gasp]: http://www.microsoft.com/typography/otspec/gasp.htm

```
gasp
{
      7           doGray
  65535 doGridfit doGray symSmoothing symGridfit
}
```


maxp
----

This block represents the [maxp] table. Each line starts with a value,
followed by its identifier. The example lists all supported identifiers.
[maxp]: http://www.microsoft.com/typography/otspec/maxp.htm

```
maxp
{
  256 maxStackElements
   32 maxFunctionDefs
   32 maxStorage
    2 maxZones
   16 maxTwilightPoints
}
```


cvt
---

This block represents the [cvt] table. Each line starts with
a control value, followed by its identifier.
[cvt]: http://www.microsoft.com/typography/otspec/cvt.htm

```
cvt
{
  -80 descender
  160 stem
  700 cap
}
```


flags
-----

Writing instruction flags in binary form can be cumbersome.
Therefore, this block allows to define flag aliases. Each line
starts with an alias, followed by the corresponding binary value.

```
flags
{
  x    1
  rnd  1
  stem 01101
  pMRB 01101
}
```


Instruction blocks
------------------

Humble type instructions for the [fpgm] and [prep] tables are placed
in blocks with the corresponding name. Glyph instructions are placed
in a block with the name of the glyph, as defined by the font.
[fpgm]: http://www.microsoft.com/typography/otspec/fpgm.htm
[prep]: http://www.microsoft.com/typography/otspec/prep.htm

```
fpgm
{
  FDEF setRoundState
    RTDG
  ENDF
}

prep
{
  IF ((8 > (MPPEM)) or (GETINFO 0b110))
    INSTCTRL 1 1
  EIF
}

asciitilde
{
  CALL setRoundState
  MDAP+r 0
}
```
