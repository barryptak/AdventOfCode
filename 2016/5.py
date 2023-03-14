"""
https://adventofcode.com/2016/day/5
"""
import hashlib
import random
from timeit import default_timer as timer
from utils.console import clear_console

ENCRYPTED_CHARS = "abcdefghijklmnopqrtsuvwxyz0123456789?!#$%^&*@"


def print_password(password_list):
    """
    Prints out the supplied password substituting any unknown characters for
    cool hacker style characters 🐱‍💻
    """
    password = [c if c != "_" else random.choice(ENCRYPTED_CHARS) for c in password_list]
    print("".join(password))


def print_passwords(title, pass1, pass2):
    """ Clears the console and prints the current passwords """
    clear_console()
    print(title)
    print_password(pass1)
    print_password(pass2)


def decrypt_passwords(door_id):
    """ Decrypt the two passwords for the specified door """
    index = 0
    password1 = ["_", "_", "_", "_", "_", "_", "_", "_"]
    password2 = list(password1)
    password1_index = 0
    prev_time = timer()

    # Keep going until we've decrypted the passwords for parts 1 and 2
    while "_" in password2 or "_" in password1:
        string_to_hash = door_id + str(index)
        result = hashlib.md5(string_to_hash.encode()).hexdigest()

        # Print a cool hacker effect while we're decrypting
        curr_time = timer()
        if (curr_time - prev_time) > 0.05:
            print_passwords("DECRYPTION IN PROGRESS...", password1, password2)
            prev_time = curr_time

        # We found a hash starting with 5 zeros. Attempt to fill in our passwords.
        if result.startswith("00000"):
            # Part 1
            if password1_index < len(password1):
                password1[password1_index] = result[5]
                password1_index += 1

            # Part 2
            if result[5].isdigit():
                password2_index = int(result[5])
                if 0 <= password2_index < len(password2) and password2[password2_index] == "_":
                    password2[password2_index] = result[6]

        index += 1

    return password1, password2


# Parts 1 & 2
# Display the decrypted passwords for both decryption methods
print_passwords("DECRYPTION COMPLETE", *decrypt_passwords("uqwqemis"))
