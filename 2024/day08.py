import itertools
from pathlib import Path

example1 = '''............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............'''
example1 = example1.split()

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

def find_antennae(grid: list[str]
                  ) -> dict[str, list[tuple[int, int]]]:
    """
    Identifies and stores the positions of antennae in a grid based on their frequency markers.

    This function scans through a grid and collects coordinates of all antenna positions,
    grouping them by their frequency markers. Each unique marker is used as a key in the returned
    dictionary, with the value being a list of tuples representing the coordinates of the antennae.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
                          Each character in the grid represents an antenna frequency marker or
                          an empty position ('.').

    Returns:
        dict[str, list[tuple[int, int]]]: A dictionary where keys are frequency markers and values
                                          are lists of tuples, each tuple representing the (x, y) 
                                          coordinates of antennae on that frequency.
    """
    antennae = {}
    # Iterate through grid to search for antennae
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            if posn != '.':
                try:
                    # If we already have antennae on this frequency
                    antennae[posn].append((x,y))
                except KeyError: # First antenna on this frequency
                    antennae[posn] = [(x,y)]

    return antennae

def in_grid(grid: list[str], x: int, y: int) -> bool:
    """
    Checks whether a given position is within the boundaries of a grid.

    This function verifies if the specified coordinates (x, y) are valid positions
    within the provided grid, ensuring they do not exceed the grid's dimensions.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        x (int): The x-coordinate (column index) to check.
        y (int): The y-coordinate (row index) to check.

    Returns:
        bool: True if the position (x, y) is within the grid boundaries; False otherwise.
    """
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return True
    else:
        return False

def invoke_resonance(grid: list[str], 
                     x1: int, y1: int, 
                     delta_x: int, delta_y: int
                     ) -> set[tuple[int, int]]:
    """
    Calculates resonant antinodes in a grid by extending from a starting position, in both 
    directions.

    This function identifies all grid positions (antinodes) that lie along a line defined by
    a starting position and directional increments (delta_x, delta_y). It extends the search in
    both forward and backward directions until the grid boundaries are reached. Naturally, 
    the set of antinodes will include both original transmitters used to form the line. 

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        x1 (int): The starting x-coordinate (column index) for resonance calculation.
        y1 (int): The starting y-coordinate (row index) for resonance calculation.
        delta_x (int): The x-directional increment for extending the resonance line.
        delta_y (int): The y-directional increment for extending the resonance line.

    Returns:
        set[tuple[int, int]]: A set of tuples, each representing the (x, y) coordinates of 
                              resonant antinodes found within the grid.

    Note:
        This does not include all antinodes when there are valid antinodes between the original 
        transmitters (ie: the delta values have a common factor). However, this does not seem 
        ever to be the case in this puzzle. 
    """
    antinodes = set()
    x, y = x1, y1
    # Search in one direction from the original transmitter
    while in_grid(grid, x, y):
        antinodes.add((x, y))
        x, y = (x-delta_x, y-delta_y)
    # Reset x and y, and search in the other direction from the original transmitter
    x, y = x1, y1
    while in_grid(grid, x, y):
        antinodes.add((x, y))
        x, y = (x+delta_x, y+delta_y)

    return antinodes

def find_antinodes(grid: list[str], 
                   antennae: dict[str, list[tuple[int, int]]]
                   ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    Identifies antinodes on a grid based on the locations of antennae. 
    This function processes pairs of antennae within each frequency group to determine potential
    antinodes, with and without invoking resonant harmonics, in the grid. It returns two sets: 
    one for basic antinodes and another for those including resonant harmonics. 

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        antennae (dict[str, list[tuple[int, int]]]): A dictionary where keys are frequency markers
                                                     and values are lists of tuples, each tuple 
                                                     representing the (x, y) coordinates of 
                                                     antennae on that frequency.

    Returns:
        tuple[set[tuple[int, int]], set[tuple[int, int]]]: A tuple containing:
            - A set of basic antinodes calculated from pairs of antennae.
            - A set of antinodes including those on resonant harmonics. 
    """
    antinodes = set()
    antinodes_part2 = set()
    for locations in antennae.values():
        # Generate all pairwise location combinations for this freqency
        pairs = list(itertools.combinations(locations, 2))
        for pair in pairs:
            (x1, y1), (x2, y2) = pair
            delta_x, delta_y = (x2-x1), (y2-y1)
            # Find exactly 2 antinodes for Part 1
            antinode1 = (x1-delta_x, y1-delta_y)
            antinode2 = (x2+delta_x, y2+delta_y)
            antinodes.update({antinode1, antinode2}) # Addition of sets

            # Find all the antinodes including resonance for Part 2
            resonant_antinodes = invoke_resonance(grid, x1, y1, delta_x, delta_y)
            antinodes_part2.update(resonant_antinodes)
    
    # Remove invisible antinodes
    antinodes = list(antinodes) # Allow iteration
    for antinode in antinodes[::-1]: # Then iterate backwards, removing antinodes outside grid
        x, y = antinode
        if not in_grid(grid, x, y):
            antinodes.remove(antinode)
    
    return antinodes, antinodes_part2

def run(grid: list[str]) -> tuple[int, int]:
    """
    Analyzes a grid to determine the number of antinodes and resonant antinodes based on 
    antenna positions.

    This function identifies antennae within the grid, calculates potential antinodes from 
    antennae pairs, and then determines additional resonant antinodes (for Part 2). It returns 
    the counts of both sets of antinodes - with and without resonant harmonics. 

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row. 
                          Each character in the grid represents either an antenna frequency 
                          marker or an empty position.

    Returns:
        tuple[int, int]: A tuple containing:
            - The number of basic antinodes found (int).
            - The number of antinodes found based on resonant harmonics (int).
    """
    antennae = find_antennae(grid)
    antinodes, antinodes_part2 = find_antinodes(grid, antennae)

    return len(antinodes), len(antinodes_part2)

inputfile = Path('day08.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 392:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 1235:
    print('PASS')