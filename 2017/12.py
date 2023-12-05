"""
https://adventofcode.com/2017/day/12
"""
from utils.data import read_data
from utils.data import extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Parse the pipe/connection data into a list of lists of program ids that can
# be communicated with from the current program index.
connections = [extract_ints(line)[1:] for line in data]


def walk(program_id, pipes, visited):
    """
    Walk from the current program to all connected programs adding them to the
    visited set.
    """
    for pipe in pipes[program_id]:
        if pipe not in visited:
            visited.add(pipe)
            walk(pipe, pipes, visited)


# Walk over all programs, find all connected programs and store the size of each
# connected group.
visited_group_sizes = []
visited_programs = set()
for current_program_id in range(len(data)):
    if current_program_id not in visited_programs:
        group_program_ids = set()
        group_program_ids.add(current_program_id)
        walk(current_program_id, connections, group_program_ids)
        visited_group_sizes.append(len(group_program_ids))
        visited_programs.update(group_program_ids)


# Part 1 - How many programs are in the group that contains program ID 0?
print(visited_group_sizes[0])

# Part 2 - How many groups are there?
print(len(visited_group_sizes))
