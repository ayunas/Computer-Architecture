"""CPU functionality."""
'''Incorrect usage of the stack with an external stack data structure.
The idea is to create a virtual stack inside of the RAM. and reference it with the SP or stack pointer.  The stack starts at the back of the RAM, and every value is pushed on top of it, or from back to front.  that is why the sp is decremented by 1 after pushing.
and when poping from the stack, first you increment the SP to point it to the top of the stack.  then you 0 out the stack at ram[sp], and set it to the register address that was passed in to the pop() method.
'''

import sys
from branch import Branch
# from stack import Stack

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*(2**8)
        self.register = [0]*8 #r0,r1,r2,r3,r4,r5,r6,r7
        self.PC = 0  #index of the pointer for the ram
        self.MAR = None  #Memory Address Register - holds memory address to read or write from
        self.MDR = None #Memory Data Register - holds memory address of value that has been read.  
        self.halted = True
        self.dispatch = {'LDI' : 130, 'MUL': 162, 'PRN': 71,'PUSH': 69, 'POP': 70, 'CALL':80, 'HLT': 1, 'MULT2PRINT':160, 'RET':17}
        self.SP = -1

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} filename not specified", file=sys.stderr)
            # raise FileNotFoundError
            sys.exit(1)
        try:
            filename = sys.argv[1]
            print('filename: ', filename)
            address = 0
            file = open(filename, 'r')
        except IOError:
            print('Could not open/read file', filename)
            sys.exit()

        instructions = []
        for line in file:
            break_up = line.split('#')
            ins = break_up[0].strip()
            # ins = int(ins,2)
            # ins = format(ins,"08b")
            if ins == '':
                continue
            self.ram[address] = int(ins,2)
            address += 1 
        file.close()

    def prn(self,address):
        self.MAR = address
        print(self.register[self.MAR])
        self.MAR = None
    
    def ldi(self,address,data):
        self.MAR = address
        self.MDR = data
        self.register[self.MAR] = self.MDR
        self.MAR = None
        self.MDR = None
        print(f'load immediate (LDI) from ram to register[{address}]:', self.register[address])

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b] 
        else:
            raise Exception("Unsupported ALU operation")
    
    def push(self,r_address):
        # Push the value in the given register on the stack.
        print('r_address in push', r_address)
        self.MDR = self.register[r_address]
        self.ram[self.SP] = self.MDR
        self.SP -= 1
        self.MDR = None
        print('ram after pushing', self.ram)
    
    def pop(self,r_address):
        #Pop the value at the top of the stack into the given register.
        self.SP += 1
        popped = self.ram[self.SP]
        self.ram[self.SP] = 0
        self.register[r_address] = popped
        print('popped', popped)
        print(f"popped into register[{r_address}]: ", self.register[r_address])
        print('ram after popping', self.ram)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    ####using a branch_table and LDI is loading into ram, but how to do so for all LDI values in O(1)???#######################
    # def run(self):
    #     try:
    #         self.load()
    #         self.halted = False
    #     except FileNotFoundError:
    #         sys.exit()
        
    #     branch_table = Branch()
    #     branch_table.run(self.ram,self.PC,self.register)
    #     print(self.register)
    ############################################################################################################################

    def run(self):
        """Run the CPU."""
        try:
            self.load()
            self.halted = False
        except FileNotFoundError:
            sys.exit()
        
        while self.halted is False:
            instruction = self.ram[self.PC]
            # print('instruction at beginning of while loop', 'PC:', self.PC, instruction)

            if instruction == self.dispatch['LDI']:  #LOAD IMMEDIATE
                # print('at the LDI instruction')
                address = self.ram[self.PC + 1] #set the register address as MAR
                data = self.ram[self.PC + 2] #set the data at the register address as MDR
                self.ldi(address,data)
                self.PC += 3
            
            elif instruction == self.dispatch['MUL']:
                reg_a = self.ram[self.PC + 1]
                reg_b = self.ram[self.PC + 2]
                self.alu('MUL',reg_a,reg_b)
                self.PC += 3
            
            elif instruction == self.dispatch['PUSH']:
                r_address = self.ram[self.PC + 1]
                self.push(r_address)
                self.PC += 2

            elif instruction == self.dispatch['POP']:
                # print('pop', instruction)
                r_address = self.ram[self.PC + 1]
                # print('r address', r_address)
                self.pop(r_address)
                self.PC += 2

            elif instruction == self.dispatch['PRN']:  #PRINT
                address = self.ram[self.PC + 1]
                self.prn(address)
                self.PC += 2
                # print('self.PC after print', self.PC)
            
            elif instruction == self.dispatch['HLT']:
                self.PC += 1
                self.halted = True

            elif instruction == self.dispatch['CALL']:
                # print('at the call instruction')
                # subroutine_address = self.ram[self.PC + 1]
                # self.push(self.ram[self.PC + 2]) #push next instruction to stack
                ####################################################
                next_instruction_pc = self.PC + 2
                
                # print('next_instruction', next_instruction_pc)
                # self.ram[self.SP] = next_instruction
                self.ram[self.SP] = next_instruction_pc
                self.SP -= 1
                ####################################################
                r_address = self.ram[self.PC + 1] #register containing the subroutine
                subroutine_address = self.register[r_address]
                self.PC = subroutine_address
                # print('subroutine: ', self.ram[self.PC])
                # self.PC += 2
            elif instruction == self.dispatch['MULT2PRINT']:
                # print('subroutine instruction reached')
                r_1 = self.ram[self.PC + 1]
                r_2 = self.ram[self.PC + 2]
                print(r_1,r_2)
                self.alu('ADD',r_1,r_2)
                self.PC += 3
            elif instruction == self.dispatch['RET']:
                # print('return instruction reached', self.PC)
                self.SP += 1
                popped_instruction_pc = self.ram[self.SP]
                self.ram[self.SP] = 0
                # print('popped_instruction', popped_instruction_pc)
                self.PC = popped_instruction_pc
            else:
                print(f"Unknown instruction at index: {self.PC}")
                sys.exit()

c = CPU()
c.run()
