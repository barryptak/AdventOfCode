"""
https://adventofcode.com/2022/day/25
"""

from functools import reduce
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

VALUES = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
NUMERALS = ("0", "1", "2", "=", "-")


def snafu_to_int(snafu):
    """ Converts the input string in SNAFU format into an int """
    total = 0
    for char in snafu:
        total = (total * 5) + VALUES[char]
    return total


def int_to_snafu(num):
    """ Converts an int into a SNAFU format string """
    snafu_string = []
    while num > 0:
        num, val = divmod(num, 5)
        if val > 2:
            num += 1
        snafu_string.append(NUMERALS[val])
    return "".join(snafu_string[::-1])


# Part 1
# Sum up all of the input numbers that are in SNAFU format then print out the
# result in SNAFU format too
snafu_sum = reduce(lambda a, b: a + b, map(snafu_to_int, data))
print(int_to_snafu(snafu_sum))
