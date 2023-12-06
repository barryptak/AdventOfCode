"""
https://adventofcode.com/2017/day/13
"""
from itertools import count

from utils.data import read_data
from utils.data import extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def layer_value(layer_range, time):
    """ Returns the value of the given firewall layer at the given time """
    return time % (2 * layer_range - 2)

def layer_severity(layer_range, time):
    """ Returns the severity of the given firewall layer at the given time """
    return time * layer_range if layer_value(layer_range, time) == 0 else 0

firewall_layers = dict([extract_ints(line) for line in data])

# Part 1
# Calculate the severity of the trip through the firewall
severity = sum([layer_severity(firewall_layers[t], t) for t in firewall_layers])
print(severity)

# Part 2
# Find the delay that will allow us to pass through the firewall without being
# detected.
delay = next(delay for delay in count(1)
             if all(layer_value(firewall_layers[t], t + delay) != 0
                    for t in firewall_layers))
print(delay)
