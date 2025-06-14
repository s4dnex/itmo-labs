; first number
NUM1_LOW: WORD 0x1000
NUM1_HIGH: WORD 0x4480

; second number
NUM2_LOW: WORD 0x0
NUM2_HIGH: WORD 0xC480

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
    ST $NUM_LOW
    LD $FLOAT_NUM_HIGH
    ST $NUM_HIGH
    LD $FLOAT_NUM_SIGN
    ST $NUM_SIGN
    CALL $FLOAT_TO_BINARIES
    CALL $PRINT_BINARIES
    HLT

PARSE_FLOAT_NUMS:
    ; LD #10
    ; HLT
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
        ; LD #11
        ; HLT ; DEBUG
        LD $NUM1_POW
        ST $FLOAT_NUM_POW

        LD $NUM2_POW
        NEG
        ADD $NUM1_POW
        ST &0
        BZS CHECK_SIGNS

        SUM_MANTIS_SHIFT:
            CLC
            LD $NUM2_MANTIS_HIGH
            ROR
            ST $NUM2_MANTIS_HIGH
            LD $NUM2_MANTIS_LOW
            ROR
            ST $NUM2_MANTIS_LOW
        LOOP &0
        JUMP SUM_MANTIS_SHIFT

    CHECK_SIGNS:
        ; LD #11
        ; HLT ; DEBUG
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
        LD $NUM2_MANTIS_LOW
        ST $ADD32_B_LOW
        LD $NUM2_MANTIS_HIGH
        ST $ADD32_B_HIGH
        CALL $ADD32
        LD $ADD32_RES_LOW
        ST FLOAT_NUM_MANTIS_LOW
        LD $ADD32_RES_HIGH
        ST FLOAT_NUM_MANTIS_HIGH
        JUMP SUM_NORMALIZE
    
    COMPARE_MANTISES:
        ; LD #11
        ; HLT ; debug
        LD $NUM1_MANTIS_HIGH
        CMP $NUM2_MANTIS_HIGH
        BEQ COMPARE_LOWER_MANTISES
        BLT NUM2_MANTIS_LARGER

    NUM1_MANTIS_LARGER:
        ; LD #11
        ; HLT ; DEBUG
        LD $NUM1_HIGH
        PUSH
        CALL $GET_SIGN
        SWAP
        POP
        ST $FLOAT_NUM_SIGN

        LD $NUM1_MANTIS_LOW
        ST $SUB32_A_LOW
        LD $NUM1_MANTIS_HIGH
        ST $SUB32_A_HIGH
        LD $NUM2_MANTIS_LOW
        ST $SUB32_B_LOW
        LD $NUM2_MANTIS_HIGH
        ST $SUB32_B_HIGH
        CALL $SUB32
        LD $SUB32_RES_LOW
        ST $FLOAT_NUM_MANTIS_LOW
        LD $SUB32_RES_HIGH
        ST $FLOAT_NUM_MANTIS_HIGH
        JUMP SUM_NORMALIZE
    
    NUM2_MANTIS_LARGER:
        LD $NUM2_HIGH
        PUSH
        CALL $GET_SIGN
        SWAP
        POP
        ST $FLOAT_NUM_SIGN

        LD $NUM2_MANTIS_LOW
        ST $SUB32_A_LOW
        LD $NUM2_MANTIS_HIGH
        ST $SUB32_A_HIGH
        LD $NUM1_MANTIS_LOW
        ST $SUB32_B_LOW
        LD $NUM1_MANTIS_HIGH
        ST $SUB32_B_HIGH
        CALL $SUB32
        LD $SUB32_RES_LOW
        ST $FLOAT_NUM_MANTIS_LOW
        LD $SUB32_RES_HIGH
        ST $FLOAT_NUM_MANTIS_HIGH
        JUMP SUM_NORMALIZE

    COMPARE_LOWER_MANTISES:
        LD $NUM1_MANTIS_LOW
        CMP $NUM2_MANTIS_LOW
        BGE NUM1_MANTIS_LARGER
        JUMP NUM2_MANTIS_LARGER

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
        LD $FLOAT_NUM_MANTIS_HIGH
        BZC CHECK_UNDERFLOW
        LD $FLOAT_NUM_MANTIS_LOW
        BZS SUM_IS_ZERO

        CHECK_UNDERFLOW:
            LD $FLOAT_NUM_MANTIS_HIGH 
            SXTB
            BMI SUM_RETURN

            ; "UNDERFLOW"
            CLC
            LD $FLOAT_NUM_MANTIS_LOW
            ROL
            ST $FLOAT_NUM_MANTIS_LOW
            LD $FLOAT_NUM_MANTIS_HIGH
            ROL
            ST $FLOAT_NUM_MANTIS_HIGH
            LD $FLOAT_NUM_POW
            DEC
            ST $FLOAT_NUM_POW
            JUMP CHECK_UNDERFLOW

    SUM_IS_ZERO:
        CLA
        ST $FLOAT_NUM_MANTIS_LOW
        ST $FLOAT_NUM_MANTIS_HIGH
        ST $FLOAT_NUM_SIGN
        ST $FLOAT_NUM_POW
        BZS FLOAT_ASSEMBLE
    
    SUM_RETURN:
        LD $FLOAT_NUM_SIGN
        BZS SET_POSITIVE_SIGN

        SET_NEGATIVE_SIGN:
            LD $NEGATIVE_SIGN
            ST $FLOAT_NUM_HIGH
            JUMP SUM_RETURN_ASSEMBLE
        
        SET_POSITIVE_SIGN:
            CLA
            ST $FLOAT_NUM_HIGH
            JUMP SUM_RETURN_ASSEMBLE

        SUM_RETURN_ASSEMBLE:    ; HIGH = SIGN (15) + EXPONENT (14..7) + MANTIS_HIGH(6..0) 
                                ; LOW  = MANTIS_LOW (15..0)
            LD #7
            ST &0
            LD $FLOAT_NUM_POW
            ADD #127
            SUM_EXPONENT_SHIFT:
                CLC
                ROL
            LOOP &0
            JUMP SUM_EXPONENT_SHIFT ; SHIFT EXPONENT TO (14..7) BITS

            FLOAT_ASSEMBLE:
            OR $FLOAT_NUM_HIGH      ; SIGN | EXPONENT (14..7)
            ST $FLOAT_NUM_HIGH
            LD $FLOAT_NUM_MANTIS_HIGH   ;
            AND $HIGH_MANTIS_MASK       ; MANTIS_HIGH & 0x7F
            OR $FLOAT_NUM_HIGH          ; SIGN | EXPONENT(14..7) | MANTIS_HIGH(6..0)
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

