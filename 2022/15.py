"""
https://adventofcode.com/2022/day/15
"""
import functools
from utils import read_data, extract_ints, Point2D, manhattan_distance

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def sort_ranges(range1, range2):
    """ Sorting helper that sorts ranges by the starting value of the range """
    if range1.start < range2.start:
        return -1
    elif range1.start == range2.start:
        return 0
    return 1


def collapse_ranges(ranges):
    """
    Takes a list of ranges and collapses them into as short a list as
    possible by throwing away ranges completely contained by others, and
    by joining together overlapping ranges into one.
    """

    # Sort the ranges by start value
    ranges.sort(key=functools.cmp_to_key(sort_ranges))

    # Collapse ranges together when they overlap
    
    collapsed_ranges = []
    starting_range = ranges[0]
    start_x = starting_range.start
    end_x = starting_range.stop
    for next_range in ranges[1:]:
        # is next_range entirely contained in the current one?
        if next_range.stop <= end_x:
            # Continue to the next range. We don't need to do anything
            # with this one as it's already covered by current.
            continue
        # does next_range overlap and extend the current range?
        elif next_range.start <= end_x:
            # Extend the end of the current window to match next_range
            end_x = next_range.stop
        # no overlap
        else:
            # There's no overlap at all so add the current window and start a new one
            collapsed_ranges.append(range(start_x, end_x))
            start_x = next_range.start
            end_x = next_range.stop

    # Don't forget to capture the currently open window when we reach the end of the ranges
    collapsed_ranges.append(range(start_x, end_x))
    return collapsed_ranges


def get_no_beacon_windows(sensor_list, row_index, x_range=None):
    """
    Returns a list of ranges for the given row/y in which we know there are no
    beacons.
    We do this by iterating over every sensor and determining the range of x
    values that we know cannot contain a beacon.
    """
    no_beacon_windows = []

    # Iterate over all sensors and determine what coverage they apply to the
    # current row. We can then mark those sections of the row as NOT having
    # a beacon.
    for sensor_position, beacon_distance in sensor_list:
        # Calculate how many steps horizontally we can take along the given row
        # for the given sensor and still be within the window in which we know
        # there are no other beacons
        dist_to_row = abs(row_index - sensor_position.y)
        overlap = beacon_distance - dist_to_row
        
        # No overlap means this sensor does not affect this row. Move on.
        if overlap < 0:
            continue

        # Get the start and end of this range
        start_x = sensor_position.x - overlap
        end_x = sensor_position.x + overlap + 1

        # Clamp the range based on the map size constraints passed in
        if x_range is not None:
            if start_x >= x_range.stop or end_x < x_range.start:
                continue
            else:
                start_x = max(start_x, x_range.start)
                end_x = min(end_x, x_range.stop)

        # Add the range in which we know there is no missing beacon to our list
        window = range(start_x, end_x)
        no_beacon_windows.append(window)

    # Return the ranges collapsed into as few as possible
    return collapse_ranges(no_beacon_windows)

# Parse data to extract postions of sensors and beacons
sensors = []
beacons = set()
for line in data:
    ints = extract_ints(line)
    sensor_pos = Point2D(ints[:2])
    beacon_pos = Point2D(ints[2:])

    dist = manhattan_distance(sensor_pos, beacon_pos)

    sensors.append((sensor_pos, dist))
    beacons.add(beacon_pos)


# Part 1
# Determine how many positions in row TEST_ROW CANNOT contain a beacon
TEST_ROW = 10 if USE_TEST_DATA else 2000000
no_beacon_ranges = get_no_beacon_windows(sensors, TEST_ROW)
num_non_beacon_positions = sum([len(r) for r in no_beacon_ranges])
num_beacons = len([b for b in beacons if b.y == TEST_ROW])
print(num_non_beacon_positions - num_beacons)


# Part 2
# Find the only possible position within SEARCH_RANGE for the missing
# beacon and determine its tuning frequency (based on its location)

# Iterate over every row within the testing window and check if it has more
# than one range of positions that DO NOT contain beacons.
# If it does then this must be the row that contains our single missing
# position.
# This seems rather slow, so there's presumably a massively simpler way to do
# this, but this works!
SEARCH_RANGE = 21 if USE_TEST_DATA else 4000001
for search_row in range(SEARCH_RANGE):
    no_beacon_ranges = get_no_beacon_windows(sensors, search_row, range(SEARCH_RANGE))
    if len(no_beacon_ranges) > 1:
        # If there is more than one beacon free range then the missing beacon
        # must be between the two ranges. Its x position is at the stop position
        # of the first range
        tuning_frequency = (no_beacon_ranges[0].stop * 4000000) + search_row
        print(tuning_frequency)
        break

# Note - I did write this pivoted around to iterate over the sensors and create
# the complete set of ranges that way. If you need to evaluate the entire map
# then this approach would be faster. But we don't. So it's not in this case.
# The code wasn't complicated, but the above solution is shorter and simpler
# to follow, so I've stuck with it.
