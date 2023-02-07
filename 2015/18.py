"""
https://adventofcode.com/2015/day/18
"""
from itertools import product
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Read the data for the light grid in and pad it on all sides with False values.
# This allows us later on to read
light_grid = [[False] + [l == "#" for l in line] + [False] for line in data]
light_grid.insert(0, [False]*len(light_grid[0]))
light_grid.append([False]*len(light_grid[0]))


def next_light_state(grid, x, y):
    """
    Determine the next state of the light at x, y given the present state of
    the light grid
    """
    # Count how many lights are on in the 3x3 area around this light
    on_count = 0
    for x_2, y_2 in product(range(x-1,x+2), range(y-1, y+2)):
        if grid[y_2][x_2]:
            on_count += 1

    # If (this light is on AND 2 or 3 neighbours are on) OR
    # (this light is off and 3 neighbours are on) then light is on.
    # Otherwise it's off.
    # The numbers below are 3 and 4 because we've changed the test slightly so
    # that we require fewer operations, but the result is the same.
    return on_count == 3 or (on_count == 4 and grid[y][x])


def turn_on_corner_lights(grid):
    """ Force the four corner lights to be on """
    grid[1][1] = grid[1][-2] = grid[-2][1] = grid[-2][-2] = True


def simulate_lights(grid, steps, force_corner_lights_on=False):
    """ Simulate the grid of lights for the specified number of steps """
    y_range = range(1, len(grid) - 1)
    x_range = range(1, len(grid[0]) - 1)

    for _ in range(steps):
        # Determine the new light values using the Game of Life rules
        new_grid = [[False]*len(line) for line in grid]
        for x, y in product(x_range, y_range):
            new_grid[y][x] = next_light_state(grid, x, y)

        if force_corner_lights_on:
            turn_on_corner_lights(new_grid)

        grid = new_grid

    return grid


# Part 1
# Simualte the lights for 100 steps and count the final lit number
final_lights = simulate_lights(light_grid, 100)
light_count = sum(1 for row in final_lights for light in row if light)
print(light_count)


# Part 2
# Simualte the lights for 100 steps when the four corner lights are stuck on
# and count the final lit number
turn_on_corner_lights(light_grid)
final_lights = simulate_lights(light_grid, 100, True)
light_count = sum(1 for row in final_lights for light in row if light)
print(light_count)
