"""
https://adventofcode.com/2016/day/10
"""
import copy
import math
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Rather than have a separate dict/list containing the output values we can
# just treat them as bots and add an extra offset to their number to avoid
# collision with the bot numbers
OUTPUT_OFFSET = 1000


def assign_chip(chip_num, bot_num, bots):
    """ Assign this chip to this bot """
    if bot_num not in bots:
        bots[bot_num] = [chip_num]
    else:
        # If we now have two chips held by this bot sort them now so that
        # it simplifies the logic later for passing them on
        bots[bot_num] = sorted(bots[bot_num] + [chip_num])

        # Not super general, but it felt like over-engineering to pass these
        # specific test values for part 1 in as parameters.
        if bots[bot_num] == [17, 61]:
            print(bot_num)


def parse_data(input_data):
    """
    Parse the input data to determine the initial set of chips held by bots,
    and the instructions used to pass chips around
    """
    bots = {}
    instructions = {}

    for line in input_data:
        values = extract_ints(line)

        # Is this an initial assignment?
        if len(values) == 2:
            assign_chip(values[0], values[1], bots)
        # This is a bot instruction to execute once they have two chips
        else:
            parts = line.split()
            low = values[1] if parts[5] == "bot" else values[1] + OUTPUT_OFFSET
            high = values[2] if parts[10] == "bot" else values[2] + OUTPUT_OFFSET
            instructions[values[0]] = (low, high)

    return bots, instructions


def run(bots, instructions):
    """
    Run the bot chip passing logic until we've finished moving all chips around
    """
    bots_copy = copy.deepcopy(bots)

    # Pull all of the bots that we want to execute instructions on (the ones
    # holding two chips) into a separate dictionary so that we can modify
    # the main bots list as we process them
    bots_to_execute = {bot: chips for bot, chips in bots_copy.items() if len(chips) == 2}

    # Keep going where there are bots to process - we'll refill this dict at
    # end of each execution pass
    while len(bots_to_execute) > 0:
        for bot, chips in bots_to_execute.items():
            # The instruction tells us which bots to pass the low and high
            # chips to. Once we've reassigned the chips to the next bots we
            # delete the old bot from the main bot list as we won't use it
            # again.
            instruction = instructions[bot]
            assign_chip(chips[0], instruction[0], bots_copy)
            assign_chip(chips[1], instruction[1], bots_copy)
            del bots_copy[bot]

        # Pull out all of the bots who now have two chips in their possession
        bots_to_execute = {bot: chips for bot, chips in bots_copy.items() if len(chips) == 2}

    return bots_copy


bot_data, instruction_data = parse_data(data)

# Part 1
# Which bot ends up holding chips 17 & 61?
bot_data = run(bot_data, instruction_data)

# Part 2
# What's the product of the chip values in outputs 0, 1, & 2?
result = math.prod(bot_data[i][0] for i in range(OUTPUT_OFFSET, OUTPUT_OFFSET + 3))
print(result)
