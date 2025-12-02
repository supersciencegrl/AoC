from pathlib import Path

example = """L68
    L30
    R48
    L5
    R60
    L55
    L1
    L99
    R14
    L82"""
example = example.split('\n    ')

def read_inputfile(inputfile: Path) -> list[str]:
    """
    Reads a text file and returns a list of its lines, with leading/trailing whitespace removed.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        list[str]: A list containing each line of the file as a string, with leading/trailing 
                   whitespace removed.
    """
    with open(inputfile, 'rt') as fin:
        data = fin.readlines()
    
    return [line.strip() for line in data]

inputfile = Path('day01.txt')
data = read_inputfile(inputfile)

START = 50
DIAL_MAX = 99

def move_dial(start_pos: int, direction: str, steps: int) -> tuple[int, int]:
    """
    Move a 0–DIAL_MAX circular dial left or right by a number of steps.

    The dial has positions 0 through DIAL_MAX inclusive. Moving left ('L') decrements 
    the position and wraps under 0; moving right ('R') increments and wraps over DIAL_MAX. 
    The function returns the new position and how many full wraparounds (times zero is 
    passed) occur during the move.

    Args:
        start_pos (int): Starting position on the dial in the range [0, DIAL_MAX].
        direction (str): Direction to move: 'L' for left (counter-clockwise) or
            'R' for right (clockwise).
        steps (int): Number of steps to move. Must be a non-negative integer.

    Returns:
        tuple[int, int]: A tuple of:
            - new_pos (int): The resulting dial position in [0, DIAL_MAX].
            - times_passing_zero (int): The count of full rotations past zero
              encountered during the move. This increments each time the motion
              crosses from DIAL_MAX to 0 (for right moves) or from 0 to DIAL_MAX
              (for left moves). If starting at 0 and moving left, the initial
              step does not count as passing zero until landing back on 0.

    Raises:
        ValueError: If direction is not 'L' or 'R'.
    """
    times_passing_zero = 0 # Default

    if direction == 'L':
        times_passing_zero += abs((start_pos - steps) // (DIAL_MAX + 1))
        new_pos = (start_pos - steps) % (DIAL_MAX + 1)
        if start_pos == 0:
            times_passing_zero -= 1
        if new_pos == 0:
            times_passing_zero += 1
    elif direction == 'R':
        times_passing_zero += abs((start_pos + steps) // (DIAL_MAX + 1))
        new_pos = (start_pos + steps) % (DIAL_MAX + 1)
    else:
        raise ValueError("Direction must be 'L' or 'R'")

    return (new_pos, times_passing_zero)

def read_instructions(data: list[str]):
    """
    Execute a sequence of dial movement instructions and count zero events.

    Processes instruction strings of the form "<D><N>" where <D> is the
    direction ('L' for left, 'R' for right) and <N> is a non-negative integer
    number of steps. Uses move_dial(...) iteratively starting from START to
    update the dial position, track how often the position lands on zero, and
    how many times zero is passed during movement.

    Args:
        data (list[str]): List of instructions like "L30", "R100". Each string
            must start with 'L' or 'R' followed by an integer step count.

    Returns:
        tuple[int, int]: A tuple of:
            - zero_positions (int): Number of times the final position after an
              instruction lands exactly on 0.
            - zero_passed (int): Total count of crossings past zero accumulated over
              all instructions (as reported by move_dial).

    Side Effects:
        Prints the position and times_passing_zero for each processed
        instruction in the form: "<position> <times_passing_zero>".

    Raises:
        ValueError: If an instruction has an invalid direction or a non-integer
            step count (propagated from parsing or move_dial).
    """
    position = START # Initial position
    zero_positions = 0 # Count of times position sits on zero
    zero_passed = 0 # Count of times position sits on or passes zero

    for instruction in data:
        direction = instruction[0]
        steps = int(instruction[1:])

        position, times_passing_zero = move_dial(position, direction, steps)
        if position == 0:
            zero_positions += 1
        print(position, times_passing_zero)
        zero_passed += times_passing_zero

    return zero_positions, zero_passed

part1_result, part2_result = read_instructions(data)

print('Day 1:', part1_result)
if part1_result == 995:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 5847:
    print('PASS')


def move_dial_tests():
    """
    Quick tests for move_dial(start_pos, direction, steps).

    Verifies that moving a 0–99 dial left ('L') or right ('R') by a number of
    steps wraps correctly and returns a tuple of (new_position, full_rotations).
    Raises AssertionError with details if any case fails.
    """
    test_cases = [
        (50, 'L', 30, (20, 0)),
        (50, 'L', 50, (0, 1)),
        (50, 'L', 80, (70, 1)),
        (50, 'L', 180, (70, 2)),
        (0, 'L', 1, (99, 0)),
        (0, 'L', 100, (0, 1)),
        (0, 'L', 200, (0, 2)),
        (50, 'R', 30, (80, 0)),
        (50, 'R', 50, (0, 1)),
        (50, 'R', 80, (30, 1)),
        (50, 'R', 180, (30, 2)),
        (0, 'R', 20, (20, 0)),
        (0, 'R', 100, (0, 1)),
        (0, 'R', 200, (0, 2)),
    ]

    for start_pos, direction, steps, expected in test_cases:
        result = move_dial(start_pos, direction, steps)
        assert result == expected, f"move_dial({start_pos}, {direction}, {steps}) = {result}, expected {expected}"