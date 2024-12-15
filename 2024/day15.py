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
    grid = []
    movements = []

    for line in data:
        if '#' in line:
            grid.append(line)
        elif line:
            movements.append(line)

    movements = ('').join(movements)

    return grid, movements

def find_robot(grid: list[str]) -> tuple[int, int]:
    for x, line in enumerate(grid):
        for y, posn in enumerate(line):
            if posn == '@': # Robot sprite
                return (x,y)

def get_sprite_in_front(grid: list[str],
                        posn: tuple[int, int],
                        direction: str
                        ) -> tuple[str, int, int]:
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
    sprite_in_front, next_posn = get_sprite_in_front(grid, posn, direction)
    next_x, next_y = next_posn

    if sprite_in_front == '#':
        return grid, posn
    elif sprite_in_front == 'O':
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
        return grid, next_posn

def calculate_gps_sum(grid: list[str]) -> int:
    result = 0
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            if posn == 'O':
                print(x+1, y+1)
                gps_coordinate = (100 * y) + x
                result += gps_coordinate
    
    return result

def run(data):
    grid, movements = parse_data(data)
    robot = find_robot(grid)

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