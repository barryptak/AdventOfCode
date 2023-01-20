"""
https://adventofcode.com/2022/day/22
"""
from utils import read_data, Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE, strip=False)

#region Facing Helper Structures

FACE_RIGHT = Point2D(1, 0)
FACE_LEFT = Point2D(-1, 0)
FACE_UP = Point2D(0, -1)
FACE_DOWN = Point2D(0, 1)

TURN = {
        FACE_RIGHT: {
            "L": FACE_UP,
            "R": FACE_DOWN
        },
        FACE_LEFT: {
            "L": FACE_DOWN,
            "R": FACE_UP
        },
        FACE_UP: {
            "L": FACE_LEFT,
            "R": FACE_RIGHT
        },
        FACE_DOWN: {
            "L": FACE_RIGHT,
            "R": FACE_LEFT
        }
}

FACING_VALUE = {
    FACE_RIGHT: 0,
    FACE_DOWN: 1,
    FACE_LEFT: 2,
    FACE_UP: 3
}

#endregion

def parse_data(input_data):
    """ Read in the board data and instructions from the input data """

    # Store the board data and grab the instructions from the end of the list
    board = input_data
    instruction_string = board.pop()
    # Get rid of the blank line
    board.pop()

    # Parse the instructions in to separate commands
    current_index = 0
    letter = False
    instructions = []
    while True:
        # If the next instruction is a letter then just place it directly into
        # the instruction list
        if letter:
            instructions.append(instruction_string[current_index])
            current_index += 1
            letter = False
        # If the next instruction is a number then we need to figure out how
        # long the number is and then the full number into the instruction list
        else:
            start = current_index
            current_index += 1
            while (current_index < len(instruction_string) and
                   instruction_string[current_index].isdigit()):
                current_index += 1

            instructions.append(int(instruction_string[start:current_index]))
            letter = True

        if current_index >= len(instruction_string):
            break

    return board, instructions


def get_new_facing(current_facing, turn_direction):
    """
    What's the new facing direction after applying the turn direction to the
    current facing?
    """
    return TURN[current_facing][turn_direction]

#region Part 1 wrapping functions

def wrap_left_1(board, pos):
    """ Wrap left round the 2D space board from pos for part 1 """
    new_x = max(board[pos.y].rindex("."), board[pos.y].rindex("#"))
    return Point2D(new_x, pos.y), FACE_LEFT


def wrap_right_1(board, pos):
    """ Wrap right round the 2D space board from pos for part 1 """
    x = min(board[pos.y].index("."), board[pos.y].index("#"))
    return Point2D(x, pos.y), FACE_RIGHT


def wrap_up_1(board, pos):
    """ Wrap up round the 2D space board from pos for part 1 """
    for y, row in enumerate(reversed(board)):
        if pos.x < len(row) and row[pos.x] != " ":
            return Point2D(pos.x, len(board) - 1 - y), FACE_UP


def wrap_down_1(board, pos):
    """ Wrap down round the 2D space board from pos for part 1 """
    for y, row in enumerate(board):
        if pos.x < len(row) and row[pos.x] != " ":
            return Point2D(pos.x, y), FACE_DOWN

#endregion

#region Part 2 wrapping functions

# NOTE: I couldn't be bothered figuring out how to determine the wrapping logic
# procedurally for any board/cube layout. It felt like way too much work.
# So, I've just hard-coded the wraping logic for this specific puzzling input
# after figuring it out manually....

def wrap_left_2(_, pos):
    """ Wrap left round the 3D space board from pos for part 2 """
    if pos.y < 50:
        return Point2D(0, 149 - pos.y), FACE_RIGHT
    elif pos.y < 100:
        return Point2D(pos.y - 50, 100), FACE_DOWN
    elif pos.y < 150:
        return Point2D(50, 49 - (pos.y - 100)), FACE_RIGHT
    else:
        return Point2D((pos.y - 149) + 49, 0), FACE_DOWN


