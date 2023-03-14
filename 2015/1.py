"""
https://adventofcode.com/2015/day/1
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Parts 1 & 2
# Find the final floor that we end up on
# Find out how many moves it takes to get to floor -1 for the first time

FLOOR_DIR = {"(": 1, ")": -1}
current_floor = 0
reach_floor_minus_one = 0
for i, char in enumerate(data):
    current_floor += FLOOR_DIR[char]
    if not reach_floor_minus_one and current_floor == -1:
        reach_floor_minus_one = i + 1

print(current_floor)
print(reach_floor_minus_one)
