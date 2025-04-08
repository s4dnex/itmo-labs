ORG 0x26D
TEMP: WORD ?
NUL: WORD 0x00
ADDR: WORD $STRING ; next word address

START:
    LD (ADDR)+
    ST TEMP
    SWAB
    PUSH
    CALL $FUNC
    POP
    LD TEMP
    PUSH
    CALL $FUNC
    POP
    JUMP START

FUNC:
    IN 3
    AND #0x40
    BEQ FUNC ; spin-loop until ready
    LD &1
    OUT 2
    CMP NUL
    BEQ STOP
    RET

STOP:
    HLT

ORG 0x5E9
STRING: WORD 0xC2B5 ; ТЕ
WORD 0xC1C2 ; СТ
WORD 0x0