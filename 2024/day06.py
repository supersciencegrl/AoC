from pathlib import Path

example='''....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...'''
example = example.split()

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

def find_guard(grid: list[str]) -> tuple[int, int]:
    """
    Finds the position of a guard character in a grid.

    This function searches through a grid of strings to find the first occurrence
    of any specified guard character from the global list, and returns its coordinates.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        tuple[int, int]: A tuple containing the x and y coordinates of the first found guard 
            character.
        None: If no guard character is found. This should not happen
    """
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            if posn in guard:
                return (x,y)
            
def take_step(grid: list[str], 
              guard_posn: tuple[int, int], 
              guard_sprite: 'str'
              ) -> tuple[str, tuple[int, int], bool]:
    """
    Moves a guard within a grid based on its current direction and handles obstacles.

    The function calculates the guard's next position based on its current position
    and direction. If the next position is within bounds and not blocked by an obstacle
    ('#'), it updates the guard's position. If blocked, the guard's sprite is updated
    to simulate a change in direction.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        guard_posn (tuple[int, int]): A tuple representing the current x and y coordinates of 
                                      the guard.
        guard_sprite (str): A character representing the guard's current direction, used to 
                            determine movement.

    Returns:
        tuple: A tuple containing:
            - The updated guard sprite (str), indicating the guard's new direction if it has 
              changed.
            - The new position (tuple[int, int]) of the guard.
            - A boolean indicating completion (or not) of the guard's path through the area. 
    """
    x, y = guard_posn
    delta_x, delta_y = guard_directions[guard_sprite]
    next_x = x + delta_x
    next_y = y + delta_y

    # Check whether the guard remains in the area
    if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid):
        potential_new_position = grid[next_y][next_x]
    else: # Guard has left the area and her path is complete
        return guard_sprite, guard_posn, True

    if potential_new_position != '#': # Guard moves forwards
        return guard_sprite, (next_x, next_y), False
    else: # There's an obstacle, "#"
        next_sprite_index = (guard.index(guard_sprite) + 1) % 4
        return guard[next_sprite_index], guard_posn, False

def add_obstacle(grid: list[str], obstacle_posn: tuple[int, int]) -> list[str] | None:
    """
    Adds an obstacle to a specified position in a grid, if the position can receive an obstacle.

    This function attempts to place an obstacle ('#') at the given coordinates in the grid.
    If the position is already occupied by a guard or an existing obstacle, the operation
    is aborted, and None is returned.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        obstacle_posn (tuple[int, int]): A tuple representing the x and y coordinates where
                                         the obstacle should be placed.

    Returns:
        list[str]: A new grid with the obstacle added, if the position is valid. 
        None: If the position is disallowed.
    """
    x, y = obstacle_posn
    new_grid = grid[:]
    disallowed_positions = guard + ['#']
    if new_grid[y][x] in disallowed_positions:
        return None

    else:
        original_line = new_grid[y]
        new_grid[y] = original_line[:x] + '#' + original_line[(x+1):]
        return new_grid

def add_to_path(path: dict[tuple[int, int], list[str]],
                guard_sprite: str,
                guard_posn: tuple[int, int]
                ) -> tuple[dict[tuple[int, int], list[str]], bool]:
    """
    Adds the current guard position and sprite to the path, indicating traversal.

    This function updates the path to record the guard's current position and direction.
    If the position and direction have been traversed before, it returns the unchanged path and 
    True to indicate redundancy; otherwise, it updates the path and returns False.

    Args:
        path (dict): A dictionary where keys are tuples representing positions (x, y) and
                     values are lists of guard sprites that have been at those positions.
        guard_sprite (str): A character representing the guard's current direction.
        guard_posn (tuple[int, int]): A tuple representing the current x and y coordinates of 
                                      the guard.

    Returns:
        tuple[dict, bool]: A tuple containing:
            - The updated path dictionary.
            - A boolean indicating whether the path at the current position and direction
              has been traversed before (True if it has, False otherwise).
    """
    # Check this subpath hasn't been traversed before
    try:
        if guard_sprite in path[guard_posn]:
            return path, True # We've done this before
        else: # It's a previous position but new direction
            path[guard_posn].append(guard_sprite)
    except KeyError: # We haven't been here before
        path[guard_posn] = [guard_sprite]
        
    return path, False

def find_guard_path(grid: list[str]
                    ) -> dict[tuple[int, int], list[str]] | None:
    """
    Determines the path of a guard moving through a grid until it completes a path or loops.

    This function tracks the guard's movement through a grid based on its initial position
    and direction. It records each position and direction in a path, returning the complete
    path if it terminates normally, or None if the path forms a loop.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        dict[tuple[int, int], list[str]]: A dictionary mapping each position (x, y) to
                                          a list of guard directions previously encountered at 
                                          that position, if the path is finite.
        None: If the path turns into a loop.
    """
    guard_posn = find_guard(grid)
    guard_sprite = grid[guard_posn[1]][guard_posn[0]]

    complete = False
    path = {}
    while not complete:
        path, repeated_path = add_to_path(path, guard_sprite, guard_posn)
        if repeated_path: # It's a loop
             return None

        guard_sprite, guard_posn, complete = take_step(grid, 
                                                       guard_posn, 
                                                       guard_sprite
                                                       )    
    
    return path

def run(grid: list[str]) -> tuple[int, int]:
    """
    Simulates the movement of a guard through a grid and evaluates the impact of adding 
    obstacles.

    This function calculates the length of the guard's path without obstacles and then attempts
    to add obstacles at each position in the grid. It counts how many obstacle placements result
    in the guard's path forming a loop.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        tuple[int, int]: A tuple containing:
            - The length of the guard's path without any obstacles (part1_result).
            - The number of successful obstacle placements that cause the guard's path to loop
              (successful_obstacles).
    """
    path = find_guard_path(grid)
    part1_result = len(path)

    # Part 2
    successful_obstacles = 0
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            # I could have made this much faster by checking for previous subpaths. But I didn't
            new_grid = add_obstacle(grid, (x,y))
            if new_grid: # If there wasn't already an obstacle here
                print('Running position', f'({x}, {y})')
                path = find_guard_path(new_grid)
                if not path:
                    successful_obstacles += 1

    return part1_result, successful_obstacles

guard_directions = {'^': (0, -1),
                    '>': (1, 0),
                    'v': (0, 1),
                    '<': (-1, 0)
                    }
guard = list(guard_directions.keys())

inputfile = Path('day06.txt')
data = read_inputfile(inputfile)
part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 4789:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 1304:
    print('PASS')