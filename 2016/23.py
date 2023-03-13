"""
https://adventofcode.com/2016/day/23
"""
import copy
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def parse_instructions(data_in):
    """ Parse the input data into a set of instructions. """

    instructions = [line.split() for line in data_in]
    for i, instruction in enumerate(instructions):
        operation = instruction[0]
        # Get a list of the arguments with any literal values as ints rather
        # than strings
        args = list(map(lambda value: value if value in "abcd" else int(value), instruction[1:]))
        instructions[i] = [operation, *args]

    return instructions


def get_value(registers, arg):
    """
    Gets the value from the current arg. It's either a literal that gets
    returned as is, or it's a register name so we return the value in that
    register.
    """
    return arg if isinstance(arg, int) else registers[arg]


def execute_cpy(instructions, registers, program_counter):
    """
    Execute the copy operation at the program_counter.
    We look for a certain pattern of operations after the cpy and perform an
    optimised execution instead of running all instructions one at a time.
    If the pattern is not present then we just execute the cpy normally.
    """

    instruction = instructions[program_counter]
    args = instruction[1:]

    # Check if this is a valid cpy instruction or if it's got bad register
    # values as the result of a tgl operation
    if not isinstance(args[1], str):
        return 1

    # We're looking for a pattern where we have a pair of loops (one nested in
    # the other) where we increment one register while decrementing another in
    # the inner loop (essentially adding the value in reg 2 to reg 1) while the
    # outer loop also decrements a further register. All together this is the
    # same as performing reg1 += reg2 * reg3.
    # So let's find that pattern and perform this operation in one step
    # rather than looping a potentially crazy number of times.
    if (instructions[program_counter + 1][0] == "inc" and # inc reg1
        instructions[program_counter + 2][0] == "dec" and
        instructions[program_counter + 2][1] == args[1] and # dec reg2
        instructions[program_counter + 3][0] == "jnz" and
        instructions[program_counter + 3][1] == args[1] and # loop around while reg2 > 0
        instructions[program_counter + 3][2] == -2 and
        instructions[program_counter + 4][0] == "dec" and # dec reg 3
        instructions[program_counter + 5][0] == "jnz" and # loop around while reg3 > 0
        instructions[program_counter + 5][1] == instructions[program_counter + 4][1] and
        instructions[program_counter + 5][2] == -5):

        # Perform the actual multiplication and add
        value_to_add = get_value(registers, instructions[program_counter + 5][1])
        value_to_add *= get_value(registers, args[0])
        registers[instructions[program_counter + 1][1]] += value_to_add

        # Reset regs 2 + 3 to 0 as they would have been after the normal set of
        # operations in case their values are relied on
        registers[args[1]] = 0
        registers[instructions[program_counter + 5][1]] = 0

        # Return the number of instructions to skip ahead
        return 6

    # This is not an optimisation opportunity - just run the normal cpy.
    registers[args[1]] = get_value(registers, args[0])
    return 1


def run_program(instructions, registers):
    """ Run the puzzle program starting with the supplied register values """

    # Keep going until the program counter ends up on an instruction that
    # doesn't exist. Then we finish execution and exit.
    program_counter = 0
    num_instructions = len(instructions)
    while 0 <= program_counter < num_instructions:
        # Pull out the current instruction and the register from the program
        instruction = instructions[program_counter]
        operation = instruction[0]
        args = instruction[1:]
        pc_step = 1

        # Execute the instruction
        if operation == "cpy":
            if isinstance(args[1], str):
                pc_step = execute_cpy(instructions, registers, program_counter)
        elif operation == "inc":
            if isinstance(args[0], str):
                registers[args[0]] += 1
        elif operation == "dec":
            if isinstance(args[0], str):
                registers[args[0]] -= 1
        elif operation == "jnz":
            pc_step = get_value(registers, args[1]) if get_value(registers, args[0]) != 0 else 1
        elif operation == "jmp":
            pc_step = get_value(registers, args[0])
        elif operation == "tgl":
            # Check that the location of the instruction we want to toggle is
            # actually valid
            other_instruction_pointer = program_counter + get_value(registers, args[0])
            if 0 <= other_instruction_pointer < len(instructions):
                other_instruction = instructions[other_instruction_pointer]
                other_operation = other_instruction[0]
                other_args = other_instruction[1:]
                # Change single argument instructions to inc unless they were
                # already inc in which case change it to a dec
                if len(other_args) == 1:
                    if other_operation == "inc":
                        other_instruction[0] = "dec"
                    else:
                        other_instruction[0] = "inc"
                # Change instructions taking 2 arguments to jnz unless they
                # were already jnz in which case change it to a cpy
                else:
                    if other_operation == "jnz":
                        other_instruction[0] = "cpy"
                    else:
                        other_instruction[0] = "jnz"

        # Update the program counter. If the executed instruction was a jump
        # then the pc_step value will contain the correct offset for us to use.
        program_counter += pc_step

    return registers


instruction_list = parse_instructions(data)

# Part 1
# What value is in register a after running the program?
part1_registers = run_program(copy.deepcopy(instruction_list), {"a": 7, "b": 0, "c": 0, "d": 0})
print(part1_registers["a"])

# Part 2
# What value is in register a after starting with 12?
part2_registers = run_program(copy.deepcopy(instruction_list), {"a": 12, "b": 0, "c": 0, "d": 0})
print(part2_registers["a"])
