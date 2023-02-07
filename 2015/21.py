"""
https://adventofcode.com/2015/day/21
"""
from functools import cache, reduce
from itertools import combinations, product
from math import ceil
from utils import add_tuples


#region Constants

# Weapons values are (cost, damage, armour)
WEAPONS = [(8, 4, 0),
           (10, 5, 0),
           (25, 6, 0),
           (40, 7, 0),
           (74, 8, 0)]

# Armour values are (cost, damage, armour)
ARMOUR = [(0, 0, 0),
          (13, 0, 1),
          (31, 0, 2),
          (53, 0, 3),
          (75, 0, 4),
          (102, 0, 5)]

# Ring values are (cost, damage, armour)
RINGS = [(0, 0, 0),
         (0, 0, 0),
         (25, 1, 0),
         (50, 2, 0),
         (100, 3, 0),
         (20, 0, 1),
         (40, 0, 2),
         (80, 0, 3)]

# Enemy values are (hit points, damage, armour)
ENEMY = (104, 8, 1)

PLAYER_HIT_POINTS = 100

COST_INDEX = 0
HIT_POINTS_INDEX = 0
DAMAGE_INDEX = 1
ARMOUR_INDEX = 2

#endregion


def fight(player, enemy):
    """
    Calculates the outcome of a fight between player and enemy
    Returns True if player wins, returns False if enemy wins
    """
    # Figure out the number of rounds it takes for the player and the enemy to
    # die. If they die on the same round then the player wins as they get to
    # attack first.
    damage_dealt_by_player = max(player[DAMAGE_INDEX] - enemy[ARMOUR_INDEX], 1)
    rounds_to_kill_enemy = ceil(enemy[HIT_POINTS_INDEX] / damage_dealt_by_player)
    damage_dealt_by_enemy = max(enemy[DAMAGE_INDEX] - player[ARMOUR_INDEX], 1)
    rounds_to_kill_player = ceil(player[HIT_POINTS_INDEX] / damage_dealt_by_enemy)
    return rounds_to_kill_enemy <= rounds_to_kill_player


@cache
def equipment_combinations():
    """ Returns a set of all possible equipment combinations """
    # Add together all of the tuples representing the (cost, damage, armour)
    # for each combination of weapon, armour, and rings (this gives us a single
    # tuple per combination containing the combined values for each field) and
    # add them to a set so that we only have unique combinations.
    return {reduce(add_tuples, [weapon, armour, rings[COST_INDEX], rings[DAMAGE_INDEX]], (0, 0, 0))
              for weapon, armour, rings in product(WEAPONS, ARMOUR, combinations(RINGS, 2))}


def find_cost(win):
    """
    Finds the lowest cost to win (True passed in) or the highest cost to lose
    (False passed in) and returns that cost
    """
    # Generate all combinations of items and sort by cost
    combos = sorted(list(equipment_combinations()), key = lambda x: x[0], reverse = not win)
    # Iterate through all of the ordered combos until we find one that meets
    # out criteria of either winning or losing the fight. Print out the cost
    # of that first combo.
    for combo in combos:
        player = (PLAYER_HIT_POINTS, combo[DAMAGE_INDEX], combo[ARMOUR_INDEX])
        if fight(player, ENEMY) == win:
            return combo[COST_INDEX]

# Part 1
# Find the lowest amount of gold we can spend and win the fight
print(find_cost(True))


# Part 1
# Find the most amount of gold we can spend and lose the fight
print(find_cost(False))
