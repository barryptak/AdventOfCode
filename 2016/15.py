"""
https://adventofcode.com/2016/day/15
"""
from utils import extract_ints, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def parse_data(data_in):
    """ Read the input data to retrieve the disc positions """
    num_positions = []
    starting_pos = []

    for line in data_in:
        ints = extract_ints(line)
        num_positions.append(ints[1])
        starting_pos.append(ints[3])

    return num_positions, starting_pos


def is_at_zero(num_positions, starting_pos, disc_index, time):
    """ Is the specified disc at the zero position at the given time? """
    pos = (starting_pos[disc_index] + time) % num_positions[disc_index]
    return pos == 0


def find_time(num_positions, starting_pos):
    """
    Find the time at which to release a capsule so that it passes through all
    discs successfully
    """

    # What's the first time that we can release the disc where it reaches the
    # first disc as it's at position 0?
    candidate_time = num_positions[0] - starting_pos[0] - 1

    while True:
        # Are all discs at position 0 when the capsule reaches them?
        collision = False
        for disc_index in range(len(num_positions)):
            time_capsule_reaches_disc = candidate_time + disc_index + 1
            if not is_at_zero(num_positions, starting_pos, disc_index, time_capsule_reaches_disc):
                collision = True
                break

        # There was no collision with any disc! candidate_time is the correct answer!
        if not collision:
            return candidate_time

        # There was a collision so candidate_time isn't a valid result.
        # Increment it to the next time that disc 1 (index 0) is at the zero position.
        candidate_time += num_positions[0]


positions, starting = parse_data(data)

# Part 1
# At what time can we release the capsule to pass through all of the discs?
print(find_time(positions, starting))

# Part 2
# What if we add another disc at the bottom?
positions.append(11)
starting.append(0)
print(find_time(positions, starting))
