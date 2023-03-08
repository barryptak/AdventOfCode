"""
https://adventofcode.com/2016/day/12
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def parse_instructions(data_in):
    """
    Parse the input data into a set of instructions and perform some basic
    optimisation on them.
    """

    # First iterate over the instructions and do some minor fixup:
    # Change cpy instructions where the value to cpy is a literal to be an
    # explicit stl (store literal) instruction as we can then execute each
    # instruction faster by not having to check if we're dealing with a
    # register or a literal at execution time.
    # We also check for any jnz instructions that are comparing against a
    # literal as we can then determine if these will always jump or never jump.
    instructions = [line.split() for line in data_in]
    for i, instruction in enumerate(instructions):
        operation = instruction[0]
        # Get a list of the arguments with any literal values as ints rather
        # than strings
        args = list(map(lambda value: value if value in "abcd" else int(value), instruction[1:]))

        # Change any cpy of literals to an explicit store literal instruction
        if operation == "cpy" and isinstance(args[0], int):
            operation = "stl"  # store literal
        # Change any jnz against a literal to be an explicit jmp or nop
        elif operation == "jnz" and isinstance(args[0], int):
            if args[0] != 0:
                operation = "jmp"
                args[0] = args[1]
            else:
                operation = "nop"

        instructions[i] = (operation, *args)

    # Optimise instructions
    # We're looking for a pattern like this:
    #
    # inc reg_2
    # dec reg_1
    # jnz reg_1 -2
    #
    # The real operation here is to increment reg_2 by the value in reg_1 and then carry on
    # We can reduce this loop of reg_1 * 3 instructions to a single new instruction add reg_1 reg_2
    for i, instruction in enumerate(instructions[:-4]):
        if (instruction[0] == "inc" and
            instructions[i+1][0] == "dec" and
            instructions[i+2][0] == "jnz" and
            instructions[i+1][1] == instructions[i+2][1] and
            instructions[i+2][2] == -2):
            operation = "add"
            args = [instructions[i+1][1] , instruction[1]]
            instructions[i] = (operation, *args)
            instructions[i+1] = ("nop", 0)
            instructions[i+2] = ("nop", 0)


    # The above two stages can have added nops into the instruction list.
    # Rather than step over them all the time we can remove the nops entirely,
    # but we also need to adjust any jumps to account for the removed nops so
    # that we don't jump too far now.
    for i, instruction in enumerate(instructions):
        # Is this instruction a jump?
        is_jnz = instruction[0] == "jnz"
        if is_jnz or instruction[0] == "jmp":
            # From the current instruction step in the direction of the jump
            # and for every nop that we encounter within the jump we need to
            # reduce the magnitude of the jump by one (as we will be removing)
            # the nop.
            jump_count = instruction[2] if is_jnz else instruction[1]
            step = 1 if jump_count >= 0 else -1
            for index in range(i, i + jump_count, step):
                if instructions[index][0] == "nop":
                    jump_count -= step
            if is_jnz:
                instructions[i] = ("jnz", instruction[1], jump_count)
            else:
                instructions[i] = ("jmp", jump_count)

    # Get the instructions with all of the nops removed
    instructions = [i for i in instructions if i[0] != "nop"]

    return instructions


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
            registers[args[1]] = registers[args[0]]
        elif operation == "stl":
            registers[args[1]] = args[0]
        elif operation == "inc":
            registers[args[0]] += 1
        elif operation == "dec":
            registers[args[0]] -= 1
        elif operation == "add":
            registers[args[1]] += registers[args[0]]
        elif operation == "jnz":
            pc_step = args[1] if registers[args[0]] != 0 else 1
        elif operation == "jmp":
            pc_step = args[0]

        # Update the program counter. If the executed instruction was a jump
        # then the pc_step value will contain the correct offset for us to use.
        program_counter += pc_step

    return registers


instruction_list = parse_instructions(data)

# Part 1
# What value is in register b after running the program?
part1_registers = run_program(instruction_list, {"a": 0, "b": 0, "c": 0, "d": 0})
print(part1_registers["a"])

# Part 2
# What about when we start with different reg values?
part2_registers = run_program(instruction_list, {"a": 0, "b": 0, "c": 1, "d": 0})
print(part2_registers["a"])
