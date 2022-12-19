"""
https://adventofcode.com/2022/day/7
"""
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

stack = []
files = {}
dirs = []
path_size = {"": 0}

for line in data:
    parts = line.split()

    # Look commands
    if parts[0] == "$":
        # We only care about cd command and can safely ignore the ls ones (as we will pick up their output later)
        if parts[1] == "cd":
            if parts[2] == "..":
                stack.pop()
            elif parts[2] == "/":
                stack = []
            else:
                stack.append(parts[2])
                path = "/".join(stack)
                path_size[path] = 0
    # ignore dir listings as we assume that we enter and ls inside every directory
    # (since otherwise the size calculations would be missing data anyway).
    # We could create path_size entries for all listed dirs just to be safe though.
    elif parts[0] == "dir":
        continue
    else:
        # This must be a file size and name listing. Store the file size.
        size = int(parts[0])
        name = parts[1]
        path = "/".join(stack + [name])
        files[path] = size

# Iterate over all files and add their size to each directory above them
for file, size in files.items():
    end_of_path_indices = [i for i in range(len(file)) if file[i] == "/"]
    for i in end_of_path_indices:
        path_size[file[:i]] += size
    path_size[""] += size

# Part 1 - sum of all dir sizes less than 100000
print(sum([dir_size for dir_size in path_size.values() if dir_size <= 100000]))

# Part 2 - size of smallest dir that can be deleted to have at least 30000000 free
total_space = 70000000
space_free = total_space - path_size[""]
needed_space = 30000000
need_to_free = needed_space - space_free
print(min([dir_size for dir_size in path_size.values() if dir_size >= need_to_free]))