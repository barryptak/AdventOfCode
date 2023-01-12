"""
https://adventofcode.com/2022/day/7
"""
from utils import read_data

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
        # We only care about cd command and can safely ignore the ls ones
        # (as we will pick up their output later)
        if parts[1] == "cd":
            if parts[2] == "..":
                stack.pop()
            elif parts[2] == "/":
                stack = []
            else:
                stack.append(parts[2])
                path = "/".join(stack)
                path_size[path] = 0
    # ignore dir listings as we assume that we enter and ls inside every
    # directory (since otherwise the size calculations would be missing data
    # anyway). We could create path_size entries for all listed dirs just to be
    # safe though.
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


# Part 1
# Sum of all dir sizes less than 100000
SIZE_LIMIT = 100000

all_dir_sizes_under_limit = [dir_size for dir_size in path_size.values() if dir_size <= SIZE_LIMIT]
sum_of_dir_sizes = sum(all_dir_sizes_under_limit)

print(sum_of_dir_sizes)

# Part 2
# Size of smallest dir that can be deleted to have at least 30000000 free
TOTAL_SPACE = 70000000
SPACE_FREE = TOTAL_SPACE - path_size[""]
NEEDE_SPACE = 30000000
NEED_TO_FREE = NEEDE_SPACE - SPACE_FREE

all_dir_sizes_over_limit = [dir_size for dir_size in path_size.values() if dir_size >= NEED_TO_FREE]
smallest_dir_size_over_limit = min(all_dir_sizes_over_limit)

print(smallest_dir_size_over_limit)
