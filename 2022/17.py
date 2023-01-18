"""
https://adventofcode.com/2022/day/17
"""
import copy
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False

# Read in our data as ints indicating the amount to move left or right
jets = [-1 if j == "<" else 1 for j in read_data(USE_TEST_DATA, SPLIT_BY_LINE)]

# Rock patterns. Note that within each rock pattern that they're upside down.
# row 0 is the lowest, row 1 is one higher, etc.
# Using bits to represent rock positions. That we can we can simply perform a
# bitwise AND with the chamber state to check for collisions, and a bitwise OR
# with the chamber state to settle a rock in position.
rocks = [
    [
        int("000111100", 2)
    ],
    [
        int("000010000", 2),
        int("000111000", 2),
        int("000010000", 2)
     ],
     [
        int("000111000", 2),
        int("000001000", 2),
        int("000001000", 2)
     ],
     [
        int("000100000", 2),
        int("000100000", 2),
        int("000100000", 2),
        int("000100000", 2)
     ],
     [
        int("000110000", 2),
        int("000110000", 2)
     ]
]

# Bit representation of a row in the chamber when empty or full. The lsb and
# msb are the walls.
# We include these in the chamber and rock representations to allow easy
# detection of a rock shifting sideways into the chamber walls via bitwise AND 
EMPTY_CHAMBER_ROW = int("100000001", 2)
FULL_CHAMBER_ROW  = int("111111111", 2)

def is_collision(chamber, rock, y, height_of_rock_stack):
    """
    Determines if the supplied rock at height y is in collision with any of the
    previously settled rocks or the chamber floor
    """
    # Have we hit the floor?
    if y <= 0:
        return True

    # No collisions if we're above the top of the existing stack
    if y > height_of_rock_stack:
        return False

    # Iterate over each row of the rock (row 0 is at the BOTTOM of the rock
    # and we move upwards as we increase ry)
    for d_y, rock_row in enumerate(rock):
        chamber_y = y + d_y

        # If the chamber y value is not stored then we know that there are no
        # rocks to collide with at this height
        # We don't have to worry about the sides of the chamber here as we
        # perform that test in shift_rock first
        if chamber_y not in chamber:
            continue

        # Collision check is as simple bitwise AND
        if rock_row & chamber[chamber_y]:
            return True

    return False

def place_rock(chamber, rock, y, height_of_rock_stack):
    """
    Places/settles the supplied rock at the y height given.
    Returns the new height of the stacked rocks.
    """

    # Iterate over each row of the rock (row 0 is at the BOTTOM of the rock
    # and we move upwards as we increase ry)
    for d_y, rock_row in enumerate(rock):

        # Get the current state of the chamber at the current y position
        chamber_y = y + d_y
        if chamber_y not in chamber:
            chamber[chamber_y] = EMPTY_CHAMBER_ROW

        # To settle the rock we simply bitwise OR the chamber and rock states!
        chamber[chamber_y] |= rock_row

        # Memory optimisation - if the current row is full then we can throw
        # away all of the rows lower than it as we'll never be able to collide
        # with them.
        if chamber[chamber_y] == FULL_CHAMBER_ROW:
            for c_y in range(chamber_y):
                if c_y in chamber:
                    del chamber[c_y]

    # Return the new height of the stack of rocks
    return max(height_of_rock_stack, y + len(rock) - 1)


def shift_rock(rock, move):
    """
    Moves the supplied rock left or right and clamps it to the chamber walls.
    This function does NOT check for collisions with already settled rocks.
    """
    moved_rock = copy.deepcopy(rock)

    # Are we moving the rock left or right?
    if move == -1:
        # Iterate over the rows of the rock pattern
        for d_y, rock_row in enumerate(moved_rock):
            # Shift the bitwise representation of the rock left
            rock_row <<= 1

            # Check if we've collided with the walls of the chamber.
            # If we have then return the original position of the rock.
            if rock_row & EMPTY_CHAMBER_ROW:
                return rock

            # Update the new position of this row of the rock
            moved_rock[d_y] = rock_row
    else:
        # Same as above, but we shift right instead
        for d_y, rock_row in enumerate(moved_rock):
            rock_row >>= 1
            if rock_row & EMPTY_CHAMBER_ROW:
                return rock
            moved_rock[d_y] = rock_row

    return moved_rock


def get_chamber_state(rock_id, jet_id, chamber, height):
    """
    Creates a hashable representation of the current state of the chamber.
    We take the current rock and jet ids and the top 20 rows of settled rocks
    and put them into a tuple that we can use for a cache lookup.
    """

    state = [rock_id, jet_id]

    for chamber_y in range(height - 20, height + 1):
        row = chamber[chamber_y] if chamber_y in chamber else EMPTY_CHAMBER_ROW
        state.append(row)

    return tuple(state)


def simulate_rockfall(rock_count):
    """
    Simulates the falling of rock_count rocks and returns the final height
    of the stacked rocks.
    """
    chamber = {}
    height = 0

    rock_id = 0
    jet_id = 0
    count = 0

    states = {}
    repeated_height = 0

    while count < rock_count:

        # Start a new rock falling above the top of the stack
        rock = copy.deepcopy(rocks[rock_id])
        rock_y = height + 4
        rock_falling = True

        while rock_falling:
            # Move the rock sideways based on the jet of air, clamping it
            # within the chamber walls
            moved_rock = shift_rock(rock, jets[jet_id])

            # If we collide sideways then don't apply the move
            if not is_collision(chamber, moved_rock, rock_y, height):
                rock = moved_rock

            # Move from gravity
            if not is_collision(chamber, rock, rock_y - 1, height):
                # No collision, move the rock down
                rock_y -= 1
            else:
                # Rock has collided with something below it and is settled.
                # Don't simulate it anymore.
                height = place_rock(chamber, rock, rock_y, height)
                rock_falling = False
                count += 1

                # Let's see if we can find a repeating pattern
                # Take the current rock and jet ids plus the top n rows of
                # rocks and generate a hashable state value that we can use
                # to check to see if we've encountered this state before and
                # just look up the result rather than recalculating the whole
                # thing again!
                chamber_state = get_chamber_state(rock_id, jet_id, chamber, height)
                if chamber_state in states:
                    # We found a repeat!!!

                    # Pull out the rock count and height from the cached state
                    # and calculate the difference between now and then
                    prev_count, prev_height = states[chamber_state]
                    height_diff = height - prev_height
                    count_diff = count - prev_count

                    # Calculate how many times we can repeat this pattern
                    # without going past the target number of rocks to drop.
                    # The integer divide ensures that we will always hit the
                    # target rock count or under.
                    repeats = (rock_count - count) // count_diff

                    # Add on how many rocks and how much height we acumulate by
                    # repeating the pattern repeats times
                    count_to_add = count_diff * repeats
                    height_to_add = height_diff * repeats
                    count += count_to_add
                    # We could add to height here, but that would mean needing
                    # to update the entries in chamber accordingly too, so
                    # instead we can just continue where we are and remember
                    # the repeated amount of height and add it right at the end
                    repeated_height += height_to_add
                else:
                    # Haven't seen this state before, store it in case we
                    # encounter it again
                    states[chamber_state] = (count, height)

            jet_id = (jet_id + 1) % len(jets)
        rock_id = (rock_id + 1) % len(rocks)

    return height + repeated_height

print(simulate_rockfall(2022))
print(simulate_rockfall(1000000000000))
