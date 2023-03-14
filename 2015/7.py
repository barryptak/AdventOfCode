"""
https://adventofcode.com/2015/day/7
"""
import copy
from utils.data import read_data

# NOTE: This could have been done more succinctly with sympy or similar, but I
# like VMs so I thought I'd do it manually.

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


# The circuit/VM instruction set
OPERATIONS = {"AND": lambda r1, r2: r1 & r2,
              "OR":  lambda r1, r2: r1 | r2,
              "LSHIFT": lambda r1, r2: r1 << r2,
              "RSHIFT": lambda r1, r2: r1 >> r2,
              "STR": lambda r1, _: r1,
              "NOT": lambda r1, _: ~r1}


def get_register(regs, reg_name):
    """ Gets the value for this register/wire if its known """
    if reg_name.isalpha() and reg_name not in regs:
        return None
    return int(reg_name) if reg_name.isdigit() else regs[reg_name]


def emulate(instructions, registers):
    """ Emulate the circuit given the list of instructions and registers """

    # We keep spinning round while there are unresolved instructions.
    # In this puzzle each register is written to only once, so execution order
    # doesn't matter as long as we eventually get all values calculated.
    while len(instructions) > 0:
        for i, instruction in enumerate(instructions):
            # Split the instruction into the main instruction and the output
            # register/wire
            in_data, output_wire = instruction.split(" -> ")

            # Split the main instruction into its parts too
            in_data_split = in_data.split()
            param_count = len(in_data_split)

            op_name = None
            reg_1 = None
            reg_2 = None

            # The only 2 param instruction is NOT
            if param_count == 2:
                if (reg_1 := get_register(registers, in_data_split[1])) is not None:
                    op_name = "NOT"
            else:
                # All other (non-NOT) instructions have an input (lhs) register
                # as the first param. Check to see if this one is a literal or
                # has a known value yet.
                if (reg_1 := get_register(registers, in_data_split[0])) is not None:
                    # The only 1 param instruction is a store/write value
                    if param_count == 1:
                        op_name = "STR"
                    # Otherwise this is a standard r1 OP r2 instruction. Read
                    # in the second register or literal to use.
                    elif (reg_2 := get_register(registers, in_data_split[2])) is not None:
                        op_name = in_data_split[1]

            # If we have all of the information needed to execute this
            # instruction then do so.
            if op_name:
                registers[output_wire] = OPERATIONS[op_name](reg_1, reg_2)
                # Blank out this instruction so that we can remove it from the
                # list and not execute it again
                instructions[i] = ""

        # We've executed all of the instructions that we had sufficient data
        # for. Now trim down the list to only include the remaining
        # instructions so that we can try them again with the new register
        # values that we have.
        instructions = [instruction for instruction in instructions if instruction != ""]


# Part 1
# Determine the final value for register a
registers_1 = {}
instructions_1 = copy.copy(data)
emulate(instructions_1, registers_1)
print(registers_1["a"])


# Part 2
# Force the previous final value a onto b and determine the new value for a
registers_2 = {"b": registers_1["a"]}
# Remove the instruction that set b's value previously so that we don't
# overwrite our new value for it
instructions_2 = [instruction for instruction in data if not instruction.endswith(" -> b")]
emulate(instructions_2, registers_2)
print(registers_2["a"])
