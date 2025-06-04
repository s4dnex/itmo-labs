NUM1_LOW: WORD 0x0
NUM1_HIGH: WORD 0x4140

NUM2_LOW: WORD 0x0
NUM2_HIGH: WORD 0x41CC

NUM1_EXP: WORD 0x0
NUM1_POW: WORD 0x0
NUM1_MANTIS_LOW: WORD 0x0
NUM1_MANTIS_HIGH: WORD 0x0

NUM2_EXP: WORD 0x0
NUM2_POW: WORD 0x0
NUM2_MANTIS_LOW: WORD 0x0
NUM2_MANTIS_HIGH: WORD 0x0

TEMP_LOW: WORD 0x0
TEMP_HIGH: WORD 0x0
TEMP_POW: WORD 0x0

START:
    CALL $PARSE_FLOAT_NUMS
    CALL $FLOAT_SUM
    LD $FLOAT_NUM_LOW
    HLT
    LD $FLOAT_NUM_HIGH
    HLT

PARSE_FLOAT_NUMS:
    ; num1 data
    LD NUM1_HIGH
    PUSH
    LD NUM1_LOW
    PUSH
    CALL $GET_MANTIS
    POP
    POP
    LD $MANTIS_LOW
    ST $NUM1_MANTIS_LOW
    LD $MANTIS_HIGH
    ST $NUM1_MANTIS_HIGH

    LD NUM1_HIGH
    PUSH
    CALL $GET_EXPONENT
    SWAP
    POP
    ST NUM1_EXP
    PUSH
    CALL $GET_POW
    SWAP
    POP
    ST $NUM1_POW

    ; num2 data
    LD NUM2_HIGH
    PUSH
    LD NUM2_LOW
    PUSH
    CALL $GET_MANTIS
    POP
    POP
    LD $MANTIS_LOW
    ST $NUM2_MANTIS_LOW
    LD $MANTIS_HIGH
    ST $NUM2_MANTIS_HIGH

    LD NUM2_HIGH
    PUSH
    CALL $GET_EXPONENT
    SWAP
    POP
    ST NUM2_EXP
    PUSH
    CALL $GET_POW
    SWAP
    POP
    ST $NUM2_POW
    RET


FLOAT_NUM_LOW: WORD ?
FLOAT_NUM_HIGH: WORD ?
FLOAT_NUM_MANTIS_LOW: WORD ?
FLOAT_NUM_MANTIS_HIGH: WORD ?
FLOAT_NUM_POW: WORD ?
FLOAT_NUM_SIGN: WORD ? ; 0x1 - NEG, 0x0 - POS
FLOAT_SUM: ; void (float) sum()
    PUSH ; temp variable
    LD $NUM1_POW
    CMP $NUM2_POW
    BGE SUM_PRENORMALIZE
        ; if (NUM1_POW < NUM2_POW) swap num1 and num2
        LD $NUM1_LOW
        ST $TEMP_LOW
        LD $NUM1_HIGH
        ST $TEMP_HIGH
        LD $NUM2_LOW
        ST $NUM1_LOW
        LD $NUM2_HIGH
        ST $NUM1_HIGH
        LD $TEMP_LOW
        ST $NUM2_LOW
        LD $TEMP_HIGH
        ST $NUM2_HIGH
        CALL $PARSE_FLOAT_NUMS
    SUM_PRENORMALIZE:
        LD $NUM1_POW
        ST $FLOAT_NUM_POW

        LD $NUM2_POW
        NEG
        ADD $NUM1_POW
        ST &0

        LD $NUM2_MANTIS_LOW
        ST FLOAT_NUM_MANTIS_LOW
        LD $NUM2_MANTIS_HIGH
        ST FLOAT_NUM_MANTIS_HIGH

        SUM_MANTIS_SHIFT:
            CLC
            LD $FLOAT_NUM_MANTIS_HIGH
            ROR
            ST $FLOAT_NUM_MANTIS_HIGH
            LD $FLOAT_NUM_MANTIS_LOW
            ROR
            ST $FLOAT_NUM_MANTIS_LOW
        LOOP &0
        JUMP SUM_MANTIS_SHIFT
    CHECK_SIGNS:
        LD $NUM1_HIGH
        PUSH
        CALL $GET_SIGN
        SWAP
        POP
        ST &0
        LD $NUM2_HIGH
        PUSH
        CALL $GET_SIGN
        SWAP
        POP
        CMP &0
        BEQ SUM_MANTISES
        JUMP COMPARE_MANTISES
    SUM_MANTISES:
        LD $NUM1_HIGH
        PUSH
        CALL $GET_SIGN
        SWAP
        POP
        ST $FLOAT_NUM_SIGN

        LD $NUM1_MANTIS_LOW
        ST $ADD32_A_LOW
        LD $NUM1_MANTIS_HIGH
        ST $ADD32_A_HIGH
        LD $FLOAT_NUM_MANTIS_LOW
        ST $ADD32_B_LOW
        LD $FLOAT_NUM_MANTIS_HIGH
        ST $ADD32_B_HIGH
        CALL $ADD32
        LD $ADD32_RES_LOW
        ST FLOAT_NUM_MANTIS_LOW
        LD $ADD32_RES_HIGH
        ST FLOAT_NUM_MANTIS_HIGH
        JUMP SUM_NORMALIZE
    COMPARE_MANTISES:
        NOP
        ; TODO
    SUM_NORMALIZE:
        LD $FLOAT_NUM_MANTIS_HIGH
        AND $MANTIS_OVERFLOW_BIT
        BZS CHECK_DENORMALIZATION

        ; OVERFLOW
        CLC
        LD $FLOAT_NUM_MANTIS_HIGH
        ROR
        ST $FLOAT_NUM_MANTIS_HIGH
        LD $FLOAT_NUM_MANTIS_LOW
        ROR
        ST $FLOAT_NUM_MANTIS_LOW
        LD $FLOAT_NUM_POW
        INC
        ST $FLOAT_NUM_POW
        JUMP SUM_RETURN

    CHECK_DENORMALIZATION:
        NOP
        ; TODO

    SUM_RETURN:
        LD #0
        ST $FLOAT_NUM_HIGH

        LD $FLOAT_NUM_SIGN
        BPL SUM_RETURN_POS
        LD $NEGATIVE_SIGN
        ST $FLOAT_NUM_HIGH
        
        SUM_RETURN_POS:
        LD #11
        HLT
        
        LD #7
        ST &0
        LD $FLOAT_NUM_POW
        ADD #127
        SUM_EXPONENT_SHIFT:
            CLC
            ROL
        LOOP &0
        JUMP SUM_EXPONENT_SHIFT


        OR $FLOAT_NUM_HIGH
        ST $FLOAT_NUM_HIGH
        LD $FLOAT_NUM_MANTIS_HIGH
        AND $HIGH_MANTIS_MASK
        OR $FLOAT_NUM_HIGH
        ST $FLOAT_NUM_HIGH

        LD $FLOAT_NUM_MANTIS_LOW
        ST $FLOAT_NUM_LOW
        
        SWAP
        POP
        RET


