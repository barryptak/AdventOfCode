"""
https://adventofcode.com/2015/day/19
"""
import re
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

replacement_pairs = [tuple(line.split(" => ")) for line in data[:-2]]
target_molecule = data[-1]

# Part 1
# How many different molecules can be made by making a single replacement to
# the starting molecule?

def create_replacement_molecules(molecule, replacements):
    """
    Create a set of the molecules that can be generated by making a single
    replacement to the input molecule
    """
    molecules = set()
    for source, destination in replacements:
        for match in re.finditer(source, molecule):
            molecule = molecule[:match.start()] + destination + molecule[match.end():]
            molecules.add(molecule)
    return molecules

print(len(create_replacement_molecules(target_molecule, replacement_pairs)))

# Part 2
# What is the minimum number of replacements it takes to go from "e" to our
# target molecule?

# Trying to go from "e" -> target_molecule will produce too many permutations.
# Instead let's go backwards from target_molecule to "e" as there will be
# fewer possible steps to try.
#
# Observe that:
# All molecules can be transformed apart from Ar, Rn & Y
# All substitutions are of the form:
# mol1 => mol2.mol3
# mol1 => mol2.Rn.mol3.Ar
# mol1 => mol2.Rn.mol3.Y.mol4.Ar
# mol1 => mol2.Rn.mol3.Y.mol4.Y.mol5.Ar
# Rn is always in a fixed position in these patterns too.
#
# Because Ar, Y & Rn are 'terminal' molecules (we cannot transform further from
# them) then we can assume that the first thing we want to do is to remove all
# of these in as few steps as possible.
#
# Realising that we don't need to worry about which molecules we're
# transforming to outside of meeting the above patterns containing Rn, Y & Ar
# (as we are presuming that all other individual atoms are easy to transform
# to) then we can substitute them all for the same character to make things
# easier and not have to worry about getting the exact permutation of
# transforms correct.
mol = target_molecule
for r in replacement_pairs:
    # o == one atom. I was going to use . but that would need to be escaped...
    mol = mol.replace(r[0], "o")
mol = mol.replace("C", "o") # Don't forget C :/

# Our replacements now become:
reps = [("o", "oRnoYoYoAr"),
        ("o", "oRnoYoAr"),
        ("o", "oRnoAr"),
        ("o", "oo")]

# Loop around making (reversed) replacements until we reach a single atom
# (which will be "e")
# As mentioned above, we are making the assumption that any transform not
# involving Ar, Y or Rn is trivial to make and that we don't need to make
# complicated jumps to get there.
steps = 0
while mol != "o":
    for dest, src in reps:
        mol, count = re.subn(src, dest, mol)
        steps += count

print(steps)
