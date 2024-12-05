from pathlib import Path

example1 = '''MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX'''
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

# Part 1
def get_next_letter(this_letter: str, letters: str) -> str | None:
    """
    Retrieves the next letter in a sequence from a given list of letters.

    This function attempts to find the letter immediately following the specified letter
    in the provided list. If the specified letter is the last in the list, the function
    returns None.

    Args:
        this_letter (str): The letter for which the next letter is to be found.
        letters (str): A word, in which to search for the next letter.

    Returns:
        str or None: The next letter in the word if it exists; otherwise, None.
    """
    try:
        next_letter = letters[letters.index(this_letter) + 1]
    except IndexError:
        next_letter = None

    return next_letter

def find_next_letter(x: int, y: int, 
                     this_letter: str, letters: str, direction: str, 
                     grid: list[str]) -> bool:
    """
    Recursively searches for the next letter in a word within a grid, following a specified 
    direction.
    This function checks if the next letter in a sequence can be found by moving in a specified
    direction from the current position in the grid. If the entire word is found, it returns True.

    Args:
        x (int): The current x-coordinate (column index) in the grid.
        y (int): The current y-coordinate (row index) in the grid.
        this_letter (str): The current letter in the sequence being searched.
        letters (str): A list of letters forming the word being searched.
        direction (str): The direction in which to search for the next letter. Expected values 
            are 'W', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', representing the compass directions, 
            where "up" is north. 
        grid (list[str]): A list of strings representing the grid of letters.

    Returns:
        bool: True if the entire word is found in the specified direction; otherwise, False.
    """
    next_letter = get_next_letter(this_letter, letters)
    if next_letter is None: # Whole word found
        return True
    
    new_coordinates = {'W': (x-1,y), 
                       'SW': (x-1,y+1), 
                       'S': (x,y+1), 
                       'SE': (x+1,y+1), 
                       'E': (x+1,y), 
                       'NE': (x+1,y-1), 
                       'N': (x,y-1), 
                       'NW': (x-1,y-1)
                       }
    new_x, new_y = new_coordinates[direction]
    # Take a step, but only if the grid boundaries allow you to
    if 0 <= new_x < len(grid[0]) \
        and 0 <= new_y < len(grid) \
        and grid[new_y][new_x] == next_letter:

        # Recursively check whether the next letter is in the expected direction
        return find_next_letter(new_x, new_y, next_letter, letters, direction, grid)

    # If the full word was not found
    return False

def find_from_x(grid: list[str]) -> int:
    """
    Counts the occurrences of the word "XMAS" in a grid, starting from each 'X' and checking
    in every direction.

    This function searches for the sequence of letters "XMAS" beginning from each 'X' in the grid,
    exploring all possible directions, and then using find_next_letter() to look in possible 
    directions for the full word. 

    Args:
        grid (list[str]): A 2D list representing the grid of letters.

    Returns:
        int: The number of times the word "XMAS" is found in the grid.
    """
    letters = 'XMAS'
    xmases = 0
    
    # Start from each 'X', checking in every direction for the full word 'XMAS'
    for y, line in enumerate(grid):
        for x, letter in enumerate(line):
            if letter == 'X':
                for direction in directions:
                    # Recursively look in this direction for each letter in turn
                    word_found = find_next_letter(x, y, 'X', letters, direction, grid)
                    if word_found:
                        xmases += 1
    
    return xmases

# Part 2
def is_x_mas(x: int, y: int, grid: list[str]) -> bool:
    """
    Determines if an "X-MAS" pattern can be formed around a given position in a grid.

    An "X-MAS" pattern is defined by the presence of the string "MAS" on both diagonal lines
    passing through the specified (x, y) centre (containing "A"). 

    Args:
        x (int): The x-coordinate (column index) of the centre position in the grid.
        y (int): The y-coordinate (row index) of the centre position in the grid.
        grid (list[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        bool: True if an "X-MAS" pattern is found around the specified position; otherwise False.
    """
    # Check whether an X-MAS can fit within the grid
    if any((x < 1, x+1 >= len(grid[0]), y < 1, y+1 >= len(grid))):
        return False

    diagonals = f'{grid[y-1][x+1]}\
                  {grid[y+1][x+1]}\
                  {grid[y+1][x-1]}\
                  {grid[y-1][x-1]}\
                  '.replace(' ','')
    
    # Check whether the diagonals about "A" represent an X-MAS
    if diagonals.count('M') == 2 and diagonals.count('S') == 2 \
        and ('SS' in diagonals or 'MM' in diagonals):

        return True
    else:
        return False

def find_x_mas(grid: list[str]) -> int:
    """
    Counts the occurrences of the "X-MAS" pattern in a grid. 

    The function checks each 'A' in the grid to determine if it is part of an "X-MAS"
    pattern, as defined by the is_x_mas() function. If the pattern is found, the count of 
    such patterns is incremented.

    Args:
        grid (list[str]): A list of strings representing the grid of letters.

    Returns:
        int: The number of "X-MAS" patterns found in the grid.
    """
    x_mases = 0
    # Starting from each 'A', look for X-MAS patterns
    for y, line in enumerate(grid):
        for x, letter in enumerate(line):
            if letter == 'A':
                result = is_x_mas(x, y, grid)
                if result:
                    x_mases += 1

    return x_mases

directions = ['W', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW']

inputfile = Path('day04.txt')
data = read_inputfile(inputfile)
part1_result = find_from_x(data)
part2_result = find_x_mas(data)

print('Day 1:', part1_result)
if part1_result == 2447:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 1868:
    print('PASS')