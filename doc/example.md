Example
=======

A more complete example can be found in the source files of
the [Oxanium font family](https://github.com/sevmeyer/oxanium).

Consider these outlines for the glyph named "H":

```
 1--2  5--6
 |  |  |  |
 |  3--4  |
 |        |
 |  10-9  |
 |  |  |  |
 0-11  8--7
```

The following plain-text source populates the Control Value Table,
defines some useful flag aliases, and instructs the outlines vertically:

```
cvt {
    0 base
  700 cap
}

flags {
  y    0
  r    1
  rp1  1
  stem 01001
}

H {
  SVTCA[y]
  MIAP[r]     0 base
  SHP[rp1]    8
  MIAP[r]     6 cap
  SHP[rp1]    2
  SRP2        0
  IP         10
  MDAP[r]    10
  MDRP[stem]  4
  IUP[y]
}

```

This is then compiled into the following TrueType glyph program.
Note that the compiler collects all arguments, maps them to the
correct table indices, and pushes them in a single call:

```
NPUSHB 10 4 10 10 0 2 6 1 8 0 0
SVTCA[0]
MIAP[1]
SHP[1]
MIAP[1]
SHP[1]
SRP2
IP
MDAP[1]
MDRP[01001]
IUP[0]
```
