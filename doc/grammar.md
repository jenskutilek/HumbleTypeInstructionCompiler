Grammar
=======

The following [ABNF](https://en.wikipedia.org/wiki/ABNF) grammar
describes the compiler input format. In addition to the official
grammar syntax, 'single quotes' denote case-sensitive strings.


Main Structure
--------------

```
 root = [flags] [gasp] [maxp] [cvt] [fpgm] [prep] *glyph
 gasp = 'gasp' open *(ws uint *(s gaspflag) nl) close
 maxp = 'maxp' open *(ws uint s maxpname nl) close
  cvt = 'cvt' open *(ws num s id nl) close
flags = 'flags' open *(ws id s bits nl) close
 fpgm = 'fpgm' block
 prep = 'prep' block
glyph = id block
```


Block Structure
---------------

```
    block = open *(ws instr nl) close
     open = ws '{' ws
    close = ws '}' ws

    instr = instrname flag *(s arg)
     flag = ['[' flagval ']']
  flagval = id / bits
      arg = id / val
      val = num / '(' (instr / op) ')'
operation = val s operator s val
```


Terminals
---------

```
        s = 1*WSP                  ; Mandatory space
       nl = *(LWSP / comment) CRLF ; Mandatory newline
       ws = *(LWSP / comment CRLF) ; Optional whitespace
  comment = '#' *(VCHAR / WSP)

       id = 1*(ALPHA / DIGIT / '_' / '.')
instrname = <TrueType instruction name>

      num = xint / bint / int / f26d6 / f2d14
     xint = '0x' 1*4HEXDIG
     bint = '0b' 1*16BIT
      int = <-32768 to 32767>
    f26d6 = <-512.0 to 511.984375>
    f2d14 = <-2:0 to 1:999938965>

     bits = 1*5BIT
     uint = %d0-65535
    delta = %d0-32767 ('+' / '-') %d1-8

 operator = '+' / '-' / '<' / '<=' / '==' / 'and' /
            '*' / '/' / '>' / '>=' / '!=' / 'or'

 gaspflag = 'doGridfit' /
            'doGray' /
            'symSmoothing' /
            'symGridfit'

 maxpname = 'maxZones' /
            'maxTwilightPoints' /
            'maxStorage' /
            'maxFunctionDefs' /
            'maxStackElements'

    param = ('func' / 'cvt' / 'pt' / 'stor' / 'val') *VCHAR
```


Altered Instructions
--------------------

These instructions differ from the TrueType specification, for
example because they use alphanumeric identifiers instead of indices.

```
instr =/ 'MIAP' flag s val s id
       / 'MIRP' flag s val s id
       / 'WCVTP' s id s val
       / 'WCVTF' s id s val
       / 'RCVT'  s id
       / 'WS' s id s val
       / 'RS' s id
       / 'FDEF' s uint s id *(s param)
       / 'CALL' s id *(s arg)
       / 'LOOPCALL' s val s id *(s arg)
```


Custom Instructions
-------------------

```
instr =/ 'push' 1*(s num)
       / 'deltac' s id  1*(s delta)
       / 'deltap' s val 1*(s delta)
       / 'void' s uint s id *(s param)
```


Unsupported Instructions
------------------------

The following list is not in ABNF format.

```
IDEF.*
AA.*          (Deprecated)
SANGW.*       (Deprecated)
DELTAC[123].* (See deltac)
DELTAP[123].* (See deltap)
N?PUSH[BW]?.* (See push)
```
