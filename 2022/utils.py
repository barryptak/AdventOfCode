import os
import re
import __main__ as main

def read_data(use_test_data, split_by_line = True):
    """
    Read puzzle input data in from text file.
    We figure out the name of the script being run (e.g. 1.py) and infer the appropriate data file to load (e.g. data/1.txt)
    use_test_data - if True then load data from ./test.txt instead for quick testing purposes
    split_by_line - if True then output is in a list with one entry per line in the input data, if False then output is a single string with all file contents in it
    """
    path_name, file_name = os.path.split(main.__file__)
    file_name = "test.txt" if use_test_data else (file_name.split('.')[0] + ".txt")
    file_path = os.path.join(path_name, "data", file_name)

    with open(file_path, "r") as f:
        data = f.read().strip()
    
    if split_by_line:
        data = data.split("\n")

    return data

def extract_ints(s):
    """ Extracts a list of all ints found in the supplied string """
    m = re.findall("-?\d+", s)
    return [int(x) for x in m]