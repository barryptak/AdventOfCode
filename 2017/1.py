"""
https://adventofcode.com/2017/day/1
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Part 1
# What's the sum of the numbers which match the next digit?
# The list is circular so we need to special case the last character.
total = sum(int(i) for i, j in zip(data, data[1:]) if i == j)
total += int(data[0]) if data[0] == data[-1] else 0
print(total)

# Part 2
# What's the sum of the numbers which match the number halfway around the
# circular list?
# By processing the first half of the list we will have covered the second half
# too. We just have to increment the sum by *2 the value.
total = sum(int(i)*2 for i, j in zip(data, data[len(data)//2:]) if i == j)
print(total)
