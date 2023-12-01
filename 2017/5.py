"""
https://adventofcode.com/2017/day/5
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def execute_jumps(jump_data, part2=False):
    """
    Execute the jump instructions until we jump outside of the jump table.
    When this happens return the number of steps executed so far.
    """
    jumps = list(map(int, jump_data))
    instruction_pointer = 0
    steps = 0
    while instruction_pointer >= 0 and instruction_pointer < len(jumps):
        jump_amount = jumps[instruction_pointer]
        if part2 and jump_amount >= 3:
            jumps[instruction_pointer] -= 1
        else:
            jumps[instruction_pointer] += 1
        instruction_pointer += jump_amount
        steps += 1

    return steps

print(execute_jumps(data))
print(execute_jumps(data, True))
