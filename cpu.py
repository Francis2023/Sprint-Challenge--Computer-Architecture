"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
AND = 0b10101000
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.pc = 0
        self.halted = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        with open(filename) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '': # ignore blanks
                    continue
                val = int(num, 2)
                self.ram_write(val, address)
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction_to_execute, operand_a,operand_b)
    
    def execute_instruction(self, instruction_to_execute, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif instruction == MULT:
            self.reg[operand_a] += self.reg[operand_b]
            self.pc += 3
        elif instruction == PUSH:
            self.reg[SP] -= 1 # decrement the stack pointer
            valueFromRegister = self.reg[operand_a] # write the value stored in register onto the stack
            self.ram_write(valueFromRegister, self.reg[SP])
            self.pc += 2
        elif instruction == POP:
            topmostValue = self.ram_read(self.reg[SP]) # Save the value on top the stack onto the register given
            self.reg[operand_a] = topmostValue
            self.reg[SP] += 1 # increment the stack pointer
            self.pc += 2
        elif instruction == CALL:
            self.reg[SP] -= 1
            address = self.pc + 2
            self.ram_write(address ,self.reg[SP])
            regToGetAddressFrom = self.ram_read(self.reg[SP])
            regToJumpTo = self.reg[operand_a]
            pc = regToJumpTo
        elif instruction == RET:
            regToReturnTo = self.ram_read(self.reg[SP])
            self.ram_write(1, self.reg[SP])
            pc = regToReturnTo
        elif instruction == CMP:
            if self.reg[operand_a] == self.reg[operand_b]:
                E = 1
            elif self.reg[operand_a] < self.reg[operand_b]:
                L = 1
            else:
                G = 1
        elif instruction == JMP:
            jumpTo = self.reg[SP]
            PC = jumpTo
        elif instruction == JEQ:
            if E:
                PC = self.reg[operand_a]
        elif instruction == JNE:
            if not E:
                PC = self.reg[operand_a]

        else:
            print("Idk this instruction. Exiting")
            sys.exit(1)