GET_SIGN: ; boolean get_sign(num_high)
    LD &1
    BMI GS_NEGATIVE
        ; if positive
        LD #0
        RET
    GS_NEGATIVE:
        LD #1
        RET

ADD32_A_LOW: WORD ?
ADD32_A_HIGH: WORD ?
ADD32_B_LOW: WORD ?
ADD32_B_HIGH: WORD ?
ADD32_RES_LOW: WORD ?
ADD32_RES_HIGH: WORD ?
ADD32: ; void (int32) add32(int16 a_low, int16 a_high, int16 b_low, int16 b_high)
    LD ADD32_A_LOW
    ADD ADD32_B_LOW
    ST ADD32_RES_LOW
    LD ADD32_A_HIGH
    ADC ADD32_B_HIGH
    ST ADD32_RES_HIGH
    RET

NUM_LOW: WORD ?
NUM_HIGH: WORD ?
MANTIS_LOW: WORD 0x0
MANTIS_HIGH: WORD 0x0

EXP_MASK: WORD 0x7F80 ; exponent mask
HIGH_MANTIS_MASK: WORD 0x007F ; 22..16 mantis' bits mask
MANTIS_HIDDEN_BIT: WORD 0x80
MANTIS_OVERFLOW_BIT: WORD 0x100
NEGATIVE_SIGN: WORD 0x8000

INT_PART_0: WORD 0x0
INT_PART_1: WORD 0x0
INT_PART_2: WORD 0x0
INT_PART_3: WORD 0x0

FRAC_PART_0: WORD 0x0
FRAC_PART_1: WORD 0x0
FRAC_PART_2: WORD 0x0
FRAC_PART_3: WORD 0x0

EXPONENT: WORD 0x0
POW: WORD 0x0

FLOAT_TO_BINARIES:
    LD NUM_HIGH
    PUSH
    LD NUM_LOW
    PUSH
    CALL $GET_MANTIS
    POP
    POP ; calculated mantis -> MANTIS_LOW, MANTIS_HIGH

    LD NUM_HIGH
    PUSH
    CALL $GET_EXPONENT
    SWAP
    POP
    ST $EXPONENT    ; calculated exponent -> EXPONENT
    PUSH
    CALL $GET_POW
    SWAP
    POP
    ST $POW ; calculated power -> POW
    
    LD $MANTIS_HIGH
    PUSH
    LD $MANTIS_LOW
    PUSH
    LD $POW
    PUSH
    CALL $GET_INTEGER_PARTS ; calculated integer parts -> INT_PART_0, INT_PART_1, INT_PART_2, INT_PART_3 
    POP
    POP
    POP
    LD $INT_PART_0
    HLT
    LD $INT_PART_1
    HLT
    LD $INT_PART_2
    HLT
    LD $INT_PART_3
    HLT

    LD $MANTIS_HIGH
    PUSH
    LD $MANTIS_LOW
    PUSH
    LD $POW
    PUSH
    CALL $GET_FRACTION_PARTS ; calculated fraction parts -> FRAC_PART_0, FRAC_PART_1, FRAC_PART_2, FRAC_PART_3 
    POP
    POP
    POP
    LD $FRAC_PART_0
    HLT
    LD $FRAC_PART_1
    HLT
    LD $FRAC_PART_2
    HLT
    LD $FRAC_PART_3
    HLT