NEG32_NUM_LOW: WORD ?
NEG32_NUM_HIGH: WORD ?
NEG32_RES_LOW: WORD ?
NEG32_RES_HIGH: WORD ?
NEG32: ; void (int32) neg32(int16 num_low, int16 num_high)
    LD NEG32_NUM_LOW
    NOT
    ST $ADD32_A_LOW
    LD NEG32_NUM_HIGH
    NOT
    ST $ADD32_A_HIGH
    LD #1
    ST $ADD32_B_LOW
    CLA
    ST $ADD32_B_HIGH
    CALL $ADD32
    LD $ADD32_RES_LOW
    ST NEG32_RES_LOW
    LD $ADD32_RES_HIGH
    ST NEG32_RES_HIGH
    RET

SUB32_A_LOW: WORD ?
SUB32_A_HIGH: WORD ?
SUB32_B_LOW: WORD ?
SUB32_B_HIGH: WORD ?
SUB32_RES_LOW: WORD ?
SUB32_RES_HIGH: WORD ?
SUB32: ; void (int32) sub32(int16 a_low, int16 a_high, int16 b_low, int16 b_high)
    LD SUB32_B_LOW
    ST $NEG32_NUM_LOW
    LD SUB32_B_HIGH
    ST $NEG32_NUM_HIGH
    CALL $NEG32
    LD $NEG32_RES_LOW
    ST $ADD32_B_LOW
    LD $NEG32_RES_HIGH
    ST $ADD32_B_HIGH
    LD SUB32_A_LOW
    ST $ADD32_A_LOW
    LD SUB32_A_HIGH
    ST $ADD32_A_HIGH
    CALL $ADD32
    LD $ADD32_RES_LOW
    ST SUB32_RES_LOW
    LD $ADD32_RES_HIGH
    ST SUB32_RES_HIGH
    RET

