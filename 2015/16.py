"""
https://adventofcode.com/2015/day/16
"""
import re
from collections import defaultdict
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# region Lookup Tables

# Output from the scan results from the MFCSAM
MFCSAM_RESULTS = {"children": 3,
                    "cats": 7,
                    "samoyeds": 2,
                    "pomeranians": 3,
                    "akitas": 0,
                    "vizslas": 0,
                    "goldfish": 5,
                    "trees": 3,
                    "cars": 2,
                    "perfumes": 1}

# For part 1 we simply compare each Sue's attributes against the search results
# using the equality operator
OPERATIONS_1 = defaultdict(lambda: lambda a, b: a == b)

# For part 2 we have different operations per attribute
OPERATIONS_2 = {"children": lambda a, b: a == b,
                "cats": lambda a, b: a > b,
                "samoyeds": lambda a, b: a == b,
                "pomeranians": lambda a, b: a < b,
                "akitas": lambda a, b: a == b,
                "vizslas": lambda a, b: a == b,
                "goldfish": lambda a, b: a < b,
                "trees": lambda a, b: a > b,
                "cars": lambda a, b: a == b,
                "perfumes": lambda a, b: a == b}

# endregion Lookup Tables

def parse_sues(data_in):
    """ Parses the list of sues and their attributes from the input data """
    sues = []
    for line in data_in:
        # Match all strings and numbers
        # Our output list will look something like:
        # ["Sue", "<sue_number>", "<attribute_1>", "<attribute_1_count>", ...]
        # e.g.
        # "Sue 7: cars: 6, vizslas: 5, cats: 3" gives us:
        # ["Sue", "7", "cars", "6", "vizslas", "5", "cats", "3"]
        matches = re.findall(r"[A-Za-z]+|-?\d+", line)
        # Add a dictionary entry for each attribute and count from the 3rd item
        # on (as we don't care about the first two fields as they're redundant)
        items = {item: int(count) for item, count in zip(matches[2::2], matches[3::2])}
        sues.append(items)
    return sues


def find_sue(sues, search_results, operations):
    """
    Find the number of the Sue who matches the search_results.
    The operations parameter is used to determine how we compare each Sue
    attribute against the search results.
    """
    # Iterate over all Sues looking for a match
    for i, sue in enumerate(sues):
        match = True
        # For each of the known attributes of this Sue compare them (using the
        # provided operations) against the results from the MFCSAM
        for item, count in sue.items():
            if not operations[item](count, search_results[item]):
                match = False
                break
        # All of this Sue's attributes match the MFCSAM results.
        # We've found her!
        if match:
            return i + 1


sue_list = parse_sues(data)

# Part 1
# Find the correct Sue when comparing using == operators
print(find_sue(sue_list, MFCSAM_RESULTS, OPERATIONS_1))

# Part 2
# Find the correct Sue when we have to use different comparisons for each
# attribute
print(find_sue(sue_list, MFCSAM_RESULTS, OPERATIONS_2))
