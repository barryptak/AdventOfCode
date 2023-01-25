"""
https://adventofcode.com/2015/day/9
"""
import math
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def add_distance(dists, loc_1, loc_2, dist):
    """ Store the distance between two locations """
    if loc_1 not in dists:
        dists[loc_1] = {}

    dists[loc_1][loc_2] = dist

    if loc_2 not in dists:
        dists[loc_2] = {}

    dists[loc_2][loc_1] = dist


def parse_distances(input_data):
    """ Parse the distance data from the input strings """
    dists = {}
    for line in input_data:
        location_1, _, location_2, _, dist = line.split()
        add_distance(dists, location_1, location_2, int(dist))
    return dists


def all_paths(starting_loc, other_locations, dists):
    """
    Generator function returning all permutations of paths (and their lengths)
    from starting_location through all other locations
    """
    for location in other_locations:
        for child_path, child_dist in all_paths(location, other_locations - {location}, dists):
            yield [starting_loc] + child_path, dists[starting_loc][location] + child_dist

    if len(other_locations) == 0:
        yield [starting_loc], 0


# Parts 1 & 2
# Find the length of the shortest and longest paths through all locations
# exactly once

distances = parse_distances(data)
locations = set(distances.keys())

shortest_path = math.inf
longest_path = 0

for start_loc in locations:
    for path, distance in all_paths(start_loc, locations - {start_loc}, distances):
        shortest_path = min(shortest_path, distance)
        longest_path = max(longest_path, distance)

print(shortest_path)
print(longest_path)
