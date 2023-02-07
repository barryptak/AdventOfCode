"""
https://adventofcode.com/2015/day/20
"""
import functools
import math


@functools.cache
def get_divisors(num):
    """ Return a list of all of the divisors of the supplied number """
    divisors = set()
    for i in range(1, round(math.sqrt(num) + 1)):
        div, mod = divmod(num, i)
        if mod == 0:
            divisors.add(i)
            divisors.add(div)

    return divisors

       
@functools.cache
def num_presents(house_num, presents_per_elf, max_visits_per_elf=math.inf):
    """ Return the number of presents delivered to a given house number """
    divisors = [d for d in get_divisors(house_num) if house_num // d <= max_visits_per_elf]
    return sum(divisors) * presents_per_elf


@functools.cache
def max_possible_presents(house_num, presents_per_elf, max_visits_per_elf=math.inf):
    """
    Return the absolute upper bound count of presents that could be delivered
    to a given house number
    """
    presents = 0
    div = 1
    while div <= house_num and div <= max_visits_per_elf:
        presents += house_num // div
        div += 1
    return presents * presents_per_elf


def find_first_house_to_reach_target(target_presents, presents_per_elf, max_visits_per_elf=math.inf):
    """
    Find the number of the first house to reach target_presents presents
    """
    # Find a very rough starting point so that we don't have to start from
    # house number 1.
    step = 10_000
    num = step + 1
    max_presents = 0
    while max_presents < target_presents:
        max_presents = max_possible_presents(num, presents_per_elf, max_visits_per_elf)
        num += step

    # When we're here then num - step gives us a starting point that we *know*
    # will not be past the first hour to reach target_presents.
    # It's probably *well* before it, but it's better than starting the full
    # search from 1.
    num -= step

    # The number of presents that a house gets is highly dependent on the
    # number of divisors that it has. Prime numbered houses have a relatively
    # low present count as they only have two divisors.
    # The houses the have the greatest relative present count are going to be
    # those whose number divides a lot. It's highly likely that for large
    # target numbers that the first house to reach it will be one whose number
    # divides by 2,3,4,6,8,12, etc...
    # So, to make things faster we can step by 12 rather than 1 for large
    # tagets.
    # THIS IS LIKELY NOT A COMPLETELY GENERAL SOLUTION! Force step to 1 for a
    # guaranteed correct solution.
    step = 12 if target_presents > 1_000_000 else 1
    num = (num // 12) * 12
    while True:
        presents = num_presents(num, presents_per_elf, max_visits_per_elf)
        if presents >= target_presents:
            return num
        num += step


TARGET = 29_000_000

# Part 1
# Find the first house to reach 29000000 presents
print(find_first_house_to_reach_target(TARGET, 10))


# Part 2
# Find the first houes to reach 29000000 presents with new elf rules
print(find_first_house_to_reach_target(TARGET, 11, 50))
