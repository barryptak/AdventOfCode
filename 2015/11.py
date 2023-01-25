"""
https://adventofcode.com/2015/day/11
"""

# Note that I've optimised this solution by having it use a list of ordinal
# values for all operations rather than the actual password string.
# This saves conversion back and forth and messing around with temp strings.

ORD_A = ord("a")
ORD_Z = ord("z")
BAD_ORDS = (ord("i"), ord("l"), ord("o"))


def string_to_ord_list(string_in):
    """ Convert a string into a list of ordinal values """
    return [ord(c) for c in string_in]


def ord_list_to_string(ords_in):
    """ Convert a list of ordinal values into a string """
    return "".join((chr(o) for o in ords_in))


def get_next_candidate_password(password):
    """
    Produce the next candidate iteration for a password by incrementing it by
    one.
    Accounts for the no i,l,o rule, but does not account for the rules about
    strights and character pairs.
    """
    output_password = []
    carry = 1
    prefix = [ORD_A]

    # Iterate over the pasword backwards so that we start at the lsb
    for char in password[::-1]:
        char += carry

        # If we would overflow this character then set it to 'a' and set the
        # carry bit to 1
        if char > ORD_Z:
            output_password.append(ORD_A)
            carry = 1
        # No overflow - set the character to char unless that's one of the bad
        # chars (i,l,o) in which case set it to char + 1.
        # Reset the carry bit since there's no oveflow.
        # Also clear the prefix since there's no overflow from the msb.
        else:
            output_password.append(char if char not in BAD_ORDS else char + 1)
            carry = 0
            prefix = []
            break

    # The final password is:
    # prefix (to account for any overflow from the old msb)
    # + the untouched msbs from the original password
    # + the modified lsbs in output_password (which we need to reverse as we
    # appended to it in lsb->msb order)
    return prefix + password[:-len(output_password)] + output_password[::-1]


def contains_straight(string):
    """
    Does this string contain a straight run of 3 or more consecutive
    characters?
    e.g. abc -> True, abbc -> False
    """
    return any((x == y - 1 == z - 2 for x, y, z in zip(string, string[1:], string[2:])))


def contains_two_pairs(string):
    """
    Does this string contain at least two different pairs of consecutive characters?
    e.g. aabb -> True, aabaa -> False
    """
    return len({x for x, y in zip(string, string[1:]) if x == y}) > 1


def get_next_valid_password(password):
    """ Gets the next valid password from the one provided """
    password = get_next_candidate_password(password)
    while not contains_straight(password) or not contains_two_pairs(password):
        password = get_next_candidate_password(password)
    return password


# Part 1
# Next valid password after vzbxkghb
next_password = get_next_valid_password(string_to_ord_list("vzbxkghb"))
print(ord_list_to_string(next_password))


# Part 2
# Next valid password after the one above
next_password = get_next_valid_password(next_password)
print(ord_list_to_string(next_password))
