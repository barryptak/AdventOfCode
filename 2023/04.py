"""
https://adventofcode.com/2023/day/4
"""

from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

total = 0
card_counts = [1]*len(data)

for card_num, line in enumerate(data):
    numbers = line.split(': ')[1].split(' | ')
    winning_numbers = [int(n) for n in numbers[0].split()]
    my_numbers = [int(n) for n in numbers[1].split()]

    # How many of my numbers match the winning numbers?
    correct_count = sum(1 for number in my_numbers if number in winning_numbers)

    # Part 1 - Add the score for this card to the total
    total += pow(2, correct_count - 1) if correct_count > 0 else 0

    # Part 2 - Increment the count of the next correct_count cards based by
    # one for every instance of the current card that we have
    # (card_counts[card_num])
    if correct_count > 0:
        for i in range(card_num + 1, card_num + correct_count + 1):
            card_counts[i] += card_counts[card_num]

print(total)
print(sum(card_counts))