NUM_LOW: WORD 0x0
NUM_HIGH: WORD 0x0
MANTIS_LOW: WORD 0x0
MANTIS_HIGH: WORD 0x0
NUM_SIGN: WORD 0x0
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
    POP             ; calculated mantis -> MANTIS_LOW, MANTIS_HIGH

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
    ST $POW         ; calculated power -> POW
    
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
    ; HLT
    LD $INT_PART_1
    ; HLT
    LD $INT_PART_2
    ; HLT
    LD $INT_PART_3
    ; HLT

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
    ; HLT
    LD $FRAC_PART_1
    ; HLT
    LD $FRAC_PART_2
    ; HLT
    LD $FRAC_PART_3
    ; HLT

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
    
    GIP_IF_NUM_IS_ZERO:
        CMP #-127
        BZC GIP_IF_GREATER_THAN_23
        CLA
        ST &0
        ST &1
        ST &2
        ST &3
        JUMP GIP_RETURN
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
    PUSH    ; frac3
    PUSH    ; frac2
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
    GFP_IF_NUM_IS_ZERO:
        CMP #-127
        BZC GFP_IF_GREATER_THAN_23
        CLA
        ST &0
        ST &1
        ST &2
        ST &3
        JUMP GFP_RETURN
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
        ; HLT
        CMP #0 ; if (pow < 0)
        BGE GFP_BETWEEN_0_AND_23 ; jump to 0 <= pow < 23

        CMP #-65
        BLT GFP_RETURN ; if (pow < -65) return because won't be able to store such value


        LD &5
        NEG
        ADD #-23
        ST &5
        BLT GFP_RETURN
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


ISO_SYMBOL_ZERO: WORD 0x30
ISO_SYMBOL_PLUS: WORD 0x2B ; MINUS - 2D

DIGITS: WORD 16 DUP (?)
DIGITS_SIZE: WORD 0x0
DIGITS_PTR: WORD $DIGITS

PRINT_BINARIES:
    LD $NUM_SIGN
    CALL $PRINT_SIGN_ISO8859
    LD $INT_PART_0
    ST $DIV32_NUM_LOW
    LD $INT_PART_1
    ST $DIV32_NUM_HIGH
    CALL $DIV32_BY_10
    ; LD #12
    ; HLT ; debug
    STORE_INT_DIGITS_LOOP:
        LD $DIV32_REM
        ST (DIGITS_PTR)+
        LD $DIGITS_SIZE
        INC
        ST $DIGITS_SIZE
        LD $DIV32_QUOT
        BZS PRINT_INT_DIGITS_LOOP
        BLT PRINT_INT_DIGITS_LOOP
        ST $DIV32_NUM_LOW
        CLA
        ST $DIV32_NUM_HIGH
        CALL $DIV32_BY_10
        JUMP STORE_INT_DIGITS_LOOP

    PRINT_INT_DIGITS_LOOP:
        LD -(DIGITS_PTR)
        CALL $PRINT_DIGIT_ISO8859
        LOOP DIGITS_SIZE
        JUMP PRINT_INT_DIGITS_LOOP

    CALL $PRINT_DOT_ISO8859

    LD $FRAC_PART_2
    ST $MUL32_NUM_LOW
    LD $FRAC_PART_3
    ST $MUL32_NUM_HIGH
    CALL $MUL32_BY_1000
    LD $MUL32_RES
    ST $DIV32_NUM_LOW
    CLA
    ST $DIV32_NUM_HIGH
    CALL $DIV32_BY_10

    STORE_FRAC_DIGITS_LOOP:
        LD $DIV32_REM
        ST (DIGITS_PTR)+
        LD $DIGITS_SIZE
        INC
        ST $DIGITS_SIZE
        LD $DIV32_QUOT
        BZS PRINT_FRAC_DIGITS_LOOP
        BLT PRINT_FRAC_DIGITS_LOOP
        ST $DIV32_NUM_LOW
        CLA
        ST $DIV32_NUM_HIGH
        CALL $DIV32_BY_10
        JUMP STORE_FRAC_DIGITS_LOOP
    
    PRINT_FRAC_DIGITS_LOOP:
        LD -(DIGITS_PTR)
        CALL $PRINT_DIGIT_ISO8859
        LOOP DIGITS_SIZE
        JUMP PRINT_FRAC_DIGITS_LOOP

    CALL $PRINT_NEWLINE_ISO8859L
    RET

