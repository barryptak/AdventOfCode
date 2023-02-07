"""
https://adventofcode.com/2015/day/15
"""
from math import prod
from utils import read_data, extract_ints


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

ingredient_list = [extract_ints(line) for line in data]
num_ingredients = len(ingredient_list)


def gen_combo(num_values, max_value):
    """ Generator function to produce all combinations of ingredient counts """
    # We could use itertools.permutations here, but this approach is much faster
    # as we need to consider a large number of permutations
    if num_values == 1:
        yield [max_value]
    else:
        for count_1 in range(max_value + 1):
            for count_2 in gen_combo(num_values - 1, max_value - count_1):
                yield [count_1] + count_2


def get_combo_score(combo, ingredients, calorie_target=None):
    """
    Calculates the score for a given combination of ingredients.
    If calorie_target is supplied then combinations NOT meeting calorie_target
    will get a score of 0.
    """
    # Calculate the total value for each cookie property
    values = [0]*len(ingredients[0])
    for count, ingredient in zip(combo, ingredients):
        for i, prop in enumerate(ingredient):
            values[i] += prop * count

    # If we have a calorie target and don't match it then return 0 as we're
    # not interestedi in cookies that have the incorrect calorie count
    if calorie_target is not None and values[-1] != calorie_target:
        return 0

    # The final score is the product of all properties (apart from calories)
    # with any property values < 0 resulting in a zero overall
    return prod([max(0, v) for v in values[:-1]])


# Part 1
# What's the maximum score for any ingredient combination?
scores = [get_combo_score(combo, ingredient_list) for combo in gen_combo(num_ingredients, 100)]
print(max(scores))


# Part 2
# What's the maximum score for any ingredient combination that has a calorie
# count of 500?
# NOTE: We could make this all faster by running through the combos once instead of
# once per question part, but this is neater for now.
scores = [get_combo_score(combo, ingredient_list, 500) for combo in gen_combo(num_ingredients, 100)]
print(max(scores))
