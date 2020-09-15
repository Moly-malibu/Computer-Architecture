"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8 #ram memory R0-R7
        self.ram = [0] * 256  #initialize memory
        self.pc = 0 #Program counter, executing instruction.
        self.ir = 0

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

    def ram_read(self, loc):
        """Read a location in memory."""
        return self.ram[loc]

    def ram_write(self, loc, value):
        """Write a value to a location in memory."""
        self.ram[loc] = value
        return None

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
        self.load()
        running = True
        while self.running:
            self.ir = self.ram[self.pc]
            if self.ir == 100:
                reg_loc = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.registers[reg_loc] = value
                self.pc += 3
            elif self.ir == 80:
                reg_loc = self.ram[self.pc + 1]
                print(self.registers[reg_loc])
                self.pc += 2
            elif self.ir == 1:
                running = False
            
        return Nones