DIV32_NUM_LOW: WORD 0x0
DIV32_NUM_HIGH: WORD 0x0
DIV32_QUOT: WORD 0x0
DIV32_REM: WORD 0x0
DIV32_BY_10:
    CLA
    ST $DIV32_REM
    ST $DIV32_QUOT
    DIV32_LOOP_DIV:
        LD DIV32_NUM_HIGH
        CMP #0
        BZS DIV32_CHECK_LOW
        BGE DIV32_SUB

        DIV32_CHECK_LOW:
            LD DIV32_NUM_LOW
            CMP #10
            BLT DIV32_RETURN

    DIV32_SUB:
        LD $DIV32_NUM_LOW
        ST $SUB32_A_LOW
        LD $DIV32_NUM_HIGH
        ST $SUB32_A_HIGH
        LD #10
        ST $SUB32_B_LOW
        CLA
        ST $SUB32_B_HIGH
        CALL $SUB32
        LD $SUB32_RES_LOW
        ST $DIV32_NUM_LOW
        LD $SUB32_RES_HIGH
        ST $DIV32_NUM_HIGH
        LD $DIV32_QUOT
        INC
        ST $DIV32_QUOT
        JUMP DIV32_LOOP_DIV

    DIV32_RETURN:
        LD $DIV32_NUM_LOW
        ST $DIV32_REM
        RET
    
MUL32_NUM_LOW: WORD 0x0
MUL32_NUM_HIGH: WORD 0x0
MUL32_RES: WORD 0x0
MUL32_BY_1000:
    LD MUL32_NUM_HIGH
    BZC MUL32_NOT_ZERO
    CLA
    ST MUL32_RES
    RET
    
    MUL32_NOT_ZERO: 
    LD #10
    PUSH
    MUL32_ASL:
        LD $MUL32_NUM_LOW
        ASL     ; AC15 -> C 
        ST $MUL32_NUM_LOW
        LD $MUL32_NUM_HIGH
        ROL     ; C -> AC0
        ST $MUL32_NUM_HIGH
        LD $MUL32_RES
        ROL
        ST $MUL32_RES
    LOOP &0
    JUMP MUL32_ASL
    SWAP
    POP
    RET

PRINT_SIGN_ISO8859: ; void print_sign_iso8859(boolean sign)
    ASL             ; if ac = 0x1, then we have minus sign, which is 2 steps away from plus, so *2
    ADD $ISO_SYMBOL_PLUS
    OUT 0xC
    RET

PRINT_DOT_ISO8859:
    LD #3
    ADD $ISO_SYMBOL_PLUS
    OUT 0xC
    RET

PRINT_DIGIT_ISO8859: ; void print_digit_iso8859(int4 digit) 
    ADD $ISO_SYMBOL_ZERO; ac=digit in binary form, so add zero digit in iso8859 and get correct one
    OUT 0xC
    RET

PRINT_NEWLINE_ISO8859L:
    LD #10
    OUT 0xC
    RET
