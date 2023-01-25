"""
https://adventofcode.com/2015/day/14
"""
from utils import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

RACE_TIME = 2503
reindeer = [extract_ints(line) for line in data]

def calculate_distance(speed, fly, rest, total_time):
    """
    Calculate the distance covered by a reindeer given their max speed,
    flying time, resting time, and the total time available.
    """
    # Determine how many complete combined flying and resting periods the
    # reindeer has completed. Then determine if the remaining time left them
    # still flying or not and calculate the total distance travelled all
    # together.
    steps, time = divmod(total_time, rest + fly)
    return (speed * fly * steps) + (min(time, fly) * speed)


# Part 1
# How far has the winning reindeer travelled after 2503 seconds?
best_distance = max((calculate_distance(speed, fly, rest, RACE_TIME))
                    for speed, fly, rest in reindeer)
print(best_distance)


# Part 2
# What's the score of the winning reindeer using the new scoring system?
scores = [0]*len(reindeer)
for t in range(1, RACE_TIME + 1):
    dists = [calculate_distance(speed, fly, rest, t) for speed, fly, rest in reindeer]
    max_dist = max(dists)
    scores = [s + 1 if d == max_dist else s for s, d in zip(scores, dists)]

print(max(scores))
