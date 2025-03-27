ORG 0x1
CALL $START

ORG 0xD0
START:
    PUSH
    LD #7
    ST &0
    CALL $FIB 
    SWAP
    POP
    HLT

ORG 0xFB
FIB:
    PUSH
    PUSH
    CLA
    ST &1
    ST &0
    LD &3
    IF_ZERO:
        CMP #1
        BGE IF_ONE
        CLA
        JUMP FIB_END
    IF_ONE: 
        CMP #1
        BNE NEXT
        LD #1
        JUMP FIB_END
    NEXT:
        PUSH
        LD &4
        SUB #1
        ST &0
        CALL $FIB
        SWAP
        POP
        ST &1
        
        PUSH
        LD &4
        SUB #2
        ST &0
        CALL $FIB
        SWAP
        POP
        
        ADD &1
    FIB_END:
        SWAP
        POP
        SWAP
        POP
        RET

; регистровые окна, как работают exceptions в C++, "необычные" вызовы функций
