"""CPU functionality."""

import sys

class Memory():
    """Main CPU class."""
    def __init__(self, size):
        """Construct a new CPU."""
        self.size = size
        self.clear()
    def clear(self):
        self.primary_memory = [0] * self.size
    def decode_bytes(self, address):                      #Read Bytes
        if address < 0 or address > self.size -1:
            raise ReferenceError('memory performance')
        return self.primary_memory[address]
    def compose_bytes(self, address, data):                #write bytes
        if address < 0 or address > self.size -1:
            raise ReferenceError('Memory Performing')
        try:
            rational_number = int(data)
            if rational_number > 0xFF:
                raise TypeError('Overflow')
            if rational_number < 0:
                raise TypeError('Underflow')
            self.primary_memory[address] =  rational_number
        except  TypeError:
            raise TypeError('8-bit number')
#Class CPU Virtual
class CPU:
  def __init__(self):
    self.Max_memory = 256
    self.ram = Memory(self.Max_memory)
    self.track_history = []
#instructions: to see LS8_CHEATSHEET
#calculator Programming
    HLT  = 0x01
    RET  = 0x11
    PUSH = 0x45
    POP  = 0x46
    PRN  = 0x47
    CALL = 0x50
    JMP  = 0x54
    JEQ  = 0x55
    JNE  = 0x56
    LDI  = 0x82
    ADD  = 0xA0
    MUL  = 0xA2
    CMP  = 0xA7
    AND  = 0xA8
    OR   = 0xAA
    XOR  = 0xAB
    NOT  = 0x69
    SHL  = 0xAC
    SHR  = 0xAD
    MOD  = 0xA4
    self.execution_table = {
      HLT:  self.HLT,
      PRN:  self.PRN,
      LDI:  self.LDI,
      PUSH: self.PUSH,
      POP:  self.POP,
      MUL:  self.MUL,
      CMP:  self.CMP,
      JMP:  self.JMP,
      JEQ:  self.JEQ,
      JNE:  self.JNE,
      AND:  self.AND,
      OR:   self.OR,
      XOR:  self.XOR,
      NOT:  self.NOT,
      SHL:  self.SHL,
      SHR:  self.SHR,
      MOD:  self.MOD,
      CALL: self.CALL,
      RET:  self.RET,
      ADD:  self.ADD
    }
    self.record = Memory(8) #FULL REGISTERS
    self.record.write_byte(7, 0xF4) 
    self.PC = 0             #SPECIFIC REGISTERS
    self.IR = 0 
    self.FL = 0x00          #FLAG
    self.FL_running = 0b10000000
    self.FL_less    = 0b00000100
    self.FL_grater = 0b00000010
    self.FL_equal   = 0b00000001
#Split
    def get_split(self):   
        return self.record.decode_bytes(7)
    def set_split(self, value):
        self.record.compuse_bytes(7, value)
#Load Data
    def load(self, ls8_file):
        self.ram.clear()
        address = 0
        with open(ls8_file) as f:
            for line in f:
                line = line.split('#')
                data = line[0].strip()
                if data == ' ':
                    continue
                try:
                    data = int(line[0], 2)
                except  ValueError:
                    continue
                self.ram_write(address, data)
                address += 1
    def ram_read(self, conduct):
        return self.ram.decode_byte(address)
    def ram_write(self, address, value):
        self.ram.compose_bytes(address, value)
    def trace(self):
        '''
        Handy function to print out the CPU state. you might want to call this
        from fun() if you need help debugging.
        '''
        print("PC | IN P1 P2 |", end='')
        for i in range(8):
            print('R%X' % i, end = '')
        print(' FL', end=' ')
        print()
        track_info = f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)) 
        for i in range(8):
            track_info += " %02X" % self.record.decode_bytes(i)
        track_info += ' ' + '{0:b}'.format(self.FL)
        self.track_history.append(track_info)
        last_track_5 = self.track_history[-5:]
        for linea in last_track_5:
            print(line, end=' ')
            print()
        print()
#ON CPU
    def run(self):
        """Run the CPU."""
        self.FL | self,FL_running
        while self.FL & self.FL_running == self.FL_running:
            self.IR = self.ram_read(self.PC)      
            quantity_ops = (self.IR & 0b11000000) >> 6 
            use_alu = (self.IR & 0b00100000) >> 5
            group_pc = (self.IR & 0b00010000) >> 4
            add_id = (self.IR & 0b00001111) >> 0
            if use_alu:
                self.alu(self.IR, self.ram_read(self.PC + 1), self.ram_read(sefl.PC + 2))
            else:
                try:
                    self.execution_table[self.IR]()
                except KeyError:
                    print(f'address' %(self.IR, self.PC))
                    self.HLT()
                if not group_pc:
                    self.pc +=(1 + quantity_ops)
    def alu(self, op, track_a, track_b):
            """ALU operations."""
            if op == "ADD":
                self.record[track_a] += self.record[track_b]
            elif op == "SUB": 
                self.record[track_a] -= self.record[track_b]
            elif op == "MUL":
                self.record[track_a] *= self.record[track_b]
            elif op == "AND":
                self.record[track_a] &= self.record[track_b]
            elif op == "CMP":
                if self.record[track_a] == self.record[track_b]:
                    self.fl = 0b00000001
                elif self.record[track_a] > self.record[track_b]:
                    self.fl = 0b00000010
                else:
                    self.fl = 0b00000100
            elif op == "DEC":
                self.record[track_a] -= 1
            elif op == "DIV":
                if self.record[track_b] == 0:
                    print("Error: Cannot divide by zero!")
                    self.halt = True
                else:
                    self.record[track_a] /= self.record[track_b]
            elif op == "INC":
                self.record[track_a] += 1
            elif op == "MOD":
                if self.record[track_b] == 0:
                    print("Error: Cannot divide by zero!")
                    self.halt = True
                else:
                    self.record[track_a] %= self.record[track_b]
            elif op == "NOT":
                self.record[track_a] = ~self.record[track_a] 
            elif op == "OR":
                self.record[track_a] |= self.record[track_b]
            elif op == "SHL":
                self.record[track_a] <<= self.record[track_b]
            elif op == "SHR":
                self.record[track_a] >>= self.record[track_b]
            elif op == "XOR":
                self.record[track_a] ^= self.record[track_b]    
            else:
                raise Exception("Unsupported ALU operation")    
