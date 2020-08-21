"""CPU functionality."""

import sys

class Memory():
  """Main CPU class."""
  def __init__(self, size):
    """Construct a New CPU"""
    self.size = size
    self.clear()
  def clear(self):
        self.primary_memory = [0] * self.size
  def decode_byte(self, address):               #read the bytes  
    if address < 0 or address > self.size - 1:
      raise ReferenceError("Memory Performance")
    return self.primary_memory[address]
  def compose_byte(self, address, data):        #write the bytes
    if address < 0 or address > self.size - 1:
      raise ReferenceError("Memory Performance")
    try:
      true_byte = int(data)
      if true_byte > 0xFF:
        raise TypeError("Overflow")
      if true_byte < 0:
        raise TypeError("Underflow")
      self.primary_memory[address] = true_byte
    except TypeError:
      raise TypeError("8-bit number")
#Virtual CPU
class CPU:
  def __init__(self):
    self.max_memory = 256
    self.ram = Memory(self.max_memory)
    self.track_history = []
#Table instructions
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
    self.execute_table = {
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
    self.record = Memory(8)            #Full Registers
    self.record.compose_byte(7, 0xF4) 
    self.PC = 0                        #Specific Registers
    self.IR = 0  
# flags 
    self.FL = 0x00
    self.FL_running = 0b10000000
    self.FL_less    = 0b00000100
    self.FL_greater = 0b00000010
    self.FL_equal   = 0b00000001

  def get_split(self):
    return self.record.decode_byte(7)
  def group_split(self, value):
    self.record.compose_byte(7, value)
  def load(self, program):
    self.ram.clear()
    address = 0
    with open(program) as f:
      for line in f:
        line = line.split("#")
        try:
          data = int(line[0], 2)
        except ValueError:
          continue
        self.ram_compose(address, data)
        address += 1
  def ram_decode(self, address):
    return self.ram.decode_byte(address)
  def ram_compose(self, address, value):
    self.ram.compose_byte(address, value)
  def trace(self):
    '''
    Handy function to print out the CPU state. you might want to call this
    from fun() if you need help debugging.
    '''
    print("PC | IN P1 P2 |", end='')
    for i in range(8):
      print(" R%X" % i, end='')
    print(" | FL", end='')
    print()
    trace_info = f"%02X | %02X %02X %02X |" % (
      self.PC,
      #self.fl,
      #self.ie,
      self.ram_decode(self.PC),
      self.ram_decode(self.PC + 1),
      self.ram_decode(self.PC + 2))
    for i in range(8):    #Fallowing the move
      track_inf += " %02X" % self.record.decode_byte(i)
    track_inf += " | " + "{0:b}".format(self.FL)
    self.track_history.append(track_inf)
    last_track = self.track_history[-5:]
    for line in last_track:
      print(line, end='')
      print()
    print()
#CPU ON
  def run(self):
    """Run the CPU"""
    self.FL |= self.FL_running  
    while self.FL & self.FL_running == self.FL_running: 
      self.IR = self.ram_decode(self.PC) 
# decode 
      number_ops = (self.IR & 0b11000000) >> 6
      use_alu = (self.IR & 0b00100000) >> 5
      group_pc = (self.IR & 0b00010000) >> 4
      add_id = (self.IR & 0b00001111) >> 0
      if use_alu:
        self.alu(self.IR, self.ram_decode(self.PC + 1), self.ram_decode(self.PC + 2))
      else:
        try:
          self.execute_table[self.IR]()  
        except KeyError:
          print(f"out instruction 0x%02X at address 0x%02X" % (self.IR, self.PC))
          self.HLT()
      if not group_pc:
        self.PC += (1 + number_ops)
  def alu(self, op, track_a, track_b):   #ALU
        try:
          self.execute_table[self.IR](track_a, track_b) # execute
        except KeyError:
          print(f"out ALU instruction 0x%02X at address 0x02X" % (self.IR, self.PC))
          self.HLT()
#IMPLEMENTE Stack data is stored in RAM
#Halt the CPU (and exit the emulator). sp
  def HLT(self):
    self.FL &= ~self.FL_running
#LDI register immediate, Set the value of a register to an integer. 
  def LDI(self):
    register_number = self.ram_decode(self.PC + 1)
    register_value = self.ram_decode(self.PC + 2)
    self.record.compose_byte(register_number, register_value)
#PRN register pseudo-instruction
  def PRN(self):
    register_number = self.ram_decode(self.PC + 1)
    register_value = self.record.decode_byte(register_number)
    print(register_value)
#Push a value in a register onto the stack, decrement sp
  def PUSH(self):
    self.group_split(self.get_split() - 1)
    register_number = self.ram_decode(self.PC + 1)
    data = self.record.decode_byte(register_number)
    self.ram_compose(self.get_split(), data)
#Pop a value from the stack into the given register
  def POP(self):
    register_number = self.ram_decode(self.PC + 1)
    data = self.ram_decode(self.get_split())
    self.record.compose_byte(register_number, data)
    self.group_split(self.get_split() + 1)
#JPM
# Jump to the address stored in the given register.
  def JMP(self):
    register_number = self.ram_decode(self.PC + 1)
    self.PC = self.record.decode_byte(register_number)
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
#CALL registe
  def CALL(self):
    # The address of the ***instruction*** _directly after_ `CALL` is pushed onto the stack.
    self.ram_compose(self.get_split(), self.PC + 2)
    self.group_split(self.get_split() - 1)
    # The PC is set to the address stored in the given register.
    register_number = self.ram_decode(self.PC + 1)
    self.PC = self.record.decode_byte(register_number)
#Return from subroutine. Pop the value from the top of the stack and store it in the PC.
  def RET(self):
    # Pop the value from the top of the stack and store it in the `PC`.
    self.group_split(self.get_split() + 1)
    return_adress = self.ram_decode(self.get_split())
    self.PC = return_adress
#Stored in registers according with the instruction.
#ADD + ->ADDITIONs
  def ADD(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value + track_b_value
    self.record.compose_byte(track_a, result)
#MUL ->MULTIPLICATION
  def MUL(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value * track_b_value
    self.record.compose_byte(track_a, result)
#BITWISE OR
  def CMP(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    if track_a_value == track_b_value:
      self.FL |= self.FL_equal   #Bitwiser, not FL = ON
    else:
      self.FL &= ~self.FL_equal  #Bitwiser or FL = OFF
    if track_a_value < track_b_value:
      self.FL |= self.FL_less
    else:
      self.FL &= ~self.FL_less
    if track_a_value > track_b_value:
      self.FL |= self.FL_greater
    else:
      self.FL &= ~self.FL_greater
#https://www.tutorialspoint.com/python/bitwise_operators_example.htm
#AND & -> mask to extract those two bits, then add one to the result
  def AND(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value & track_b_value
    self.record.compose_byte(reg_a, result)
#OR | 
#-> Select let's bitwise-OR the shifted value with the result from the previous step. 
# It copies a bit if it exists in either operand.
  def OR(self, reg_a, reg_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value | track_b_value
    self.record.compose_byte(track_a, result)
#XOR ^ 
# -> is exclusiveor, its resul is true if only one of its inputs is true. 
  def XOR(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value ^ track_b_value
    self.record.compose_byte(track_a, result)
#NOT ~ 
# call inverter has a single input and a single output. 
# If that input is 1 (or TRUE), then the output is 0 (FALSE).
  def NOT(self, track_a, _):
    track_a_value = self.record.decode_byte(track_a)
    result = ~track_a_value
    self.record.compose_byte(track_a, result)
#SHL << 
# -> Returns x with the bits shifted to the left by y places 
# (and new bits on the right-hand-side are zeros). This is the same as multiplying x by 2**y.
  def SHL(self, reg_a, reg_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value << track_b_value
    self.record.compose_byte(track_a, result)
#SHR >>  
# ->Returns x with the bits shifted to the right by y places. 
# This is the same as //'ing x by 2**y
  def SHR(self, reg_a, reg_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value >> track_b_value
    self.record.compose_byte(track_a, result)
#https://docs.python.org/3.4/library/operator.html
#MOD % modulo
  def MOD(self, track_a, track_b):
    track_a_value = self.record.decode_byte(track_a)
    track_b_value = self.record.decode_byte(track_b)
    result = track_a_value % track_b_value
    self.record.compose_byte(track_a, result)
