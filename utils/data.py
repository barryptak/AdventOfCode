"""
Data parsing helpers for Advent of Code problems.
"""

import os
import re
import __main__ as main


def read_data(use_test_data, split_by_line=True, strip=True, input_file_name=None):
    """
    Read puzzle input data in from text file.
    We figure out the name of the script being run (e.g. 1.py) and infer the
    appropriate data file to load (e.g. data/1.txt)

    Args:
        use_test_data (bool): If True then load data from data/test.txt instead
            for quick testing purposes.
        split_by_line (bool, optional): If True then output is in a list with
            one entry per line in the input data, if False then output is a
            single string with all file contents in it. Defaults to True.
        strip (bool, optional): Whether to strip input data or not. Defaults to
            True.
        input_file_name (str, optional): Use this to override the file to load
            data from. Defaults to None.

    Returns:
        str or list: Data as read from input file. If split_by_line is True
            then return type is a list of strings. If split_by_line is False
            then return type is a single string.
    """
    path_name, file_name = os.path.split(main.__file__)
    if not input_file_name:
        input_file_name = "test.txt" if use_test_data else (
            file_name.split('.')[0] + ".txt")
    file_path = os.path.join(path_name, "data", input_file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        if strip:
            data = data.strip()

    if split_by_line:
        data = data.split("\n")

    return data


def extract_ints(input_string):
    """ Extracts a list of all ints found in the supplied string """
    return [int(i) for i in re.findall(r"-?\d+", input_string)]


def add_tuples(tuple1, tuple2):
    """
    Adds two tuples (or lists, etc) element by element and returns a tuple
    containing the results
    """
    return tuple(map(lambda x, y: x + y, tuple1, tuple2))


def merge_overlapping_ranges(ranges):
    """ Sorts and merges a list of ranges to remove any overlaps. """
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key = lambda r: r.start)
    merged_ranges = [sorted_ranges[0]]

    for current_range in sorted_ranges[1:]:
        last_merged_range = merged_ranges[-1]
        if current_range.start <= last_merged_range.stop:
            merged_ranges[-1] = range(last_merged_range.start,
                                      max(last_merged_range.stop, current_range.stop))
        else:
            merged_ranges.append(current_range)

    return merged_ranges