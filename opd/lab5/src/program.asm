ORG 0x26D
TEMP: WORD ?
NUL: WORD 0x00
ADDR: WORD $STRING ; next word address

MAIN:
    LD (ADDR)+
    ST TEMP
    SWAB
    PUSH
    CALL $PRINT_SYMBOL
    POP
    LD TEMP
    PUSH
    CALL $PRINT_SYMBOL
    POP
    JUMP MAIN

PRINT_SYMBOL:
    IN 3
    AND #0x40
    BEQ PRINT_SYMBOL ; spin-loop until ready
    LD &1
    OUT 2
    CMP $NUL
    BEQ STOP
    RET

STOP:
    HLT

ORG 0x5E9
STRING: WORD 0xC2B5 ; ТЕ
WORD 0xC1C2 ; СТ
WORD 0x0

; Как общаются суперкомпьютеры? (interconnect)
; Enterprise Storage (NetworkAttachmentStorage, StorageAttachmentNetwork), (блочные, файловые блоки), (fiber channel)
; real-time devices