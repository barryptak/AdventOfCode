"""
https://adventofcode.com/2022/day/6
"""
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def all_chars_unique(s):
    """
    Create a set of all characters in the input string and check that the length of the set and the string match.
    If they don't then we have repeated characters in the input string.
    """
    return len({c for c in s}) == len(s)

def find_end_of_marker(data, marker_length):
    """
    Iterate over the data set looking for a set of marker_length non-repeating characters.
    When we find them return the index of the next character following the marker.
    """
    for start in range(0, len(data) - marker_length):
        end = start + marker_length - 1
        # Do a quick and dirty check to see if the latest character is repeated or not
        if data[end] not in data[start:end]:
            # If the last character isn't repeated then check the entire length of the marker string
            if all_chars_unique(data[start:end + 1]):
                return end + 1

print(find_end_of_marker(data, 4))
print(find_end_of_marker(data, 14))

