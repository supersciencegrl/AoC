from pathlib import Path

example = """..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@."""
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

def analyse_surroundings(data: list[str], x: int, y: int) -> int:
    """
    Count the number of adjacent '@' symbols around a grid coordinate.

    Checks the eight neighboring positions (as defined by the iterable
    `surroundings` of (dx, dy) offsets) around the cell at (x, y) in the
    2D character grid `data`. In-bounds neighbors with the character '@'
    are counted.

    Args:
        data (list[str]): Rectangular grid represented as a list of equal-length
            strings, where data[y][x] accesses the character at (x, y).
        x (int): Zero-based column index of the reference cell.
        y (int): Zero-based row index of the reference cell.

    Returns:
        int: The number of adjacent cells containing '@'.

    Notes:
        - Cells outside the grid boundaries are ignored.
    """
    adjacent_rolls = 0
    max_x = len(data[0])
    max_y = len(data)

    for delta_x, delta_y in surroundings:
        new_x = x + delta_x
        new_y = y + delta_y
        if 0 <= new_x < max_x and 0 <= new_y < max_y:
            new_char = data[new_y][new_x]
            if new_char == '@':
                adjacent_rolls += 1
    
    return adjacent_rolls

def run_part1(data: list[str]) -> list[tuple[int, int]]:
    """
    Find all '@' positions with fewer than four adjacent '@' neighbors.

    Scans the 2D grid and, for each cell containing '@', counts adjacent '@'
    using analyse_surroundings. Rolls with a neighbor count less than 4 are
    collected as accessible rolls.

    Args:
        data (list[str]): Rectangular character grid represented as a list of
            equal-length strings.

    Returns:
        list[tuple[int, int]]: List of (x, y) coordinates where the cell is '@'
        and has fewer than four adjacent '@' cells.
    """
    accessible_rolls = []

    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == '@':
                adjacent_rolls = analyse_surroundings(data, x, y)
                # print(x+1, y+1, adjacent_rolls)
                if adjacent_rolls < 4:
                    accessible_rolls.append((x, y))
    
    return accessible_rolls

def remove_roll(grid: list[str], roll: tuple[int, int]) -> list[str]:
    """
    Replace a single '@' (or any character) at a given coordinate with '.' in a grid.

    Takes an immutable-string grid representation (list of strings), targets the
    specified (x, y) coordinate, and returns that roll replaced by a '.' character.

    Args:
        grid (list[str]): Rectangular grid as a list of equal-length strings.
        roll (tuple[int, int]): Zero-based (x, y) coordinate to clear.

    Returns:
        list[str]: The same list object with the specified cell replaced by '.'.
    """
    roll_x, roll_y = roll
    row = grid[roll_y]

    grid[roll_y] = row[:roll_x] + '.' + row[roll_x+1:]

    return grid

def run_part2(data: list[str]) -> int:
    """
    Iteratively remove accessible '@' cells until none remain and count th eremovals.

    Repeatedly computes accessible '@' positions using run_part1 and removes
    them from the grid with remove_roll. Continues until a pass finds no
    accessible rolls, then returns the total number of removals performed.

    Args:
        data (list[str]): Rectangular character grid represented as a list of
            equal-length strings.

    Returns:
        int: Total count of '@' cells removed across all iterations.
    """
    grid = data
    accessible_rolls = True # Default
    rolls_removed = 0

    while accessible_rolls:
        accessible_rolls = run_part1(grid)
        # Define new grid with rolls removed
        for roll in accessible_rolls:
            grid = remove_roll(grid, roll)
        rolls_removed += len(accessible_rolls)

    return rolls_removed

inputfile = Path('day04.txt')
data = read_inputfile(inputfile)

surroundings = [
    (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)
    ]

part1_result = len(run_part1(data))
part2_result = len(run_part2(data))

print('Day 1:', part1_result)
if part1_result == 1464:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 8409:
    print('PASS')