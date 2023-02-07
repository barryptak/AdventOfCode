"""
https://adventofcode.com/2015/day/23
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
instructions = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def run_program(registers):
    """ Run the puzzle program starting with the supplied register values """

    # Keep going until the program counter ends up on an instruction that
    # doesn't exist. Then we finish execution and exit.
    pc = 0
    while 0 <= pc < len(instructions):
        # Pull out the current instruction and the register from the program
        parts = instructions[pc].split()
        instruction = parts[0]
        reg = parts[1][0]
        pc_step = int(parts[-1]) if instruction[0] == "j" else 1

        # Execute the instruction
        if instruction == "hlf":
            registers[reg] //= 2
        elif instruction == "tpl":
            registers[reg] *= 3
        elif instruction == "inc":
            registers[reg] += 1
        elif instruction == "jie":
            pc_step = pc_step if registers[reg] % 2 == 0 else 1
        elif instruction == "jio":
            pc_step = pc_step if registers[reg] == 1 else 1

        # Update the program counter. If the executed instruction was a jump
        # then the pc_step value will contain the correct offset for us to use.
        pc += pc_step

    return registers


# Part 1
# What value is in register b after running the program?
regs = run_program({"a": 0, "b": 0})
print(regs["b"])


# Part 2
# What value is in register b if we start with a equal to 1 instead?
regs = run_program({"a": 1, "b": 0})
print(regs["b"])
