"""
https://adventofcode.com/2022/day/4
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def section_is_contained(subsection, supersection):
    """
    Returns whether subsection is entirely contained within supersection
    """
    return subsection[0] >= supersection[0] and subsection[1] <= supersection[1]


def sections_contained(section1, section2):
    """
    Returns whether the either supplied section is entirely contained within
    the other
    """
    return section_is_contained(section1, section2) or section_is_contained(section2, section1)


def sections_overlap(section1, section2):
    """
    Returns whether the supplied sections overlap at all
    """
    return section1[0] <= section2[1] and section1[1] >= section2[0]


contained_count = 0
overlapped_count = 0
for line in data:
    # Convert the string input ("A-B,C-D") into a list of int pairs (in a list):
    # [[A,B], [C,D]]
    sections = [list(map(int, section.split("-"))) for section in line.split(",")]

    if sections_overlap(sections[0], sections[1]):
        overlapped_count += 1
        # If the sections don't overlap then they can't contain each other
        # either so we can do this test inside the overlap True case
        if sections_contained(sections[0], sections[1]):
            contained_count += 1

print(contained_count)
print(overlapped_count)
