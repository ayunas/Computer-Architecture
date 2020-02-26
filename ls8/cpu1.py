"""CPU functionality."""

import sys
from program import program,LDI,TARGET_VAL,PRN,HLT

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*len(program)
        self.register = [0]*8 #r0,r1,r2,r3,r4,r5,r6,r7
        self.pc = 0  #index of the pointer for the ram
        self.MAR = None  #Memory Address Register - holds memory address to read or write from
        self.MDR = None #Memory Data Register - holds memory address of value that has been read.  
        self.halted = True

    def load(self,program):
        """Load a program into memory."""
        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self):
        #MAR = Memory Address Register.  the address containing the data to be read from the register
        MAR = self.ram[self.pc + 1]
        print(self.register[MAR])

    # def ram_write(self):
    #     #MDR = Memory Data Register. the data sent 
    #     MAR = self.ram[self.pc + 1]
    #     MDR = self.ram[self.pc + 2]
    #     self.register[MAR] = MDR

    def reg_read(self):
        print(self.register[self.MAR])
    
    def reg_write(self):
        self.register[self.MAR] = self.MDR
        return self.register[self.MAR]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        try:
            self.load(program)
            self.halted = False
            print('RAM loaded successfully...')
            data = [bin(entry) for entry in self.ram]
            print(data)

        except Exception:
            print('there has been an error loading the program')
            return
        
        while self.halted is False:
            instruction = self.ram[self.pc]

            if instruction == LDI:  #LOAD IMMEDIATE
                self.MAR = self.ram[self.pc + 1] #set the register address as MAR
                self.MDR = self.ram[self.pc + 2] #set the data at the register address as MDR
                self.reg_write()
                self.pc += 3
            
            elif instruction == PRN:  #PRINT
                self.reg_read()
                self.pc += 2
            
            elif instruction == HLT:
                self.pc += 1
                self.halted = True
            
            else:
                print(f"Error occured at register index: {self.pc}")

            

c = CPU()
c.run()
