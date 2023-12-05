"""
https://adventofcode.com/2023/day/5
"""

from utils.data import read_data
from utils.data import extract_ints
from utils.data import merge_overlapping_ranges

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

groups = data.split("\n\n")
seeds = extract_ints(groups[0])
mapping_groups = [group.split("\n") for group in groups[1:]]
maps = [[[range(src, src + length), range(dest, dest + length)]
        for mapping_range in mapping_group[1:]
        for dest, src, length in [extract_ints(mapping_range)]]
        for mapping_group in mapping_groups]


def walk_maps(conversion_maps, starting_seed):
    """
    Walks through the conversion maps in order to convert the initial seed value
    to the final location.
    """
    value = starting_seed
    for map_ranges in conversion_maps:
        for source_range, dest_range in map_ranges:
            # If the value is in the source range then we can convert it.
            # If not then it passes through unchanged.
            if value in source_range:
                delta = dest_range.start - source_range.start
                value += delta
                break
    return value


def walk_maps2(conversion_maps, seed_ranges):
    """
    Walks through the conversion maps in order to convert a list of seed ranges
    into a list of final location ranges.
    """
    for map_ranges in conversion_maps:
        next_seeds = []
        for seed_range in seed_ranges:
            mapped = False
            for source_range, dest_range in map_ranges:
                # Ignore if the seed range is not in the map range at all
                if ((seed_range.start >= source_range.stop) or
                    (seed_range.stop <= source_range.start)):
                    continue

                # We can directly process the seed range that is a subset of
                # the map range
                intersection_start = max(source_range.start, seed_range.start)
                intersection_stop = min(source_range.stop, seed_range.stop)
                delta = dest_range.start - source_range.start
                next_seeds.append(range(intersection_start + delta, intersection_stop + delta))
                mapped = True

                # Any parts of the seed range that are not covered by the
                # current map range need to be split out and processed against
                # the correct map range
                left_range = range(seed_range.start, intersection_start)
                right_range = range(intersection_stop, seed_range.stop)
                if left_range:
                    seed_ranges.append(left_range)
                if right_range:
                    seed_ranges.append(right_range)

            # If we didn't map the seed range to any map ranges then we just
            # pass the values through to the next mapping stage unchanged
            if not mapped:
                next_seeds.append(seed_range)

        # Merge any overlapping ranges in order to reduce the number of ranges
        # we need to process in the next mapping stage
        seed_ranges = merge_overlapping_ranges(next_seeds)

    return seed_ranges


# Part 1
# Find the lowest numbered location that can be reached from a starting seed.
print(min(walk_maps(maps, seed) for seed in seeds))

# Part 2
# Find the lowest numbered location that can be reached from a starting seed
# when the input seeds are a set of ranges instead of single values.
seeds = [range(src, src + length) for src, length in zip(seeds[::2], seeds[1::2])]
print(min(seed_range.start for seed_range in walk_maps2(maps, seeds)))
