"""
https://adventofcode.com/2023/day/7
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

CARD_VALUES = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8,
               "7": 7,  "6": 6,  "5": 5,  "4": 4,  "3": 3,  "2": 2 }

JACKS_ARE_WILD_JACK_VALUE = 1

# Read input data in a list of hands of the form:
#([cards...], bet)
hands = [([CARD_VALUES[card] for card in hand], int(bet))
         for line in data
         for hand, bet in [line.split(" ")]]


def determine_hand_type(hand, jacks_are_wild):
    """
    Determines the type of hand and returns a score for the strength of the
    hand type.
    0 = High card
    1 = One pair
    2 = Two pair
    3 = Three of a kind
    4 = Full house
    5 = Four of a kind
    6 = Five of a kind
    """
    # If jacks are wild then just strip them out of the hand
    # The rest of the logic below works correctly for any number of cards up
    # to 5. Any missing cards are treated as wild in order to obtain the best
    # possible hand.
    if jacks_are_wild:
        hand = [card for card in hand if card != CARD_VALUES["J"]]

    hand_length = len(hand)
    unique_cards = set(hand)
    unique_count = len(unique_cards) if unique_cards else 0

    if unique_count <= 1:
        return 6 # Five of a kind
    elif unique_count == 2:
        min_count = min(hand.count(card) for card in unique_cards)
        if min_count == 2:
            return 4 # Full house
        return 5 # Four of a kind
    elif unique_count == 3:
        if hand_length <= 4:
            return 3 # Three of a kind
        max_count = max(hand.count(card) for card in unique_cards)
        if max_count == 3:
            return 3 # Three of a kind
        return 2 # Two Pair
    elif unique_count == 4:
        return 1 # One pair
    else:
        return 0 # High card


def compare_hands(left_hand, right_hand, jacks_are_wild):
    """
    Compares two hands and returns <0, 0, >0 depending on whether left < right.
    Used for sorting.
    """
    type_diff = (determine_hand_type(left_hand, jacks_are_wild) -
                 determine_hand_type(right_hand, jacks_are_wild))

    if type_diff != 0:
        return type_diff

    # If hand types match compare card by card to find the stronger hand
    # If jacks are wild then set the updated value for each jack
    if jacks_are_wild:
        left_hand = [card if card != CARD_VALUES["J"]
                        else JACKS_ARE_WILD_JACK_VALUE
                        for card in left_hand]
        right_hand = [card if card != CARD_VALUES["J"]
                        else JACKS_ARE_WILD_JACK_VALUE
                        for card in right_hand]

    # Compare the cards first to last until we find a difference
    for left_card, right_card in zip(left_hand, right_hand):
        card_diff = left_card - right_card
        if card_diff != 0:
            return card_diff

    return 0


class HandComparator:
    """
    Wrapper class to allow us to compare hands using the standard < operator
    """
    def __init__(self, hand, jacks_are_wild):
        self.hand = hand
        self.jacks_are_wild = jacks_are_wild

    def __lt__(self, other):
        return compare_hands(self.hand[0], other.hand[0], self.jacks_are_wild) < 0


def calculate_winnings(hands_of_cards, jacks_are_wild):
    """ Calculates the total winnings for the supplied hands """

    # Sort the hands by strength
    sorted_hands = sorted([HandComparator(hand, jacks_are_wild) for hand in hands_of_cards])

    # Calculate the winnings based on hand strength order * bid
    winnings = 0
    for rank, hand in enumerate(sorted_hands, 1):
        winnings += hand.hand[1]*rank

    return winnings


# Part 1
# Find the winnings for the hands
print(calculate_winnings(hands, False))

# Part 2
# Find the winnings when jacks are wild
print(calculate_winnings(hands, True))
