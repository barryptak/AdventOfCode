"""
https://adventofcode.com/2016/day/22
"""
from utils import astar_path_length, extract_ints, manhattan_distance, Point2D, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def parse_data(data_in):
    """
    Read the node data from the input file.
    Returns a dict of used space, a dict of available space, and the highest x
    position in the grid
    """
    used = {}
    avail = {}

    highest_x = 0

    for line in data_in[2:]:
        x, y, _, u, a, _ = extract_ints(line)
        position = Point2D(x, y)
        used[position] = u
        avail[position] = a
        highest_x = max(x, highest_x)

    return used, avail, highest_x


def count_viable_pairs(used, avail):
    """"
    Counts the number of viable node pairs in the grid.
    Viable means that the data in one node can fit into another node.
    """
    count = 0
    for a in used.items():
        used_space = a[1]
        if used_space > 0:
            for b in avail.items():
                if a[0] == b[0]:
                    continue
                if used_space < b[1]:
                    count += 1

    return count


def get_empty_node():
    """ Gets the position of the empty node """
    for position, used in used_values.items():
        if used == 0:
            return position
    return None


def get_neighbours(position):
    """
    Used for our A* search - provides a list of valid nodes that the data from
    the specified node can be copied into. We exclude large nodes as we won't
    be able to put the data from that node somewhere else.
    """
    neighbours = []
    offsets = (Point2D(-1, 0), Point2D(1, 0), Point2D(0, -1), Point2D(0, 1))
    for offset in offsets:
        neighbour_pos = position + offset
        if neighbour_pos in used_values:
            if used_values[neighbour_pos] < 200:
                neighbours.append(neighbour_pos)
    return neighbours


# Read our data in
used_values, avail_values, goal_x = parse_data(data)


# Part 1
# Count the number of viable pairs
print(count_viable_pairs(used_values, avail_values))


# Part 2
# What are the minimum number of moves required to get the data from goal_x,0
# to 0,0?

# This isn't as complex as it seems. There is no situation where we transfer
# one node into another one that already contains data and so increase the
# number of empty nodes. This is just a sliding puzzle problem with some
# fixed/immovable nodes.
# What we really want to do is move the empty node _ to the left of G, then move
# G and _ left together until _ is in 0,0 and G is in 1,0, then do one
# final swap to get G into 0,0.
# The number of steps required to move _ and G left by one cell is 5 steps.
# The total steps to move _ and G from top right to top left are 5 * goal_x
# The final step is 1 step.
# So what we need to do if figure out how many steps it takes to move _ from
# its starting position to the left of G (goal_x - 1, 0). This is the
# Manhattan distance between the two positions (without obstructions (large
# unmovable nodes)). With obstructions we'll need to path find! :(

empty_start_pos = get_empty_node()
empty_target_pos = Point2D(goal_x - 1, 0)

stage_1_steps = astar_path_length([empty_start_pos], empty_target_pos, manhattan_distance, get_neighbours)
stage_2_steps = manhattan_distance(empty_target_pos, Point2D(0, 0)) * 5
total_steps = stage_1_steps + stage_2_steps + 1

print(total_steps)
