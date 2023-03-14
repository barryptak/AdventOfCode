"""
https://adventofcode.com/2022/day/23
"""
import copy
import math
from collections import defaultdict
from utils.data import read_data
from utils.point2d import Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

moves = ((Point2D(-1, -1), Point2D( 0, -1), Point2D( 1, -1)),
         (Point2D(-1,  1), Point2D( 0,  1), Point2D( 1,  1)),
         (Point2D(-1, -1), Point2D(-1,  0), Point2D(-1,  1)),
         (Point2D( 1, -1), Point2D( 1,  0), Point2D( 1,  1)))

OFFSETS = (Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1),
           Point2D(-1, 0), Point2D(1, 0),
           Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1))


def update_move_index(index):
    """
    Increments the move index (which indicates which direction we should
    attempt to move in next) and wraps it back to zero when necessary
    """
    index += 1
    if index >= len(moves):
        index = 0
    return index


def in_bounds(pos, grid):
    """ Is the position within the bounds of the grid? """
    return (0 <= pos.y < len(grid) and
            0 <= pos.x < len(grid[pos.y]))


def is_isolated(pos, grid, test_offsets):
    """ Are all of the positions offset from pos empty? """
    for offset in test_offsets:
        new_pos = pos + offset
        if in_bounds(new_pos, grid):
            if grid[new_pos.y][new_pos.x] == "#":
                return False
    return True


def get_next_position(pos, grid, move_index):
    """ Gets the next position for the elf at pos to move to """
    if is_isolated(pos, grid, OFFSETS):
        return pos

    index = move_index
    for _ in range(4):
        if is_isolated(pos, grid, moves[index]):
            return pos + moves[index][1]

        index = update_move_index(index)

    return pos


def run_round(grid, move_index):
    """
    Runs one movement round.
    move_index indicates which direction to attempt to move in first
    """
    new_positions = defaultdict(lambda: [])

    min_y = len(grid)
    max_y = -1
    min_x = len(grid[0])
    max_x = -1

    # Calc new positions
    for pos_y, row in enumerate(grid):
        for pos_x, cell_value in enumerate(row):
            if cell_value == "#":
                pos = Point2D(pos_x, pos_y)
                new_pos = get_next_position(pos, grid, move_index)

                # We don't just write to the new position - we actually write
                # the old position into a list associated with the new location
                # instead. This because more than one elf might want to move
                # there.
                # When applying the new positions below, when we detect that
                # more than one elf wants to move to the new position we
                # use the list of their old positions to place them back where
                # they were previously instead.
                new_positions[new_pos].append(pos)

                min_y = min(min_y, new_pos.y, pos.y, 0)
                max_y = max(max_y, new_pos.y, pos.y)
                min_x = min(min_x, new_pos.x, pos.x, 0)
                max_x = max(max_x, new_pos.x, pos.x)

    # Apply new positions

    new_grid = defaultdict(lambda: defaultdict(lambda: "."))
    move_count = 0
    for pos in new_positions:
        # Did a single elf move to this position?
        if len(new_positions[pos]) == 1:
            # Single elf only - set the elf position on the new grid
            # (while adjusting the overall grid coords to start at 0,0 again)
            new_grid[pos.y - min_y][pos.x - min_x] = "#"
            if new_positions[pos][0] != pos:
                move_count += 1
        # Did more than one elf want to move to this position?
        else:
            # More than one elf tried to move here - put everyone back to their
            # original positions
            # (while adjusting the overall grid coords to start at 0,0 again)
            old_positions = new_positions[pos]
            for old_pos in old_positions:
                new_grid[old_pos.y - min_y][old_pos.x - min_x] = "#"

    # The new_grid that we've formed is a default_dict rather than a list that
    # we can iterate through.
    # Let's convert it to a flattened list for use in the next round.
    flattened_grid = []
    for pos_y in range(max_y - min_y + 1):
        row = [new_grid[pos_y][pos_x] for pos_x in range(max_x - min_x + 1)]
        flattened_grid.append("".join(row))

    return flattened_grid, move_count


def run_rounds(grid, max_rounds = math.inf, dir_check_index = 0):
    """
    Run up to max_rounds rounds of movement.
    Stop when we complete max_rounds round OR no further moves are made.
    Returns the final grid layout and the number of rounds run.
    """
    round_num = 1
    while round_num <= max_rounds:
        grid, moves_made = run_round(grid, dir_check_index)

        # Increment the index that indicates what direction we should check in the
        # next round
        dir_check_index = update_move_index(dir_check_index)

        if moves_made == 0:
            return grid, round_num, dir_check_index

        round_num += 1

    return grid, max_rounds, dir_check_index


def calc_min_bounds(grid):
    """ Find the bounds of the grid that actually contain elves """

    def find_first_elf_in_row(grid):
        for row_index, row in enumerate(grid):
            if row.find("#") >= 0:
                return row_index

    def find_first_elf_in_column(grid, col_range):
        for col in col_range:
            for row in grid:
                if row[col] == "#":
                    return col

    # Find the first and last rows containing an elf
    max_y_index = len(grid) - 1
    min_y = find_first_elf_in_row(grid)
    max_y = max_y_index - find_first_elf_in_row(reversed(grid))

    # Find the first and last columns containing an elf
    grid_width_range = range(len(grid[0]))
    min_x = find_first_elf_in_column(grid, grid_width_range)
    max_x = find_first_elf_in_column(grid, reversed(grid_width_range))

    return min_x, min_y, max_x, max_y


def calc_empty_tiles(grid):
    """
    Calculates how many empty tiles there are in the grid inside the bounds of
    the outermost elves
    """

    # Calculate the area covered by the outermost elves and subtract the number
    # of elves to get the number of empty tiles

    min_x, min_y, max_x, max_y = calc_min_bounds(grove_grid)
    area = (max_x - min_x + 1) * (max_y - min_y + 1)

    num_elves = sum([len([c for c in line if c == "#"]) for line in grid])
    empty_tile_count = area - num_elves

    return empty_tile_count

# Part 1
# Run 10 rounds of movement and calculate how many empty tiles there are
# within the bounds formed by the outermost elves

# Run the simulation
grove_grid = copy.deepcopy(data)
grove_grid, _, dir_index = run_rounds(grove_grid, 10)
empty_tiles = calc_empty_tiles(grove_grid)
print(empty_tiles)


# Part 2
# Continue to run movement rounds until no further moves are made
_, rounds, _ = run_rounds(grove_grid, dir_check_index=dir_index)
print(rounds + 10) # + 10 is from part 1
