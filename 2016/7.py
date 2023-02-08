"""
https://adventofcode.com/2016/day/7
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def is_abba(s):
    """ Does the supplied string match the ABBA pattern? """
    return s[0] == s[3] and s[1] == s[2] and s[0] != s[1]


def supports_tls(ip):
    """ Does the supplied IP string support TLS? """
    in_bracket = False
    has_abba = False
    # Iterate over the whole string looking for brackets and ABBA patterns
    for i in range(len(ip) - 3):
        # There are no nested brackets so we can just negate our 'in bracket'
        # state whenever we encounter a [ or ]
        if ip[i] in "[]":
            in_bracket = not in_bracket
        # Did we find a valid ABBA sequence?
        elif is_abba(ip[i:i+4]):
            if in_bracket:
                return False
            has_abba = True
    return has_abba


def is_aba(s):
    """ Does the suppplied string match the ABA pattern? """
    return s[0] == s[2] and s[0] != s[1]


def get_bab(aba):
    """ Returns the corresponding BAB pattern for the supplied ABA pattern """
    return aba[1] + aba[0] + aba[1]


def supports_ssl(ip):
    """ Does teh supplied IP string support SSL? """
    in_bracket = False
    outside_sequences = []
    inside_sequences = []
    # Iterate over the whole string looking for brackets and ABA patterns
    for i in range(len(ip) - 2):
        # There are no nested brackets so we can just negate our 'in bracket'
        # state whenever we encounter a [ or ]
        if ip[i] in "[]":
            in_bracket = not in_bracket
        else:
            # Did we find a valid ABA patern?
            aba = ip[i:i+3]
            if is_aba(aba):
                # Check if we already found the corresponding BAB pattern
                # inside or outside brackets (the opposite of our current
                # bracket state)
                bab = get_bab(aba)
                if in_bracket:
                    if bab in outside_sequences:
                        return True
                    inside_sequences.append(aba)
                else:
                    if bab in inside_sequences:
                        return True
                    outside_sequences.append(aba)
    return False


# Part 1
# How many IPs support TLS?
print(sum(1 for line in data if supports_tls(line)))

# Part 2
# How many IPs support SSL?
print(sum(1 for line in data if supports_ssl(line)))
