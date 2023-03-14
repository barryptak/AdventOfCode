"""
https://adventofcode.com/2015/day/12
"""
import json
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Part 1
# Sum all numbers in the json input
print(sum(extract_ints(data)))

# Part 2
# Sum all numbers in the json input that are NOT part of an object with a
# property of value "red"s

def sum_nums(obj):
    """
    Recursive function that returns the sum of the integer value in this
    element UNLESS this is an object that contains the value "red" in which
    we return 0 for this entire object and its children
    """

    # If this object is a list then simply sum the values of all items
    if isinstance(obj, list):
        return sum((sum_nums(o) for o in obj))
    # If this object is a dic then we must check for "red" values and return 0
    # if we find any. If not then simply sum the values of the dict values.
    elif isinstance(obj, dict):
        if any((v == "red" for v in obj.values())):
            return 0
        else:
            return sum((sum_nums(v) for v in obj.values()))
    # If this object is an int then simply return its value
    elif isinstance(obj, int):
        return obj
    # This is not a list, dict or int so it has no value assigned
    else:
        return 0

print(sum_nums(json.loads(data)))