GET_EXPONENT: ; uint8 get_exponent(num_high)
    PUSH
    LD #7
    ST &0
    LD &2
    AND $EXP_MASK
    GET_EXPONENT_LOOP: ASR
    LOOP &0
    JUMP GET_EXPONENT_LOOP
    SWAP
    POP
    RET

GET_POW: ; int8 get_pow(exponent)
    LD &1
    ADD #-127
    RET

GET_MANTIS: ; void (int32) get_mantis(num_low, num_high)
    LD &2
    AND $HIGH_MANTIS_MASK
    OR $MANTIS_HIDDEN_BIT ; add hidden 24th bit to high mantis
    ST $MANTIS_HIGH
    LD &1
    ST $MANTIS_LOW
    RET

GET_INTEGER_PARTS: ; void (int64) get_integer_part(pow, mantis_low, mantis_high)
    CLA
    PUSH    ; int3
    PUSH    ; int2
    PUSH
    PUSH
    LD &6   ; mantis_low -> int0
    ST &0   ; int0
    LD &7   ; mantis_high -> int1
    ST &1   ; int1
    LD &5
    GIP_IF_GREATER_THAN_23:
        CMP #23 ; if (pow >= 23)
        BLT GIP_IF_LESS_THAN_0 ; jump to if (pow < 0)
        
        CMP #65
        BGE GIP_RETURN ; if (pow >= 65) return because won't be able to store such value

        LD #23  ; pow - 23 -> pow
        NEG     ;
        ADD &5  ; 
        ST &5   ;

        GIP_ASL:
            LD &0
            ASL     ; AC15 -> C 
            ST &0
            LD &1
            ROL     ; C -> AC0
            ST &1
            LD &2
            ROL
            ST &2
            LD &3
            ROL
            ST &3
        LOOP &5
        JUMP GIP_ASL
        JUMP GIP_RETURN
    GIP_IF_LESS_THAN_0: 
        CMP #0 ; if (pow < 0)
        BGE GIP_BETWEEN_0_AND_23 ; jump to 0 <= pow < 23
        CLA
        ST &0
        ST &1
        ST &2
        ST &3
        JUMP GIP_RETURN
    GIP_BETWEEN_0_AND_23: 
        NEG
        ADD #23
        ST &5
        GIP_ASR:
            CLC
            LD &1
            ROR
            ST &1 ; mantis_high >>
            LD &0
            ROR
            ST &0 ; mantis_low >>
        LOOP &5
        JUMP GIP_ASR
        JUMP GIP_RETURN

    GIP_RETURN:
        POP
        ST $INT_PART_0
        POP
        ST $INT_PART_1
        POP
        ST $INT_PART_2
        POP
        ST $INT_PART_3
        RET

GET_FRACTION_PARTS: ; void (int64) get_fraction_part(pow, mantis_low, mantis_high)
    CLA
    PUSH ; frac3
    PUSH ; frac2
    PUSH    ; frac1
    PUSH    ; frac0
    LD &7   ; mantis_high -> frac3
    ST &3   ; 
    LD &6   ; mantis_low -> frac2
    ST &2   ;

    SHIFT_MANTIS:
        LD #8
        PUSH
        SHIFT_LOOP:
            LD &3
            ASL
            ST &3
            LD &4
            ROL
            ST &4
        LOOP &0
        JUMP SHIFT_LOOP
        POP
    
    LD &5   ; pow -> AC
    GFP_IF_GREATER_THAN_23:
        CMP #23 ; if (pow >= 23)
        BLT GFP_IF_LESS_THAN_0 ; jump to if (pow < 0)
        CLA
        ST &0
        ST &1
        ST &2
        ST &3
        JUMP GFP_RETURN
    GFP_IF_LESS_THAN_0: 
        CMP #0 ; if (pow < 0)
        BGE GFP_BETWEEN_0_AND_23 ; jump to 0 <= pow < 23

        CMP #-65
        BLO GFP_RETURN ; if (pow < -65) return because won't be able to store such value


        LD &5
        NEG
        ADD #-23
        ST &5

        GFP_ASR:
            CLC 
            LD &3
            ROR
            ST &3
            LD &2
            ROR      
            ST &2
            LD &1
            ROR  
            ST &1
            LD &0
            ROR
            ST &0
        LOOP &5
        JUMP GFP_ASR
        JUMP GFP_RETURN

    GFP_BETWEEN_0_AND_23:
        ADD #1
        ST &5
        GFP_ASL:
            LD &2
            ASL     ; AC15 -> C 
            ST &2
            LD &3
            ROL     ; C -> AC0
            ST &3
        LOOP &5
        JUMP GFP_ASL
        JUMP GFP_RETURN

    GFP_RETURN:
        POP
        ST $FRAC_PART_0
        POP
        ST $FRAC_PART_1
        POP
        ST $FRAC_PART_2
        POP
        ST $FRAC_PART_3
        RET