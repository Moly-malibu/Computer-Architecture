"""CPU functionality."""

import sys
import datetime import datetime
from msvcrt import kbhit, getch

#Instructions
LDI = 0b10000010 
PRN = 0b01000111    # Print
HLT = 0b00000001    # Halt
MUL = 0b10100010    # Multiply
ADD = 0b10100000    # Addition
PUSH = 0b01000101   # Push in stack
POP = 0b01000110    # Pop from stack
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8 #ram memory R0-R7
        self.ram = [0] * 256  #initialize memory
        self.pc = 0 #Program counter, executing instruction.
        self.ir = 0
        self.running = True
        self.halt = False
        self.pc_override = False
        self.interrupt = True

        # Initialize alu_table
        self.alu_table = {}
        self.alu_table[0b10100010] = "MUL"
        self.alu_table[0b10100000] = "ADD"
        self.alu_table[0b10101000] = "AND"
        self.alu_table[0b10100111] = "CMP"
        self.alu_table[0b01100110] = "DEC"
        self.alu_table[0b10100011] = "DIV"
        self.alu_table[0b01100101] = "INC"
        self.alu_table[0b10100100] = "MOD"
        self.alu_table[0b01101001] = "NOT"
        self.alu_table[0b10101010] = "OR"
        self.alu_table[0b10101100] = "SHL"
        self.alu_table[0b10101101] = "SHR"
        self.alu_table[0b10100001] = "SUB"
        self.alu_table[0b10101011] = "XOR"

        # Initialize Interupt Table
        self.interrupt_table = {}
        self.interrupt_table[0b00000001] = 0xF8
        self.interrupt_table[0b00000010] = 0xF9

    def load(self):
        """Load a program into memory."""
    program = sys.argv[1]
    try:
        address = 0
        with open(program) as f:
            for line in f:
                t = line.split('#')[0]
                n = t[0].strip()
                if n == '':
                    continue
            try:
                n = int(n,2)
                self.ram[address] = n
            except ValueError:
                print(f"Invalid Number'{n}'")
                sys.exit(1)
            memory[address] = n
            address += 1
    except FileNotFoundError:
        print(f'{sys.argv[0]}:{sys.argv[1]} File not found: {sys.argv[1]}')
        sys.exit()

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
            
    def ram_read(self, address):
        """Read a location in memory."""
        return self.ram[address]

    def ram_write(self, address, value):
        """Write a value to a location in memory."""
        self.ram[address] = value
        return None
    def hlt(self):
        self.running = False
        self.pc+=1
    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc+=3
    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc+=2
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):   #Load instructions file
        """Run the CPU."""
        self.load()
        running = True
        while self.running:
            self.ir = self.ram[self.pc]
            reg_a = self.ram[self.pc+1]
            reg_b = self.ram[self.pc+2]
            if self.ir == HLT:
                self.hlt()
            elif ir == LDI:
                self.ldi(reg_a, reg_b)
            elif ir == PRN:
                self.prn(reg_a)
            elif ir == MUL:
                self.alu("MUl", reg_a, reg_b)
                self.pc+=3
            elif ir == PUSH:
                self.reg[7] -= 1 #decrement stack pointer
                value = self.reg[reg_a]
                stack_pointer = self.reg[7]
                self.ram[stack_pointer] = value
                self.pc+=2
            elif ir == POP:
                stack_pointer = self.reg[7]
                value = self.ram[stack_pointer]
                self.reg[reg_a] = value
                self.reg[7] +=1
                self.pc+=2
            elif ir == CALL:
                address = self.reg[reg_a]
                address_return = self.pc+2
                self.reg[7]
                self.ram[stack_pointer] = address_return
                self.pc = address
            elif ir == RET:
                stack_pointer = self.reg[7]
                address_return = self.ram[stack_pointer]
                self.reg[7] += 1
                self.pc = address_return
            else:
                print(f'Direction number{self.pc} not recognizing')
                self.pc += 1

