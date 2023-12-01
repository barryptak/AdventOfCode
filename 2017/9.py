"""
https://adventofcode.com/2017/day/9
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

skip = False
group_depth = 0
in_garbage = False
score = 0
garbage_chars = 0

for char in data:
    if skip:
        skip = False
    elif char == "!":
        skip = True
    elif in_garbage:
        if char == ">":
            in_garbage = False
        else:
            garbage_chars += 1
    elif char == "<":
        in_garbage = True
    elif char == "{":
        group_depth += 1
        score += group_depth
    elif char == "}":
        group_depth -= 1

print(score)
print(garbage_chars)

