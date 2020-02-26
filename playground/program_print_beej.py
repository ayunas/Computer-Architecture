#instructions for this particular print beej program
#assign numerical values 
#job as a software engineer is to find holes in the spec and question until it is clear

#INSTRUCTIONS
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4


memory = [ #EVERY instruction at least 1 byte long.  
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    #############
    SAVE_REG, #SAVE VALUE 10 IN R2.  LDI in LS-8.  3 bytes long
    30,  #REFERRING TO R2 NOT THE HALT COMMAND
    2,   ############## INSTRUCTION 3 ARGUMENTS LONG
    ###############
    PRINT_REG, #save the value 10 in register R2. (total of 8 register variables available)  in python: print('Beej') r2 = 10 print r2
    2,
    ############### 2 byte instruction
    HALT
]


register = [0] * 8 #like variables, limited fixed # of them. fixed names:  R0,R1,R2,R3,R4,R5,R6,R7

pc = 0  #pc is known as the program counter. referring to the current_index.  or pointer to currently executed instruction
halted = False

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_BEEJ:
        print("Beej")
        pc += 1

    elif instruction == SAVE_REG:
        value = memory[pc + 1]
        reg_num = memory[pc + 2]

        register[reg_num] = value
        pc += 3
    
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2
    
    elif instruction == HALT:
        halted = True
        pc += 1
    
    else:
        print('error occured at index', pc)



