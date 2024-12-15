from pathlib import Path

example1 = """########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    <^^>>>vv<v>>v<<"""
example1 = example1.split()

example2 = """##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########

    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
example2 = example2.split()

def read_inputfile(inputfile: Path) -> str:
    """
    Reads a text file and returns its contents, with leading/trailing whitespace removed.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        str: A string representing the file contents, with leading/trailing whitespace removed. 
    """
    with open(inputfile, 'rt') as fin:
        data = fin.readlines()

    return [line.strip() for line in data]

def parse_data(data: list[str]) -> tuple[list[str], str]:
    """
    Parses input data into a grid sequence and movement instructions.

    This function processes a list of strings, separating them into grid 
    lines and movement instructions. Lines containing the '#' (wall) character 
    are considered part of the grid, while non-empty lines without walls are 
    combined into a single movement string.

    Args:
        data (list[str]): A list of strings where each string may represent 
                          a line of the grid or a part of the movement 
                          sequence.

    Returns:
        tuple[list[str], str]: A tuple containing:
            - A list of strings representing the grid.
            - A single string representing the concatenated movement 
              instructions.
    """
    grid = []
    movements = []

    for line in data:
        if '#' in line:
            grid.append(line)
        elif line:
            movements.append(line)

    # Convert movements to a single string
    movements = ('').join(movements)

    return grid, movements

def find_robot(grid: list[str]) -> tuple[int, int]:
    """
    Locates the position of a robot within a grid.

    This function searches through a grid to find the coordinates of the robot,
    which is represented by the '@' character. It returns the position as a 
    tuple of indices.

    Args:
        grid (list[str]): A list of strings representing the grid, where each 
                          string is a row. Each character in the grid represents 
                          a grid position (wall, box, space, or robot).

    Returns:
        tuple[int, int]: A tuple containing the x and y coordinates of the 
                         robot in the grid.
        None: If the robot is not found. This should not happen. 
    """
    for x, line in enumerate(grid):
        for y, posn in enumerate(line):
            if posn == '@': # Robot sprite
                return (x,y)

def get_sprite_in_front(grid: list[str],
                        posn: tuple[int, int],
                        direction: str
                        ) -> tuple[str, int, int]:
    """
    Determines the sprite and position directly in front of a given position 
    in a specified direction.

    This function calculates the position directly in front of the current 
    position based on the given direction. It returns the sprite at that 
    position, along with its coordinates.

    Args:
        grid (list[str]): A list of strings representing the grid, where each 
                          string is a row.
        posn (tuple[int, int]): A tuple of integers representing the current x 
                                and y coordinates.
        direction (str): A string representing the direction to look in, where 
                         valid keys correspond to entries in the `directions` 
                         dictionary.

    Returns:
        tuple[str, tuple[int, int]]: A tuple containing:
            - The character (sprite) found at the next position in the 
              specified direction.
            - A tuple of the next x and y coordinates.
    """
    x, y = posn
    delta_x, delta_y = directions[direction]
    next_x = x + delta_x
    next_y = y + delta_y
    sprite = grid[next_y][next_x]

    return sprite, (next_x, next_y)

def move(grid: list[str],
         posn: tuple[int, int],
         direction: str
         ) -> tuple[list[str], tuple[int, int]]:
    """
    Moves a robot within a grid in a specified direction, handling obstacles 
    and movable boxes.

    This function attempts to move the robot from its current position in the 
    given direction. It does not move if a wall ('#') is obstructing, and moves 
    boxes ('O') if they are not blocked. The grid is updated to reflect the 
    new positions of any moved objects.

    Args:
        grid (list[str]): A list of strings representing the grid, where each 
                          string is a row. Characters in the grid include '.' 
                          for empty space, '#' for walls, and 'O' for boxes.
        posn (tuple[int, int]): A tuple representing the current x and y 
                                coordinates of the robot.
        direction (str): A string representing the direction to move, where 
                         valid keys correspond to entries in the `directions` 
                         dictionary.

    Returns:
        tuple[list[str], tuple[int, int]]: A tuple containing:
            - The updated grid after the move attempt.
            - A tuple of the new x and y coordinates of the robot after the 
              move.

    Note: This function does not update the position of the robot sprite, since 
          it is deemed not to matter. 
    """
    # Find out about the potential next position
    sprite_in_front, next_posn = get_sprite_in_front(grid, posn, direction)
    next_x, next_y = next_posn

    if sprite_in_front == '#': # Nothing can move
        return grid, posn
    elif sprite_in_front == 'O': # Box in front: decide whether we move
        sprite_posn = next_posn
        while True:
            next_sprite, sprite_posn = get_sprite_in_front(grid, sprite_posn, direction)
            sprite_in_front = f'{sprite_in_front}{next_sprite}'
            if next_sprite != 'O': # End of decision-making
                break
        if sprite_in_front.endswith('#'): # Nothing can move
            return grid, posn
        else: # We move a series of at least 1 boxes, and the robot
            # Update the last place pushed to be a box
            sprite_x, sprite_y = sprite_posn
            sprite_line = grid[sprite_y]
            grid[sprite_y] = sprite_line[:sprite_x] + 'O' + sprite_line[sprite_x+1:]
            # Update the position the robot moved to
            robot_line = grid[next_y]
            grid[next_y] = robot_line[:next_x] + '.' + robot_line[next_x+1:]

            return grid, next_posn
    else:
        return grid, next_posn # Only the robot moves

def calculate_gps_sum(grid: list[str]) -> int:
    """
    Calculates the sum of GPS coordinates for boxes ('O') in a grid.

    This function scans a grid to find all positions marked with 'O' and 
    calculates a GPS coordinate for each. The GPS coordinate is calculated 
    as (100 * row_index) + column_index. It then returns the sum of all 
    GPS coordinates.

    Args:
        grid (list[str]): A list of strings representing the grid, where each 
                          string is a row. The character 'O' represents a box 
                          whose GPS coordinate is to be calculated.

    Returns:
        int: The sum of all GPS coordinates for the boxes ('O') found in the 
             grid.
    """
    result = 0
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            if posn == 'O':
                # Calculate GPS coordinate and add it to the running total
                gps_coordinate = (100 * y) + x
                result += gps_coordinate
    
    return result

def run(data: list[str]) -> int:
    """
    Simulates robot movements within a grid and calculates the sum of GPS 
    coordinates for boxes.

    This function first parses the input data to separate the grid and the 
    movement instructions.
    It then finds the initial position of the robot and processes each 
    movement to update the grid.
    Finally, it calculates and returns the sum of GPS coordinates for all 
    boxes ('O') in the grid after completing the movements.

    Args:
        data (list[str]): A list of strings where each string may represent 
                          a line of the grid or a part of the movement 
                          sequence.

    Returns:
        int: The sum of GPS coordinates for all boxes ('O') in the grid after 
             executing all movements.
    """
    # Split the input into the map and the movement instructions
    grid, movements = parse_data(data)
    robot = find_robot(grid)

    # Execute all movement instructions
    for movement in movements:
        grid, robot = move(grid, robot, movement)
    
    part1_result = calculate_gps_sum(grid)

    return part1_result

inputfile = Path(r"day15.txt")
data = read_inputfile(inputfile)

directions = {'<': (-1, 0),
              'v': (0, 1),
              '>': (1, 0),
              '^': (0, -1)
              }

part1_result = run(data)

print('Day 1:', part1_result)
if part1_result == 1463715:
    print('PASS')