"""
https://adventofcode.com/2022/day/1
"""
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Get the data as ints grouped per elf
# e.g. 
# 1000
# 2000
# 3000
#
# 4000
# Becomes [[1000,2000,3000],[4000]]
elf_payloads = [[int(line) for line in str_data.split("\n")] for str_data in data.split("\n\n")]

# Part 1
# Get the highest of the totals for each elf
highest = max(sum(payload) for payload in elf_payloads)
print(highest)

#Part 2
# Get the totals for all elves, sort them and pull out the top three
elf_totals = [sum(payload) for payload in elf_payloads]
elf_totals = sorted(elf_totals, reverse=True)
three_highest = sum(elf_totals[:3])
print(three_highest)
