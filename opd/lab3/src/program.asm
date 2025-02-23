ORG 0x40B
ARR: WORD 0x0424    
I: WORD 0x0200
N: WORD 0xE000
RES: WORD 0x0200
START: LD #0x80 ; прямая загрузка в AC = 128
DEC
SWAB ; Обмен ст. и мл. байтов, AC = 2^15 - 1 = 32767
ST RES ; EEFB - ST IP-5+1 - прямая относительная
LD #0x4 ; прямая загрузка в AC = 4
ST N ; EEF8 - ST IP-8+1 - прямая относительная
ADD ARR ; 4EF5 - ADD IP-11+1 - прямая относительная
ST I ; EEF5 - ST IP-11+1 - прямая относительная
LI: LD -(I) ; ABF4 - LD -(IP-12+1) - косвенная относительная автодекрементная
ROR
BCS LS ; F407 - BCS IP+7+1 - переход если выше или равно / перенос (C == 1)
ROR
BCS LS ; F405 - BCS IP+5+1 - переход если выше или равно / перенос (C == 1)
ROL
ROL
CMP RES ; 7EEF - CMP IP-17+1
BGE LS ; F901 - BGE IP+1+1 - переход если больше или равно (N XOR V == 0 / N == V)
ST RES ; EEED - ST IP-19+1 - прямая относительная
LS: LOOP $N 
JUMP LI ; CEF4 - JUMP IP-12+1 - прямая относительная
HLT
A_1: WORD 0x0B00
A_2: WORD 0x0000
A_3: WORD 0xCE01
A_4: WORD 0x0802
