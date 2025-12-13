from collections import deque
from pathlib import Path

example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
example = [line.strip() for line in example.split('\n')]

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

def parse_schematics(schematics_str: str) -> list[list[int]]:
    """
    Parse a string of button schematics into a list of integer index lists.

    The input string is expected to contain groups of zero-based indices enclosed
    in parentheses and separated by spaces, e.g. "(0,2,5) (1,3) (4)". Parentheses 
    are removed, then each group is split by commas and converted to a list of 
    integers, producing a list of buttons where each button is a list of indices 
    it affects.

    Args:
        schematics_str (str): A string describing buttons, where spaces separate 
            buttons and commas separate indices.

    Returns:
        list[list[int]]: A list of buttons, where each button is a list of
            zero-based integer indices (e.g., [[0, 2, 5], [1, 3], [4]]).

    Raises:
        ValueError: If any index token cannot be converted to an integer.

    Examples:
        Input: "(0,2,5) (1,3) (4)"
        Output: [[0, 2, 5], [1, 3], [4]]
    """
    schematics_str = schematics_str.replace('(', '').replace(')', '')
    schematics = []
    for schematic in schematics_str.split(' '):
        schematics.append([int(x) for x in schematic.split(',')])

    return schematics

def parse_joltages(joltage_str: str) -> tuple[int]:
    """
    Parse a string of target joltages into a tuple of integers.

    The input string is expected to use curly braces and commas to list values,
    e.g. "{3,5,4,7}". Curly braces are stripped, and the remaining comma-separated
    tokens are converted to integers, yielding a tuple.

    Args:
        joltage_str (str): A string of comma-separated integers, enclosed in curly 
            braces.

    Returns:
        tuple[int]: A tuple of integers representing target joltages. 

    Raises:
        ValueError: If any token cannot be converted to an integer.

    Examples:
        Input: "{230,50,217}"
        Output: (230, 50, 217)
    """
    joltage_str = joltage_str.replace('{', '').replace('}', '')

    return tuple(int(x) for x in joltage_str.split(','))

def parse_input(data: list[str]) -> list[tuple[str, list[list[int]], tuple[int]]]:
    """
    Parse puzzle input lines into (indicator pattern, button schematics, target joltages).

    Each input line is expected to contain:
      - An indicator lights pattern in square brackets (e.g., "[.##.]"),
      - A space, then a series of button schematics (e.g., "(0,2,5) (1,3) ..."),
      - A space, then a joltage target list in curly braces (e.g., "{3,5,4,7}").

    The function extracts and converts:
      - indicators: the raw string inside the leading square brackets, e.g. ".##."
      - schematics: a list of buttons (each button is a list of zero-based indices)
        parsed via parse_schematics
      - joltages: a tuple of integers parsed via parse_joltages

    Args:
        data (list[str]): Input lines in the expected format, one per puzzle row.

    Returns:
        list[tuple[str, list[list[int]], tuple[int]]]:
            A list of tuples (indicators, schematics, joltages), where:
              - indicators (str): e.g., ".##."
              - schematics (list[list[int]]): e.g., [[0,2,5], [1,3]]
              - joltages (tuple[int]): e.g., (3, 5, 4, 7)

    Raises:
        ValueError: Propagated from parse_schematics or parse_joltages if the
            schematics or joltage segments contain invalid tokens.

    Examples:
        Input line:
            "[...#.] (0,2,3,4) (2,3) (0,4) {7,5,12,7,2}"
        Parsed tuple:
            ("...#.", [[0,2,3,4], [2,3], [0,4]], (7, 5, 12, 7, 2))
    """
    manual = []
    for row in data:
        indicators, _, remainder = row.partition(' ')
        indicators = indicators[1:-1]
        schematics_str, _, joltage_str = remainder.rpartition(' ')
        schematics = parse_schematics(schematics_str)
        joltages = parse_joltages(joltage_str)

        new_row = (indicators, schematics, joltages)
        manual.append(new_row)

    return manual

def press_button(indicators: str, button: list[int]) -> str:
    """
    Toggle indicator lights at specified positions.

    Given an indicator string of '.' (off) and '#' (on), this function flips
    the state of each zero-based position listed in `button`. A '.' becomes '#',
    and a '#' becomes '.'. Positions not listed remain unchanged.

    Args:
        indicators (str): Current indicator pattern, e.g., ".##.#".
        button (list[int]): Zero-based indices of lights to toggle.

    Returns:
        str: The updated indicator pattern after applying the toggles.
    """
    input_list = list(indicators)
    for pos in button: # Toggle each relevant position
        if input_list[pos] == '#':
            input_list[pos] = '.'
        else:
            input_list[pos] = '#'
    
    return ''.join(input_list)

def calc_min_presses(indicators: str, schematics: list[list[int]]) -> int | None:
    """
    Compute the minimum number of button presses to reach a target indicator pattern.

    Uses breadth-first search (BFS) over indicator states starting from the all-off
    pattern ('.' repeated for the length of `indicators`). Each button press toggles
    specified positions, generating successor states. The first time the target 
    `indicators` is dequeued, the current depth is the minimal number of presses.

    Args:
        indicators (str): Target indicator pattern of '.' and '#', e.g., ".##.#".
        schematics (list[list[int]]): List of buttons, each a list of zero-based
            indices to toggle.

    Returns:
        int: The minimal number of presses to reach `indicators` from the
            all-off state. 
        None: If the target is unreachable. 
    """
    initial_state = ('').join(('.' for _ in indicators))

    queue = deque()
    queue.append((initial_state, 0)) # (current_state, num_presses)
    visited = set()
    visited.add(initial_state)

    while queue:
        current_state, num_presses = queue.popleft()

        if current_state == indicators:
            return num_presses

        for button in schematics:
            new_state = press_button(current_state, button)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, num_presses + 1))

    return None # If no solution found

def run(data: list[str]) -> int:
    manual = parse_input(data)

    total = 0
    for row in manual:
        total += calc_min_presses(row[0], row[1])
    
    return total

inputfile = Path('day10.txt')
data = read_inputfile(inputfile)

part1_result = run(example)

print('Day 1:', part1_result)
if part1_result == 509:
    print('PASS')