"""
https://adventofcode.com/2016/day/6
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Transpose the data so that we have a list per column
column_chars = [list(col) for col in zip(*data)]

# Part 1
# What's the message when we look at the most frequent character in each column?
message = [max(col, key=col.count) for col in column_chars]
print("".join(message))

# Part 2
# What's the message when we look at the least frequent character in each column?
message = [min(col, key=col.count) for col in column_chars]
print("".join(message))
