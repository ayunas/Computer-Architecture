"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*(2**8)
        self.register = [0]*8 #r0,r1,r2,r3,r4,r5,r6,r7
        self.pc = 0  #index of the pointer for the ram
        self.MAR = None  #Memory Address Register - holds memory address to read or write from
        self.MDR = None #Memory Data Register - holds memory address of value that has been read.  
        self.halted = True
        self.dispatch = {'LDI' : 130, 'MUL': 162, 'PRN': 71, 'HLT': 1}

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

    # def ram_read(self):
    #     #MAR = Memory Address Register.  the address containing the data to be read from the register
    #     MAR = self.ram[self.pc + 1]
    #     print(self.register[MAR])

    # def ram_write(self):
    #     #MDR = Memory Data Register. the data sent 
    #     MAR = self.ram[self.pc + 1]
    #     MDR = self.ram[self.pc + 2]
    #     self.register[MAR] = MDR

    def reg_read(self,address):
        self.MAR = address
        print(self.register[self.MAR])
        self.MAR = None
    
    def reg_write(self,address,data):
        self.MAR = address
        self.MDR = data
        self.register[self.MAR] = self.MDR
        self.MAR = None
        self.MDR = None

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b] 
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
            self.load()
            self.halted = False
        except FileNotFoundError:
            sys.exit()
        
        while self.halted is False:
            instruction = self.ram[self.pc]

            if instruction == self.dispatch['LDI']:  #LOAD IMMEDIATE
                address = self.ram[self.pc + 1] #set the register address as MAR
                data = self.ram[self.pc + 2] #set the data at the register address as MDR
                self.reg_write(address,data)
                self.pc += 3
            
            elif instruction == self.dispatch['MUL']:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('MUL',reg_a,reg_b)
                self.pc += 3

            elif instruction == self.dispatch['PRN']:  #PRINT
                address = self.ram[self.pc + 1]
                self.reg_read(address)
                self.pc += 2
            
            elif instruction == self.dispatch['HLT']:
                self.pc += 1
                self.halted = True
            
            else:
                print(f"Error occured at register index: {self.pc}")
                sys.exit()

c = CPU()
c.run()
