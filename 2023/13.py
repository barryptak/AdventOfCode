"""
https://adventofcode.com/2023/day/13
"""

from utils.data import read_data


USE_TEST_DATA = True
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def find_horizontal_reflection(terrain):
    reflections = []
    for y in range(len(terrain) - 1):
        match = True
        for y1, y2 in zip(terrain[y::-1], terrain[y+1:]):
            if y1 != y2:
                match = False
                break

        if match:
            reflections.append(y + 1)

    return reflections


def get_all_reflections(row):
    reflections = []
    for x in range(len(row) - 1):
        match = True
        for x1, x2 in zip(row[x::-1], row[x+1:]):
            if x1 != x2:
                match = False
                break

        if match:
            reflections.append(x + 1)

    return reflections


def find_vertical_reflection(terrain):
    reflections_set = set(i for i in range(1, len(terrain[0]) + 1))
    for row in terrain:
        reflections = get_all_reflections(row)
        reflections_set.intersection_update(reflections)
        if len(reflections_set) == 0:
            return []

    return list(reflections_set)



terrains = [terrain.split("\n") for terrain in data.split("\n\n")]
for terrain in terrains:
    for y, row in enumerate(terrain):
        terrain[y] = list(row)

old_reflections = []

total = 0
for terrain in terrains:
    found = False
    for val in find_horizontal_reflection(terrain):
        if val:
            #print(val)
            total += val*100
            old_reflections.append((val, None))
            found = True
            break
    if not found:
        for val in find_vertical_reflection(terrain):
            if val:
                #print(val)
                total += val
                old_reflections.append((None, val))
                break

print(total)



import copy


total = 0
for terrain in terrains:

    terrain2 = copy.deepcopy(terrain)
    found = False
    for y, row in enumerate(terrain2):
        for x, cell in enumerate(row):
            row[x] = "." if cell == "#" else '#'

            for val in find_horizontal_reflection(terrain2):
                if val and val != old_reflections[y][0]:
                    #print(val)
                    total += val*100
                    found = True
                    break
            else:
                for val in find_vertical_reflection(terrain2):
                    if val and val != old_reflections[x][1]:
                        #print(val)
                        total += val
                        found = True
                        break

            if found:
                break
        if found:
            break


print(total)

