"""
Helpers for Advent of Code problems.
"""

import os
import re
import __main__ as main


def read_data(use_test_data, split_by_line=True, input_file_name=None):
    """
    Read puzzle input data in from text file.
    We figure out the name of the script being run (e.g. 1.py) and infer the
    appropriate data file to load (e.g. data/1.txt)
    use_test_data - if True then load data from ./test.txt instead for quick
                    testing purposes
    split_by_line - if True then output is in a list with one entry per line in
                    the input data, if False then output is a single string with
                    all file contents in it
    """
    path_name, file_name = os.path.split(main.__file__)
    if not input_file_name:
        input_file_name = "test.txt" if use_test_data else (
            file_name.split('.')[0] + ".txt")
    file_path = os.path.join(path_name, "data", input_file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read().strip()

    if split_by_line:
        data = data.split("\n")

    return data


def extract_ints(s):
    """ Extracts a list of all ints found in the supplied string """
    return [int(i) for i in re.findall("-?\d+", s)]


def add_lists(a, b):
    """
    Adds two lists (or tuples, etc) element by element and returns a list
    containing the results
    """
    return list(map(lambda x, y: x + y, a, b))

class Point2D:
    """ 2D integer Point class """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))
