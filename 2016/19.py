"""
https://adventofcode.com/2016/day/19
"""

# Explanation:
# I figured that there must be some kind of repeating pattern here as
# simulating the entire thing step by step didn't seem overly feasible (for
# part 2 at least).
#
# So I wrote the slow iterative method and printed out the results for a
# reasonable number of elves.
#
# This let me see that pattern for part 1 where the sequence increases by 2
# for each additional elf, but resets back to one when we reach a number of
# elves that is a power of 2.
#
# Part 2 is a little more complex, but the pattern is that when we encounter a
# power of 3 then the sequence resets to 1. It them counts up in ones until it
# reaches the same value as the power of three that we reset at. Then it counts
# in twos until it reaches the next power of three and resets again.
#
# I have no idea exactly why these patterns are the case, but this is what is
# happening.


def find_previous_power(num, power):
    """
    Return the power of 'power' that is equal to or lower than num.
    e.g.
    find_previous_power(7, 2) -> 4
    find_previous_power(13, 3) -> 9
    """
    next_power = 1
    while next_power <= num:
        next_power *= power
    return next_power // power


def find_final_elf_using_next_rule(num_positions):
    """
    Determine the final elf holding all parcels when each elf steals from the
    next elf in the circle
    """
    # Find the previous power of 2 and then simply increment by 2 from there to
    # get the final elf for a circle of num_positions
    prev_power = find_previous_power(num_positions, 2)
    diff = num_positions - prev_power
    return 1 + (diff * 2)


def find_final_elf_using_opposite_rule(num_positions):
    """
    Determine the final elf holding all parcels when each elf steals from the
    elf opposite them in the circle
    """
    # Find the previous power of 3 and then figure out if we need to just
    # increment by 1 to our current number, or if we need to do that and then
    # further increment by 2 to get the final answer.
    prev_power  = find_previous_power(num_positions, 3)
    diff = num_positions - prev_power

    if diff == 0:
        return num_positions
    elif diff <= prev_power:
        return diff
    else:
        return 2*diff - prev_power


# Part 1
# What is the number of the elf holding all the parcels when they take them
# from the next elf in the circle?
print(find_final_elf_using_next_rule(3001330))

# Part 2
# What is the number of the elf holding all the parcels when they take them
# from the elf opposite them in the circle?
print(find_final_elf_using_opposite_rule(3001330))
