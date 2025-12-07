from functools import lru_cache
from pathlib import Path

example = """.......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ..............."""
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

def find_start(grid: list[str]) -> tuple[int, int]:
    """
    Locate the start coordinate 'S' in a 2D grid of characters.

    Scans the grid row by row and returns the (x, y) coordinate of the first
    occurrence of the character 'S'. Coordinates are zero-based: x is the
    column index within a row, y is the row index within the grid.

    Args:
        grid (list[str]): The character grid represented as a list of strings.

    Returns:
        tuple[int, int]: The (x, y) position of the first 'S' found.

    Raises:
        ValueError: If no 'S' character exists in the grid.
    """
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == 'S':
                return (x, y)

def progress_tachyons(grid: list[str], start: tuple[int, int]) -> int:
    """
    Advance a beam through the grid from a start position and count splits.

    Treats the beam as a set of coordinates reached in the previous row. For each
    cell (x, y), if its parent (x, y-1) is in the beam:
    - '.' moves the beam straight down to (x, y).
    - '^' splits the beam to (x-1, y) and (x+1, y) and increments beam_splits.

    Args:
        grid (list[str]): 2D character grid as a list of strings.
        start (tuple[int, int]): Initial coordinate (x, y) where the beam starts.

    Returns:
        int: The total number of splits achieved.
    """
    beam = {start} # Set of 1 tuple
    beam_splits = 0

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if (x, y-1) in beam:
                if char == '.':
                    beam.add((x, y))
                elif char == '^':
                    beam.update({(x-1, y), (x+1, y)})
                    beam_splits += 1
    
    return beam_splits

def count_timelines(grid: list[str], start: tuple[int, int]) -> int:
    """
    Count the number of completed downward paths from a start coordinate.

    Uses recursion with memoization to traverse the grid from `start`, moving one
    row down per step according to the cell beneath:
    - '^' splits the path to (x-1, y+1) and (x+1, y+1).
    - '.' continues straight to (x, y+1).
    - Any other character ends the path immediately (a completion).
    A path is considered complete when it reaches the last grid row.

    Args:
        grid (list[str]): The character grid as a list of strings.
        start (tuple[int, int]): Starting coordinate (x, y).

    Returns:
        int: Total number of completed paths from `start`.
    """
    @lru_cache(maxsize = None)
    def recur(cur_x: int, cur_y: int) -> int:
        """
        Recursively compute the number of paths downwards from (cur_x, cur_y).

        At each step, look one row below (next_y = cur_y + 1) and apply the movement
        rule based on the cell beneath:
        - '^': split to (cur_x - 1, next_y) and (cur_x + 1, next_y), summing both.
        - '.': continue straight to (cur_x, next_y).
        - any other character: terminate the path (counts as 1 completed path).

        A path is considered complete when it has reached the bottom row, in which 
        case 1 is returned.

        Args:
            cur_x (int): Current column index.
            cur_y (int): Current row index.

        Returns:
            int: Number of completed paths reachable from (cur_x, cur_y).

        Notes:
            - Results are memoized per (x, y) via lru_cache to avoid recomputation.
            - Since no splitters exist on the outer row-wise bounds of grid, no bounds checks
            are performed for sideways moves. 
        """
        next_y = cur_y + 1
        if next_y > max_y:
            return 1 # Path is complete
        
        cell_beneath = grid[next_y][cur_x]
        if cell_beneath == '^':
            total = 0
            total += recur(cur_x - 1, next_y) # Add from left split
            total += recur(cur_x + 1, next_y) # Add from right split
            return total if total > 0 else 1 # XXX
        elif cell_beneath == '.':
            return recur(cur_x, next_y) # Add from path straight down
        else:
            return 1

    max_y = len(grid) - 1
    paths = recur(*start)

    return paths

def run(grid: list[str]) -> tuple[int, int]:
    """
    Execute both beam progression and timeline counting from the grid start.

    Finds the start coordinate 'S' in the grid, advances the beam according to
    progress_tachyons, and counts the total number of completed downward paths
    using count_timelines. Returns both results.

    Args:
        grid (list[str]): 2D character grid as a list of strings.

    Returns:
        tuple[int, int]: (part1, part2) where:
            - part1 is the split count (or result) from progress_tachyons.
            - part2 is the total number of completed paths from count_timelines.

    Raises:
        ValueError: If no 'S' start coordinate is found by find_start.
    """
    start = find_start(grid)
    part1 = progress_tachyons(grid, start)
    part2 = count_timelines(grid, start)

    return part1, part2

inputfile = Path('day07.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(example)

print('Day 1:', part1_result)
if part1_result == 1553:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 15811946526915:
    print('PASS')