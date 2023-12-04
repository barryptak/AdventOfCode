"""
https://adventofcode.com/2023/day/2
"""

from utils.data import read_data
from functools import reduce
from operator import mul

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

possible_games_sum = 0
power_sum = 0
MAX_DICE_LIMITS = {"red": 12, "green": 13, "blue": 14}

for game_id, line in enumerate(data, 1):
    # Get the list of the dice pulls from the input
    dice_pulls = line.split(": ")[1]

    # Iterate through each individual pull and store the maximum number of
    # each colour ever seen at one time.
    max_dice_counts = {}
    for dice_pull in dice_pulls.split("; "):
        for colour_and_count in dice_pull.split(", "):
            count, colour = colour_and_count.split(" ")
            max_dice_counts[colour] = max(max_dice_counts.get(colour, 0), int(count))

    # Part 1 - Add together the IDs of the possible games.
    # A game is only possible if we didn't see more than the maximum number of
    # dice for each colour at any one time.
    if all(count <= MAX_DICE_LIMITS[colour] for colour, count in max_dice_counts.items()):
        possible_games_sum += game_id

    # Part 2 - Multiply together the minimum number of dice for each colour it's
    # possible for the bag to hold.
    power_sum += reduce(mul, max_dice_counts.values(), 1)

print(possible_games_sum)
print(power_sum)