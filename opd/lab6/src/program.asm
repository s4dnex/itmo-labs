ORG 0x0
V0: WORD $DEFAULT, 0x180
V1: WORD $DEFAULT, 0x180 
V2: WORD $INT2,    0x180
V3: WORD $INT3,    0x180
V4: WORD $DEFAULT, 0x180
V5: WORD $DEFAULT, 0x180
V6: WORD $DEFAULT, 0x180
V7: WORD $DEFAULT, 0x180

DEFAULT: IRET

ORG 0x17
X: WORD ?
MIN: WORD 0xFFC3 ; -61
MAX: WORD 0x0043 ; 67 (макс. 66, но так как сравниваем с помощью BGE, то берем 67)

ORG 0x20
START:
    DI
    CLA
    OUT 0x1
    OUT 0x3
    OUT 0xB
    OUT 0xE
    OUT 0x12
    OUT 0x16
    OUT 0x1A
    OUT 0x1E
    LD #0xA     ; 1010 - разрешаем прерывание, вектор V2
    OUT 5       ; ВУ-2
    LD #0xB     ; 1011 - разрешаем прерывание, вектор V3
    OUT 7       ; ВУ-3
    EI


MAIN:
    DI
    LD X
    INC
    INC
    CALL $CHECK
    ST X
    EI
    JUMP MAIN

CHECK:
    CMP $MIN
    BLT LOAD_MIN
    CMP $MAX
    BGE LOAD_MIN
    JUMP CHECK_RETURN
    LOAD_MIN: 
        HLT ; NOP
        LD $MIN
    CHECK_RETURN: RET

INT2:
    PUSH
    IN 4    ; y
    SXTB
    HLT     ; NOP
    PUSH
    LD $X   ; x
    HLT     ; NOP
    NEG     ; -x
    ADD &0  ; -x + y
    ADD &0  ; -x + 2*y
    ADD &0  ; -x + 3*y
    SWAP
    POP
    HLT     ; NOP
    ST $X
    POP
    IRET

INT3:
    PUSH
    LD $X   ; x
    HLT     ; NOP
    ASL     ; 2*x
    NEG     ; -2*x
    ADD #5  ; -2*x + 5
    HLT     ; NOP
    OUT 6
    POP
    IRET