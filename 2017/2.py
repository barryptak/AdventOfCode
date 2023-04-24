"""
https://adventofcode.com/2017/day/2
"""
from itertools import combinations
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Parts 1 & 2
# Calculate the checksum (the sum of the max - min value on each row) and the
# division sum (the sum of even divisions on each row) for the spreadsheet.

checksum = 0
division_sum = 0
for row in data:
    ints = extract_ints(row)
    checksum += max(ints) - min(ints)

    # Iterate over each combination of 2 values from the list and check if
    # either number divides evenly by the other.
    for num1, num2 in combinations(ints, 2):
        if num1 % num2 == 0:
            division_sum += num1 // num2
            break
        elif num2 % num1 == 0:
            division_sum += num2 // num1
            break

print(checksum)
print(division_sum)
