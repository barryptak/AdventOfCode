"""
https://adventofcode.com/2015/day/6
"""
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Rather than requiring a load of if/else statements to apply the correct
# operation to each light we can store a function pointer / lambda in a dict
# and look it up instead. This is neater and involves less branching.
OPERATIONS_1 = {"turn on": lambda x: True,
              "turn of": lambda x: False,
              "toggle ": lambda x: not x}

OPERATIONS_2 = {"turn on": lambda x: x + 1,
              "turn of": lambda x: x - 1 if x > 0 else 0,
              "toggle ": lambda x: x + 2}

lights_1 = [[False] * 1000 for _ in range(1000)]
lights_2 = [[False] * 1000 for _ in range(1000)]

# Iterate over each input line and determine the operation to apply (turn on,
# turn off, or toggle) and the rectangle of lights to apply the operation to.
for line in data:
    operation_key = line[:7]
    operation_1 = OPERATIONS_1[operation_key]
    operation_2 = OPERATIONS_2[operation_key]
    start_x, start_y, end_x, end_y = extract_ints(line)

    # Apply the operations over the range of lights indicated
    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            lights_1[y][x] = operation_1(lights_1[y][x])
            lights_2[y][x] = operation_2(lights_2[y][x])


# Part 1
# How many lights are lit?
lit_count = sum((len([col for col in row if col]) for row in lights_1))
print(lit_count)


# Part 2
# What's the total brightness?
brightness = sum((sum(row) for row in lights_2))
print(brightness)