#IMPLEMENTE Stack data is stored in RAM
#Halt the CPU (and exit the emulator). 
    def HLT(self):
        self.FL &= ~self.FL_running
#LDI register immediate, Set the value of a register to an integer. 
    def LDI(self):
        register_number = self.ram_read(self.PC + 1)
        register_value = sefl.ram_read(self.PC + 2)
        self.record.compose(register_number, resiter_value)
#PRN register pseudo-instruction
    def PRN(self):
        register_number = self.ram_read(self.PC + 1)
        register_value = self.record.read_byte(register_number)
        print(register_value)
#Push a value in a register onto the stack, decrement sp
    def Push(self):                                         
        self.set_split(self.get_split()-1)
        register_number = self.ram_read(self.PC + 1)
        data = self.record.decode_bytes(resiter_number)
        self.ram_write(self.get_split(), data)
#Pop a value from the stack into the given register
    def Pop(self):                                          #POP
        register_number = self.ram_read(self.PC +1)
        data = self.ram_read(self.get_split())
        self.record.compose(resiter_number_3, data)
        sefl.set_split(sefl.get_split()+1)
#Jump to the address stored in the given register.
    def JMP(self):
        register_number = self.ram_read(self.PC + 1)
        self.PC = self.record.read_byte(register_number)
#JEQ register, If equal flag is set (true), jump to the address stored in the given register.
    def JEQ(self):
        if self.FL & self.FL_equal == self.FL_equal:
           self.JMP()
        else:
           self.PC += 2
#JNE register, If E flag is clear (false, 0), jump to the address stored in the given register.
    def JNE(self):
        if self.FL & self.FL_equal == 0:
           self.JMP()
        else:
           self.PC += 2
#CALL register
    def Call(self):                                         
        self.ram_write(self.get_split(), self.PC + 2)
        self.set_split(self.get_split()-1)
        register_number = self.ram_read(self.PC + 1)
        self.PC = self.record.read_byte(register_number)
#Return from subroutine. Pop the value from the top of the stack and store it in the PC.
    def RET(self):                                      
        self.set_split(self.get_split()+ 1)
        return_address = self.ram_read(self.get_split())
        self.PC = return_address

#Stored in registers according with the instruction.
#ADD + ->ADDITION
    def ADD(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value + track_b_value
        self.record.compuse_bytes(track_a, track_b)
#MUL ->MULTIPLICATION
    def Mul(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value * track_b_value
        self.record.compuse_bytes(track_a, track_b)
#BITWISE OR
    def CMP(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        if track_a_value == track_b_value:
            self.FL |= self.FL_equal
        else:
            self.FL &= ~self.FL_equal   #BITWISE, NOT
        if track_a_value < track_b_value:
            self.FL |= self.FL_less     #BITWISER OR
        else:
            self.FL &= ~self.FL_less
        if track_a_value > track_b_value:
            self.FL |= self.FL_greater
        else:
            self.FL & ~self.FL_greater
#https://www.tutorialspoint.com/python/bitwise_operators_example.htm
#AND & -> mask to extract those two bits, then add one to the result
    def And(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value & track_b_value
        self.record.compuse_bytes(track_a, result)
#OR | 
#-> Select let's bitwise-OR the shifted value with the result from the previous step. 
# It copies a bit if it exists in either operand.
    def OR(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value | track_b_value
        self.record.compuse_bytes(track_a, result)
#XOR ^ 
# -> is exclusiveor, its resul is true if only one of its inputs is true. 
    def XOR(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value ^ track_b_value
        self.record.compuse_bytes(track_a, result)
#NOT ~ 
# call inverter has a single input and a single output. 
# If that input is 1 (or TRUE), then the output is 0 (FALSE).
    def NOT(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        result = ~track_a_value 
        self.record.compuse_bytes(track_a, result)
#SHL << 
# -> Returns x with the bits shifted to the left by y places 
# (and new bits on the right-hand-side are zeros). This is the same as multiplying x by 2**y.
    def SHL(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value << track_b_value
        self.record.compuse_bytes(track_a, result)
#SHR >>  
# ->Returns x with the bits shifted to the right by y places. 
# This is the same as //'ing x by 2**y.
    def SHR(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value >> track_b_value
        self.record.compuse_bytes(track_a, result)
#https://docs.python.org/3.4/library/operator.html
#MOD % modulo
    def MOD(self, track_a, track_b):
        track_a_value = self.record.read_byte(track_a)
        track_b_value = self.record.read_byte(track_b)
        result = track_a_value % track_b_value
        self.record.compuse_bytes(track_a, result)