def wrap_right_2(_, pos):
    """ Wrap right round the 3D space board from pos for part 2 """
    if pos.y < 50:
        return Point2D(99, 149 - pos.y), FACE_LEFT
    elif pos.y < 100:
        return Point2D(99 + (pos.y - 49), 49), FACE_UP
    elif pos.y < 150:
        return Point2D(149, 49 - (pos.y - 100)), FACE_LEFT
    else:
        return Point2D(49 + (pos.y - 149), 149), FACE_UP


def wrap_up_2(_, pos):
    """ Wrap up round the 3D space board from pos for part 2 """
    if pos.x < 50:
        return Point2D(50, pos.x + 50), FACE_RIGHT
    elif pos.x < 100:
        return Point2D(0, (pos.x - 50) + 150), FACE_RIGHT
    else:
        return Point2D(pos.x - 100, 199), FACE_UP


def wrap_down_2(_, pos):
    """ Wrap down round the 3D space board from pos for part 2 """
    if pos.x < 50:
        return Point2D(pos.x + 100, 0), FACE_DOWN
    elif pos.x < 100:
        return Point2D(49, (pos.x - 50) + 150), FACE_LEFT
    else:
        return Point2D(99, (pos.x - 100) + 50), FACE_LEFT

#endregion

# Which wrap function to call for the current facing and problem part
WRAP = {FACE_LEFT: {1: wrap_left_1, 2: wrap_left_2},
        FACE_RIGHT: {1: wrap_right_1, 2: wrap_right_2},
        FACE_UP: {1: wrap_up_1, 2: wrap_up_2},
        FACE_DOWN: {1: wrap_down_1, 2: wrap_down_2} }


def out_of_bounds_or_empty(board, pos):
    """
    Is this position outside the bounds of the board or empty?
    Empty means that the position is outside of the board too (but is stored as
    a space character as it's padding out the board)
    """
    if (0 <= pos.y < len(board) and
        0 <= pos.x < len(board[pos.y])):
        return board[pos.y][pos.x] == " "
    return True


def follow_path(board, path, part):
    """
    Follow the supplied path instructions on the board.
    Part indicates if this is part 1 or part 2 of the puzzle as we use different
    wrapping functions depending which part we are solving.
    """
    # Determine our starting position
    current_pos = Point2D(board[0].index("."), 0)
    current_facing = FACE_RIGHT

    # Iterate over all of the instructions we have to process
    is_move = True
    for instruction in path:
        # If this is a move instruction then apply wrapping around the board
        # and check for being blocked by #s on the board
        if is_move:
            # We need to apply move instructions one step at a time as we could
            # wrap or be blocked at any step
            for _ in range(instruction):
                next_pos = current_pos + current_facing
                next_facing = current_facing

                # Handle wrapping and 'empty' positions
                if out_of_bounds_or_empty(board, next_pos):
                    next_pos, next_facing = WRAP[current_facing][part](board, next_pos)

                # Are we blocked?
                if board[next_pos.y][next_pos.x] == "#":
                    # Don't move any further and jump to the next instruction
                    continue
                else:
                    # Not blocked - update our position and facing
                    current_pos = next_pos
                    current_facing = next_facing
        else:
            # Is turn instruction
            current_facing = get_new_facing(current_facing, instruction)

        # Instructions alternate between num moves to make and turn instructions
        is_move = not is_move

    return current_pos, current_facing


def get_password(pos, facing_dir):
    """ Calculate the password for the supplied position and facing """
    password = (1000 * (pos.y + 1)) + (4 * (pos.x + 1)) + FACING_VALUE[facing_dir]
    return password


# Part 1
# Follow the path around the board as if the board is a flat 2D space
PART_1 = 1
board_map, path_instructions = parse_data(data)
position, facing = follow_path(board_map, path_instructions, PART_1)
print(get_password(position, facing))

# Part 2
# Follow the path around the board as if the board folds up into a 3D cube
PART_2 = 2
position, facing = follow_path(board_map, path_instructions, PART_2)
print(get_password(position, facing))
