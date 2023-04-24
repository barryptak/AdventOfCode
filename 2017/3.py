"""
https://adventofcode.com/2017/day/3
"""
from collections import defaultdict
from utils.point2d import Point2D

# This seems like a lot of code, but it's mostly me trying to be a smartarse
# and do part 1 in (almost) constant time.

def next_odd_square(num):
    """
    Return the next odd square number equal to or greater than num.
    This is useful because the last number in each ring/layer of the sequence
    for part 1 is an odd square (1, 9, 25, etc..).
    """
    sqrt = int(num ** 0.5)
    if sqrt % 2 == 0:
        sqrt += 1
    return sqrt**2


def get_layer(num):
    """
    Which 'layer' of the spiral pattern is the given number on?
    The first number (1) is on layer 0, next ring (2->9) is layer 1.
    """
    sqrt = int(num ** 0.5)
    return sqrt // 2


def get_steps_to_access_port(num):
    """
    Returns how many steps it takes to move the specified number from its
    initial position to the access port at 0, 0.
    Steps is the Manhattan Distance from the starting position to 0, 0.
    We could brute force this entire thing and just walk the spiral from 1 to
    num, but this is a faster solution for large numbers.
    """
    # Determine the layer of this number, and from that the minimum and maximum
    # possible steps from a number in the layer to the access port / origin.
    # e.g. in layer 1, you can be at min 1 step away, and at max 2 steps.
    #      in layer 2, you can be between 2 and 4 steps away.
    #      etc...
    layer_num = get_layer(num)
    min_steps = layer_num
    max_steps = layer_num*2

    steps = max_steps
    direction = -1

    # The largest number on any layer is in the bottom right corner and is an
    # odd square (e.g. 1, 9, 25, etc..).
    # How far our number is from the next odd square tells us how many steps
    # we have to walk clockwise around the spiral to get from the bottom right
    # of the layer to our number.
    # As we walk around the spiral from the bottom right to our number we move
    # first closer to the access port (moving left from bottom right towards
    # bottom centre) and then further away (moving left from bottom centre to
    # bottom left). The same pattern of getting closer and then further away
    # from the access port repeats along each side until we reach our
    # number. By taking account of whether we're moving a step closer to the
    # access port, or a step further away, as we move around the spiral, we
    # can figure out the final distance of our number from the access port.
    for _ in reversed(range(num, next_odd_square(num))):
        steps += direction
        if steps == min_steps or steps == max_steps:
            direction *= -1

    return steps


def get_next_position():
    """
    Generator function to return the next position in the spiral sequence.
    """
    pos = Point2D(0, 0)
    direction = Point2D(1, 0)

    # Always start at 0, 0
    yield pos

    while True:
        # Should we start the next layer?
        if pos.x >= 0 and pos.x == pos.y:
            pos += Point2D(1, 0)
            direction = Point2D(0, -1)
        else:
            # Should we start moving left?
            if pos.x > 0 and pos.x == -pos.y:
                direction = Point2D(-1, 0)
            # Should we start moving down?
            elif pos.x < 0 and pos.x == pos.y:
                direction = Point2D(0, 1)
            # Should we start moving right?
            elif pos.x < 0 and pos.x == -pos.y:
                direction = Point2D(1, 0)

            pos += direction
        yield pos


def get_first_stress_num_greater_than(target):
    """
    Returns the first number produced in the stress test pattern that is
    greater than the target number.
    """
    nums = defaultdict(int)
    nums[Point2D(0, 0)] = 1

    OFFSETS = (Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1),
            Point2D(-1, 0), Point2D(1, 0),
            Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1))

    # Walk round the spiral and add the values of the surrounding positions
    # to determine the value of the current position.
    for p in get_next_position():
        nums[p] = max(1, sum(nums[p + o] for o in OFFSETS))
        if nums[p] > target:
            return nums[p]


# Part 1
# How many steps does it take to move the number 312051 to the data port at
# the first position?
print(get_steps_to_access_port(312051))

# Part 2
# Using the stress pattern what's the first number generated that's greater
# than 312051?
print(get_first_stress_num_greater_than(312051))
