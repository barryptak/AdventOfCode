"""
https://adventofcode.com/2016/day/9
"""
import re
from math import prod
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def get_decompressed_length(compressed_data):
    """ Gets the final decompressed length of the input data """
    decompressed_length = 0
    index = 0
    while index < len(data):
        # Find the next marker location
        match = re.search(r"\((\d+)x(\d+)\)", compressed_data[index:])
        if match:
            # Add the section before the marker
            decompressed_length += match.start()

            # Repeat the section indicated by the marker
            length = int(match.groups()[0])
            repeat = int(match.groups()[1])
            decompressed_length += length*repeat

            # Update to the new index
            index += match.end() + length
        else:
            # Add the last markerless section
            decompressed_length += len(data) - index
            break

    return decompressed_length


def get_multiplier(query_index, multiplier_list):
    """
    Returns the accumulated multiplier to apply to the input character length
    at index query_index
    """
    return prod(m[2] for m in multiplier_list if m[0] <= query_index < m[1])


def get_decompressed_length_2(compressed_data):
    """
    Gets the final decompressed length of the input data when we decompress
    nested markers too
    """

    decompressed_length = 0
    index = 0
    multipliers = []
    while index < len(data):
        # Find the next marker location
        match = re.search(r"\((\d+)x(\d+)\)", compressed_data[index:])
        if match:
            # Add the start and end indices and the repeat value for this
            # multiplier to our list for future look up
            length = int(match.groups()[0])
            repeat = int(match.groups()[1])
            multiplier_start_index = index + match.end()
            multiplier_end_index = multiplier_start_index + length
            multipliers.append((multiplier_start_index, multiplier_end_index, repeat))

            # Add the section before the marker
            for i in range(index, index + match.start()):
                decompressed_length += get_multiplier(i, multipliers)

            # Update to the new index
            index += match.end()

            # Clean up any multipliers that we won't need again in order to keep
            # the size of the list that we search through down
            multipliers = [m for m in multipliers if index <= m[1]]
        else:
            # Add the last markerless section
            for i in range(index, len(data)):
                decompressed_length += get_multiplier(i, multipliers)
            break

    return decompressed_length


# Part 1
# Find the length of the decompressed file
print(get_decompressed_length(data))

# Part 2
# Find the length of the decompressed file when we decompress nested markers
print(get_decompressed_length_2(data))
