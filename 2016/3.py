"""
https://adventofcode.com/2016/day/3
"""
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def count_possible_triangles(triangle_data):
    """
    Returns the count of how many valid/possible triangles the input data
    contains
    """
    count = 0
    for triangle in triangle_data:
        # Pull all of the ints from each lines and sort them so that we can simply
        # check if the sum of the first and second is greater than the (longest)
        # third side.
        sides = sorted(extract_ints(triangle))
        if sum(sides[0:2]) > sides[2]:
            count += 1

    return count


def count_possible_triangles_2(triangle_data):
    """
    Returns the count of how many valid/possible triangles the input data
    contains when the triangle sides are defined in columns
    """
    count = 0
    for index in range(0, len(triangle_data), 3):
        # Pull out all of the ints from this set of three rows
        sides = [extract_ints(triangle_data[index + i]) for i in range(3)]
        # Pull the sides for each of the three triangles and sort them for easy
        # comparison
        triangles = [sorted([sides[0][i], sides[1][i], sides[2][i]]) for i in range(3)]
        # Count how many of our three triangles are possible
        count += sum(1 for i in range(3) if sum(triangles[i][0:2]) > triangles[i][2])

    return count


# Part 1
# How many of the triangles are possible?
print(count_possible_triangles(data))

# Part 2
# How many triangles are possible if the sides are in columns in groups of
# three?
print(count_possible_triangles_2(data))
