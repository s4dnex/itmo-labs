ORG 0x83
A: WORD 0x2083   ;83
B: WORD 0xE08F   ;84
START: CLA       ;85
NOT              ;86
AND 0x83         ;87
AND 0x84         ;88
ST 0x90          ;89
LD 0x8E          ;8A
SUB 0x90         ;8B
ST 0x8F          ;8C
HLT              ;8D
C: WORD 0xA08E   ;8E
D: WORD 0x0280   ;8F
E: WORD 0x0200   ;90