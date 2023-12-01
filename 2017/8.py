"""
https://adventofcode.com/2017/day/8
"""
from collections import defaultdict
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Iterate over each input instruction and use eval to run the condition without
# requiring lots of custom parsing and handling.
# If the condition is met then we can simply check if it's an inc or dec
# operation and add the appropriate number.
registers = defaultdict(int)
max_value = 0
for line in data:
    dst_reg, op, val, _, if_reg, if_op, if_val = line.split()

    if eval(f"registers['{if_reg}'] {if_op} {if_val}"):
        registers[dst_reg] += int(val) if op == "inc" else -int(val)
        max_value = max(max_value, registers[dst_reg])

print(max(registers.values()))
print(max_value)
