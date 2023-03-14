"""
Console helpers for Advent of Code problems.
"""

import os
import platform

def clear_console():
    """ Clears the output console """
    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)
