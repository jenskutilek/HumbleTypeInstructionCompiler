Example
=======

A more extensive example can be found in the sourcefiles
of the [Xolonium](https://gitlab.com/sev/xolonium) fonts.

First, the cvt table is populated with a few values,
and some useful flag aliases are defined as well:

```
cvt
{
   80 side
  160 stem
  120 bar
  700 cap
}

flags
{
  x    1
  y    0
  r    1
  rp2  0
  side 01110
  stem 01101
  body 10100
}
```

Now consider these outlines:

```
 1--2  5--6
 |  |  |  |
 |  3--4  |
 |        |
 |  10-9  |
 |  |  |  |
 0-11  8--7
```

The code on the left shows an exemplary instruction of the outlines.
It is then compiled into the TrueType program on the right.
Note that the compiler collects all arguments, maps them to the
correct indices, and pushes them in a single call:

```
H                    | NPUSHB
{                    |  21
  MIAP[r]     0 side |  10 2 4 4 0 2 6 3 8 0
  MIRP[stem]  2 stem |  13 0 4 8 1 6 10 2 1 0 0
  SHP[rp2]   10      | MIAP[1]
  MDRP[body]  6      | MIRP[1101]
  MIRP[stem]  8 stem | SHP[0]
  SHP[rp2]    4      | MDRP[10100]
  MIRP[side] 13 side | MIRP[1101]
  IUP[x]             | SHP[0]
                     | MIRP[1110]
  SVTCA[y]           | IUP[1]
  MDAP[r]     0      | SVTCA[0]
  ALIGNRP     8      | MDAP[1]
  MIAP[r]     6 cap  | ALIGNRP
  ALIGNRP     2      | MIAP[1]
  SRP2        0      | ALIGNRP
  IP          4      | SRP2
  MDAP[r]     4      | IP
  MIRP[stem] 10 bar  | MDAP[1]
  IUP[y]             | MIRP[1101]
}                    | IUP[0]
```
