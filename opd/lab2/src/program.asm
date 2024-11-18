ORG 0x83
VAR1: WORD 0x2083
VAR2: WORD 0xE08F
START: CLA          ;85
NOT                 ;86
AND 0x83            ;87
AND 0x84            ;88
ST 0x90             ;89
LD 0x8E             ;8A
SUB 0x90            ;8B
ST 0x8F             ;8C
HLT                 ;8D
LD 0x8E             ;8E
NOT                 ;8F
CLA                 ;90
