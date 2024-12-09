ORG 0x83
A: WORD 0xDADA   ;83
B: WORD 0xDEAD   ;84    
C: WORD 0x00FF   ;85
D: WORD 0x0000   ;86
START: LD 0x83   ;87
AND 0x84         ;88
NEG              ;89
ADD 0x85         ;8A
ST  0x86         ;8B
HLT              ;8C