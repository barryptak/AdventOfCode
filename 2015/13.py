"""
https://adventofcode.com/2015/day/13
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

MUL = {"gain": 1, "lose": -1}


def parse_people(data_in):
    """
    Parse the input data into a dictionary of people and happiness weights
    """
    happiness = {}
    for line in data_in:
        parts = line.split()
        person1 = parts[0]
        person2 = parts[10][:-1]

        if person1 not in happiness:
            happiness[person1] = {}

        happiness[person1][person2] = int(parts[3]) * MUL[parts[2]]

    return happiness


def all_orders(starting_person, other_people):
    """
    Generator function returning all permutations of seating orders
    """
    for person in other_people:
        for child_order in all_orders(person, other_people - {person}):
            yield [starting_person] + child_order

    if len(other_people) == 0:
        yield [starting_person]


def score_order(order, happiness):
    """
    Calculate the overall happiness score for the supplied seating order
    """
    score = 0

    # Iterate through all people in the order from first to second last
    # (as we need to special-case the index lookups for the last person)
    for i, person in enumerate(order[:-1]):
        score += happiness[person][order[i-1]]
        score += happiness[person][order[i+1]]

    # Don't forget to account for the last person in the order who needs to
    # consider the first person too.        
    score += happiness[order[-1]][order[0]]
    score += happiness[order[-1]][order[-2]]

    return score


def add_me(happiness):
    """ Add entries for me to the happiness weights """
    for k in happiness.keys():
        happiness[k]["me"] = 0
    happiness["me"] = {k: 0 for k in happiness.keys()}


# Read in the data and pick someone to be the starting person in our seating
# order. It doesn't matter who.
weights = parse_people(data)
start = next(iter(weights.keys()))


# Part 1
# What is the greatest overall happiness score that we can achieve by ordering
# the dinner guests appropriately?
best_score = max((score_order(order, weights) 
                  for order in all_orders(start, weights.keys() - {start})))
print(best_score)


# Part 2
# What is the greatest overall happiness score that we can achieve when I also
# attend?
add_me(weights)
best_score = max((score_order(order, weights) 
                  for order in all_orders(start, weights.keys() - {start})))
print(best_score)
