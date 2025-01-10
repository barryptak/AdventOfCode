"""
https://adventofcode.com/2023/day/14
"""

import copy
from utils.data import read_data


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

platform1 = [list(line) for line in data]

# Actually, find each O in order from top to bottom then scan through all the . above it until we find a #, O or end of platform, then move the O and replace it with a .


for y, row in enumerate(platform1):
    for x, cell in enumerate(row):
        if cell == "O":
            # Walk upwards until we find a non-.
            found = None
            for y2 in range(y - 1, -1, -1):
                if platform1[y2][x] in ["#", "O"]:
                    break
                found = y2

            if found is not None:
                platform1[y][x] = "."
                platform1[found][x] = "O"

total = 0
for y, row in enumerate(platform1):
    total += sum(cell == "O" for cell in row)*(len(platform1) - y)

print(total)


def platform_hash(platform):
    return hash("".join("".join(row) for row in platform))

north_cache = {}
south_cache = {}
east_cache = {}
west_cache = {}

def print_platform(platform):
    for row in platform:
        print("".join(row))
    print("\n")


def walk_north(platform):
    # hash = platform_hash(platform)
    # if hash in north_cache:
    #     return north_cache[hash]

    for y, row in enumerate(platform):
        for x, cell in enumerate(row):
            if cell == "O":
                # Walk upwards until we find a non-.
                found = None
                for y2 in range(y - 1, -1, -1):
                    if platform[y2][x] in ["#", "O"]:
                        break
                    found = y2

                if found is not None:
                    platform[y][x] = "."
                    platform[found][x] = "O"

    # north_cache[hash] = platform

def walk_south(platform):
    # hash = platform_hash(platform)
    # if hash in south_cache:
    #     return south_cache[hash]

    for y in range(len(platform) - 1, -1, -1):
        row = platform[y]
        for x, cell in enumerate(row):
            if cell == "O":
                # Walk down until we find a non-.
                found = None
                for y2 in range(y + 1, len(platform)):
                    if platform[y2][x] in ["#", "O"]:
                        break
                    found = y2

                if found is not None:
                    platform[y][x] = "."
                    platform[found][x] = "O"

    # south_cache[hash] = platform

def walk_east(platform):
    # hash = platform_hash(platform)
    # if hash in east_cache:
    #     return east_cache[hash]

    for x in range(len(platform[0]) - 1, -1, -1):
        for y, row in enumerate(platform):
            cell = row[x]
            if cell == "O":
                # Walk right until we find a non-.
                found = None
                for x2 in range(x + 1, len(row)):
                    if platform[y][x2] in ["#", "O"]:
                        break
                    found = x2

                if found is not None:
                    platform[y][x] = "."
                    platform[y][found] = "O"

    # east_cache[hash] = platform

def walk_west(platform):
    # hash = platform_hash(platform)
    # if hash in west_cache:
    #     return west_cache[hash]

    for y, row in enumerate(platform):
        for x, cell in enumerate(row):
            if cell == "O":
                # Walk left until we find a non-.
                found = None
                for x2 in range(x - 1, -1, -1):
                    if platform[y][x2] in ["#", "O"]:
                        break
                    found = x2

                if found is not None:
                    platform[y][x] = "."
                    platform[y][found] = "O"

    # west_cache[hash] = platform


platform2 = [list(line) for line in data]
history = []#[platform_hash(platform2)]
CYCLES = 1_000_000_000
done = False
for i in range(CYCLES):
#    start = platform_hash(platform2)

    #print_platform(platform2)
    walk_north(platform2)
    #print_platform(platform2)
    walk_west(platform2)
    #print_platform(platform2)
    walk_south(platform2)
    #print_platform(platform2)
    walk_east(platform2)
    #print_platform(platform2)
    end = platform_hash(platform2)

    for j, (h, p) in enumerate(history):
        if end == h:
            loop_length = len(history) - j
            cycles_left = CYCLES - i - 1

            print("Found cycle at", i)
            print("Cycle length is", loop_length)
            final_index = (cycles_left % loop_length) + j
            platform2 = history[final_index][1]


            done = True
            break

    if done:
        break

    history.append((end, copy.deepcopy(platform2)))

    # if start == end:
    #     break

total = 0
for y, row in enumerate(platform2):
    total += sum(cell == "O" for cell in row)*(len(platform2) - y)

print(total)