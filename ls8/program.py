LDI = 0b10000010
TARGET_VAL = 0b00001000
PRN = 0b01000111
HLT = 0b00000001

 # From print8.ls8
program = [
            ###################
            LDI, # LDI R0,8  3 byte instruction.  #writing to register[0] the target value of 8 (0b1000)
            0b00000000,
            TARGET_VAL,
            ##################
            PRN, # PRN R0  - 2 byte instruction - Read from the register[0]
            0b00000000,
            ##################
            HLT # HLT Stop operations
        ]
