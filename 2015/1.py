"""
https://adventofcode.com/2015/day/1
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Pythony implementation for part 1
# We need to iterate through the list twice here though, and since we also need
# to iterate again for part 2 we may as well just combine them all into one
# loop instead.
# Just keeping this here as a note.
#
# up_count = len([up for up in data if up == "("])
# down_count = len([down for down in data if down == ")"])
# print(up_count - down_count)


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
