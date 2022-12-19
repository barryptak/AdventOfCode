"""
https://adventofcode.com/2022/day/2
"""
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# region HELPFUL CONSTANTS
OPPONENT_PLAYS_ROCK = "A"
OPPONENT_PLAYS_PAPER = "B"
OPPONENT_PLAYS_SCISSORS = "C"

YOU_PLAY_ROCK = "X"
YOU_PLAY_PAPER = "Y"
YOU_PLAY_SCISSORS = "Z"

LOSE = "X"
DRAW = "Y"
WIN = "Z"

POINTS_FOR_LOSS = 0
POINTS_FOR_DRAW = 3
POINTS_FOR_WIN = 6

POINTS_FOR_ROCK = 1
POINTS_FOR_PAPER = 2
POINTS_FOR_SCISSORS = 3
# endregion

# region LOOKUP TABLES
# Look up table for points for each permutation of moves
POINTS_FOR_RESULT = {
    OPPONENT_PLAYS_ROCK: {
        YOU_PLAY_ROCK: POINTS_FOR_DRAW + POINTS_FOR_ROCK,
        YOU_PLAY_PAPER: POINTS_FOR_WIN + POINTS_FOR_PAPER,
        YOU_PLAY_SCISSORS: POINTS_FOR_LOSS + POINTS_FOR_SCISSORS
        },
    OPPONENT_PLAYS_PAPER : {
        YOU_PLAY_ROCK: POINTS_FOR_LOSS + POINTS_FOR_ROCK,
        YOU_PLAY_PAPER: POINTS_FOR_DRAW + POINTS_FOR_PAPER,
        YOU_PLAY_SCISSORS: POINTS_FOR_WIN + POINTS_FOR_SCISSORS
        },
    OPPONENT_PLAYS_SCISSORS : {
        YOU_PLAY_ROCK: POINTS_FOR_WIN + POINTS_FOR_ROCK,
        YOU_PLAY_PAPER: POINTS_FOR_LOSS + POINTS_FOR_PAPER,
        YOU_PLAY_SCISSORS: POINTS_FOR_DRAW + POINTS_FOR_SCISSORS
        }
    }

# Look up table for part two that determines the move to make based on 
# the opponent's move and the outcome we want
MOVE_TO_MAKE = {
    OPPONENT_PLAYS_ROCK: {
        LOSE: YOU_PLAY_SCISSORS,
        DRAW: YOU_PLAY_ROCK,
        WIN: YOU_PLAY_PAPER
    }, 
    OPPONENT_PLAYS_PAPER: {
        LOSE: YOU_PLAY_ROCK,
        DRAW: YOU_PLAY_PAPER,
        WIN: YOU_PLAY_SCISSORS
    }, 
    OPPONENT_PLAYS_SCISSORS: {
        LOSE: YOU_PLAY_PAPER,
        DRAW: YOU_PLAY_SCISSORS,
        WIN: YOU_PLAY_ROCK
    }
}
# endregion

part1_points = 0
part2_points = 0

for line in data:
    opponent_move, my_move = line.split(" ")

    # Get the points for the moves indicated in the input data
    part1_points += POINTS_FOR_RESULT[opponent_move][my_move]

    # For part 2 we need to determine the move to make based on the outcome we want 
    # so look that actual move up first and then get the points for making it.
    move_to_make = MOVE_TO_MAKE[opponent_move][my_move]
    part2_points += POINTS_FOR_RESULT[opponent_move][move_to_make]

print(part1_points)
print(part2_points)