"""
https://adventofcode.com/2015/day/22
"""

import copy
import math
from utils.data import add_tuples

#region CONSTANTS

ENEMY = (59, 9, 0) # hit points, damage, armour
PLAYER = (50, 0, 500) # hit points, armour, mana

HIT_POINTS_INDEX = 0
DAMAGE_INDEX = 1
ARMOUR_INDEX = 1
MANA_INDEX = 2

COST = [53, 73, 113, 173, 229]
INSTANT_DAMAGE = [4, 2, 0, 0, 0]
INSTANT_HEAL = [0, 2, 0, 0, 0]
EFFECT_ARMOUR = [0, 0, 7, 0, 0]
EFFECT_DAMAGE = [0, 0, 0, 3, 0]
EFFECT_MANA = [0, 0, 0, 0, 101]
EFFECT_DURATION = [0, 0, 6, 6, 5]
NUM_SPELLS = len(COST)

EFFECTS = [0]*NUM_SPELLS

#endregion


#region Optimisation Helpers

# We can store the lowest successful mana cost so far so that we don't go bother
# to explore further combinations of spells that are already more expensive
# than this.
global_low = math.inf

def get_global_low():
    """ Returns the current lowest successful mana cost """
    return global_low


def set_global_low(low):
    """ Sets a new current lowest successful mana cost """
    global global_low
    global_low = low

# A set of states that we have already evaluated.
# We're going to encounter the same state (player stats, enemy stats, and
# active spells) more than once, so rather than evaluate them again we can
# just skip the ones that we've already seen (as we'd just get the same
# answer again anyway).
visited = set()

#endregion


def apply_effects(player, enemy, active_effects):
    """ Apply any active spell effects to the player and enemy """
    armour_boost = 0
    damage = 0
    mana = 0

    for i, effect in enumerate(active_effects):
        if effect >= 1:
            active_effects[i] -= 1
            armour_boost += EFFECT_ARMOUR[i]
            damage += EFFECT_DAMAGE[i]
            mana += EFFECT_MANA[i]

    enemy = add_tuples(enemy, (-min(damage, enemy[HIT_POINTS_INDEX]), 0, 0))

    # NOTE: If you are getting 1235 as your result and you can't figure out why,
    # it's because you're adding 7 armour every turn that the shield spell is
    # active. The spell is only supposed to boost the player's armour by 7 for
    # the current turn. Not accumulate 7 each turn. This is not overly clear
    # in the wording of the puzzle!
    # Here I return the amount of armour boost rather than adjusting the
    # player's armour stat (as that would be more awkward to handle).
    player = add_tuples(player, (0, 0, mana))

    return player, enemy, armour_boost


def fight(player_state, enemy_state, effects_state, mana_used, part2):
    """
    Simulates the fight between the player and the enemy and returns the least
    amount of mana that can be spent and still win the fight
    """

    # Check if we've already seen this state before. If we have then there' no
    # point simulating it again as the result will be the same.
    state = (player_state, enemy_state, tuple(effects_state), mana_used, part2)
    if state in visited:
        return math.inf
    visited.add(state)

    # If the mana used to get here is equal or higher to the lowest we've seen
    # so far then don't bother going any further as this won't give us a better
    # result.
    if mana_used >= get_global_low():
        return math.inf

    lowest_mana_used_to_win = math.inf

    ####
    # Player turn
    ####

    # Go through each spell available
    for i in range(NUM_SPELLS):
        player = player_state
        enemy = enemy_state
        active_effects = copy.deepcopy(effects_state)

        # If the player does not have enough mana to cast a spell OR the cost
        # of casting this spell takes us above the lowest winning mana that
        # we've already seen then don't bother continuing.
        mana_cost = COST[i]
        if mana_cost > player[MANA_INDEX] or ((mana_used + mana_cost) >= lowest_mana_used_to_win):
            continue

        # If this spell is currently active with time left > 1 then continue as
        # we're not allowed to cast a spell that's currently still active.
        if active_effects[i] > 1:
            continue

        # If this is part two of the puzzle then remove one hit point from the
        # player
        if part2:
            player = add_tuples(player, (-1, 0, 0))
            if player[HIT_POINTS_INDEX] <= 0:
                continue

        # Apply any active spell effects
        player, enemy, _ = apply_effects(player, enemy, active_effects)

        # Did the enemy die?
        if enemy[HIT_POINTS_INDEX] <= 0:
            #print(f"Player wins using {mana_used} mana")
            lowest_mana_used_to_win = min(lowest_mana_used_to_win, mana_used)
            if lowest_mana_used_to_win < get_global_low():
                set_global_low(lowest_mana_used_to_win)
            return lowest_mana_used_to_win

        # Cast the new spell at this point
        # Apply instant effects and deduct cost of spell
        enemy = add_tuples(enemy, (-INSTANT_DAMAGE[i], 0, 0))
        player = add_tuples(player, (INSTANT_HEAL[i], 0, -mana_cost))
        new_mana_used = mana_used + mana_cost

        # Set new durations if needed - at least one side of these is going to be 0
        active_effects[i] += EFFECT_DURATION[i]

        # Did the enemy die after casting the spell?
        if enemy[HIT_POINTS_INDEX] <= 0:
            lowest_mana_used_to_win = min(lowest_mana_used_to_win, new_mana_used)
            if lowest_mana_used_to_win < get_global_low():
                set_global_low(lowest_mana_used_to_win)
            continue

        ####
        # Enemy turn
        ####

        # Apply active spell effects
        player, enemy, armour_boost = apply_effects(player, enemy, active_effects)

        # Did the enemy die?
        if enemy[HIT_POINTS_INDEX] <= 0:
            lowest_mana_used_to_win = min(lowest_mana_used_to_win, new_mana_used)
            if lowest_mana_used_to_win < get_global_low():
                set_global_low(lowest_mana_used_to_win)
            continue

        # Apply result of the enemy's attack
        damage = max(enemy[DAMAGE_INDEX] - (player[ARMOUR_INDEX] + armour_boost), 1)
        player = add_tuples(player, (-damage, 0, 0))

        # Did the player die?
        if player[HIT_POINTS_INDEX] <= 0:
            continue

        # Neither the player or the enemy won in this round - go for another round
        lowest_win_cost = fight(player, enemy, active_effects, new_mana_used, part2)
        lowest_mana_used_to_win = min(lowest_mana_used_to_win, lowest_win_cost)

    return lowest_mana_used_to_win

# Part 1
# What's the least amount of mana we can spend to win the fight?
print(fight(PLAYER, ENEMY, EFFECTS, 0, False))

# Part 2
# What's the lowest cost if the player loses 1 HP at the start of each of their turns?
# Don't forget to reset the global low mana value for this pass through.
set_global_low(math.inf)
print(fight(PLAYER, ENEMY, EFFECTS, 0, True))
