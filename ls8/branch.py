LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111

class Branch:
    def __init__(self):
        self.data = {}
        self.data[LDI] = self.handle_ldi
        self.data[MUL] = self.handle_mul
        self.data[PRN] = self.handle_prn
        self.data['WRITE'] = self.handle_write
    
    def handle_ldi(self,ram,pc,register):
          #LOAD IMMEDIATE
        address = ram[pc + 1] #set the register address as MAR
        data = ram[pc + 2] #set the data at the register address as MDR
        self.handle_write(address,data,register)
        pc += 3
    
    def handle_write(self,address, data, register):
        register[address] = data
    
    def handle_mul(self):
        pass

    def handle_prn(self):
        pass
    
    def run(self,ram,pc,register):
        ir = LDI
        print('ram in branch', ram)
        self.data[ir](ram,pc,register)


