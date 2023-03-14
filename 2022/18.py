"""
https://adventofcode.com/2022/day/18
"""
import collections
import math
from utils.data import read_data, extract_ints, add_tuples

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

FILLED = 1
EMPTY = 0
OUTSIDE = -1
OFFSETS = ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1))


def parse_cubes(data_in):
    """
    Parse the cube data in.
    Returns the list of cubes, their state (filled or not), the min and max
    bounds of the space, and the answer to the exposed face count for part 1.
    """
    cube_set = set()
    states = collections.defaultdict(int)

    minimum_bounds = [math.inf, math.inf, math.inf]
    maximum_bounds = [-math.inf, -math.inf, -math.inf]
    exposed_sides = 0

    for cube_data in data_in:
        # Pull this cube from the data and add it to our list of cubes that we will
        # use in part 2
        cube = tuple(extract_ints(cube_data))
        cube_set.add(cube)
        states[cube] = FILLED

        # For Part 1
        # By default a cube will have 6 faces exposed.
        # If it's connected to a cube on one of its side then we need to deduct 2
        # from the expose face count as both cubes will have 1 face each touching
        exposed_sides += 6
        for offset in OFFSETS:
            other_cube = add_tuples(cube, offset)
            if states[other_cube]:
                exposed_sides -= 2

        # Update the bounds of all the cubes so far
        # This is used in part 2
        minimum_bounds = map(min, minimum_bounds, cube)
        maximum_bounds = map(max, maximum_bounds, cube)

    return cube_set, states, minimum_bounds, maximum_bounds, exposed_sides


def in_bounds(pos, volume_bounds):
    """ Is the position inside or outside of the volume? """
    inside = (p in bound for p, bound in zip(pos, volume_bounds))
    return all(inside)


def crude_fill(start_pos, volume_bounds, values, fill_value):
    """
    Crude flood fill
    Starts at start_pos and crawls over all connected positions within
    volume_bounds that are empty setting their value to fill_value
    """

    # Start with just our starting position in the queue
    queue = collections.deque()
    queue.append(start_pos)

    # Pop positions from the queue until it's empty
    while len(queue) > 0:
        pos = queue.pop()

        # If this position is within the volume AND it's currently empty
        # then set it to filled and append all of its connected neighbours to
        # the queue
        if in_bounds(pos, volume_bounds) and values[pos] == EMPTY:
            values[pos] = fill_value
            for offset in OFFSETS:
                queue.append(add_tuples(pos, offset))


def count_outside_faces(cube_list, states, minimum_bounds, maximum_bounds):
    """
    Counts the number of outside faces on the shape by performing a flood fill
    to determine the outside faces (as opposed to the faces in internal
    cavities).
    """
    # We can figure this out by performing a crude flood fill from a position
    # that we know is outside of the cube volume.
    # We mark every empty cell that we touch as empty and can use that
    # information to determine how many cube faces are touching empty space and
    # are thus on the outside of the shape.

    # Create a volume with a gap of at least one around all sides of the cubes
    volume = [range(min_bound - 1, max_bound + 2)
              for min_bound, max_bound in zip(minimum_bounds, maximum_bounds)]

    # Start our flood fill somewhere on the edge of the volume since we know it
    # will not have a cube in it
    known_outside_position = tuple(r.start for r in volume)
    crude_fill(known_outside_position, volume, states, OUTSIDE)

    # For each cube that we read in from the input check how many of its
    # neighbours are marked as being outside. This gives us the total number of
    # outside faces
    return sum(1 for cube in cube_list
               for offset in OFFSETS
               if states[add_tuples(cube, offset)] == OUTSIDE)


# Parse the data needed for part 2 and calculate part 1 at the same time
cubes, cube_states, min_bounds, max_bounds, exposed_face_count = parse_cubes(data)

# Part 1
# How many cube faces are 'exposed' (i.e. not connected to another cube)?
print(exposed_face_count)

# Part 2
# What is the exterior surface size (i.e. ignoring internal chambers)?
print(count_outside_faces(cubes, cube_states, min_bounds, max_bounds))
