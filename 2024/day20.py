from collections import deque
from pathlib import Path

example = """###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############"""
example = example.split()

def read_inputfile(inputfile: Path) -> list[str]:
    """
    Reads a text file and returns its contents as a list of strings, with leading/trailing 
    whitespace removed from each string.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        list[str]: A list of strings representing the file contents, with leading/trailing 
                   whitespace removed from each string. 
    """
    with open(inputfile, 'rt') as fin:
        data = fin.readlines()

    return [line.strip() for line in data]

def find_start_and_end(grid: list[str]) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Finds the coordinates of the start ('S') and end ('E') positions in a grid.

    This function scans a grid represented as a list of strings to locate the positions
    marked by 'S' (start) and 'E' (end). It returns the coordinates of these positions
    as tuples.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
                          The characters 'S' and 'E' indicate the start and end positions, 
                          respectively.

    Returns:
        tuple[tuple[int, int], tuple[int, int]]: A tuple containing two tuples:
            - The first tuple represents the (x, y) coordinates of the start position.
            - The second tuple represents the (x, y) coordinates of the end position.
    """
    start = None
    end = None
    for y, row in enumerate(grid):
        for x, posn in enumerate(row):
            if posn == 'S': # Start
                start = (x, y)
            elif posn == 'E': # End
                end = (x, y)
        if start and end:
            return start, end

def validate_position(grid: list[str], 
                      posn: tuple[int, int]
                      ) -> bool:
    """
    Validates whether a given position is within the internal area of a grid, excluding borders.

    This function checks if the specified position (x, y) is located within the interior of the 
    grid, ensuring it is also not on the border. The interior is defined as the area within the 
    grid that is not on the border.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        posn (tuple[int, int]): A tuple of integers representing the (x, y) coordinates to 
                                validate.

    Returns:
        bool: True if the position is within the internal part of the grid; False if it is on the 
              border.
    """
    x, y = posn
    boundary = {'x_min': 1, 'x_max': len(grid[0]) - 1,
                'y_min': 1, 'y_max': len(grid) - 1
                }
        
    if boundary['x_min'] <= x < boundary['x_max'] and \
        boundary['y_min'] <= y < boundary['y_max']:
        return True
    else:
        return False

# Ok we're going to do one of those bfs things
def bfs(grid: list[str], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Performs a breadth-first search (BFS) on a grid to find the shortest path from a start to an 
    end position.

    This function uses a queue to explore the grid from the start position, moving in all possible 
    directions until the end position is reached. It returns the path taken as a list of coordinates, 
    or None if no path exists. Positions marked with '#' are walls that cannot be traversed.

    Args:
        grid (list[list[str]]): A 2D list representing the grid, where each element is a character.
                                The character '#' represents a wall.
        start (tuple[int, int]): A tuple representing the starting coordinates (x, y) in the grid.
        end (tuple[int, int]): A tuple representing the ending coordinates (x, y) in the grid.

    Returns:
        list[tuple[int, int]]: A list of tuples representing the path from the start to the end 
                               coordinates, in order.
        None: If no path is found.
    """
    queue = deque([start])
    path_so_far = {start: None} # dict of format {posn: previous_posn}

    while queue:
        current_posn = queue.popleft()
        x, y = current_posn
        # If we finished, return the path we took from start to end
        if current_posn == end:
            path = []
            while current_posn:
                path.append(current_posn)
                current_posn = path_so_far[current_posn]
            return path[::-1]

        for direction in directions:
            delta_x, delta_y = direction
            next_x = x + delta_x
            next_y = y + delta_y

            # Figure out whether we can move this way
            if validate_position(grid, (next_x, next_y)) and \
                grid[next_y][next_x] != '#':
                possible_next_step = (next_x, next_y)
                # If we haven't been here, move & record where we've been
                if possible_next_step not in path_so_far:
                    queue.append(possible_next_step)
                    path_so_far[possible_next_step] = current_posn

def find_cheats(grid: list[str]) -> list[list[tuple[int, int], tuple[int, int]]]:
    """
    Identifies potential "cheat" moves within a grid, where a move bypasses a wall.

    This function scans the grid to find pairs of adjacent positions where the first is a wall
    ('#') and the second is not. It returns a list of such pairs, representing "cheat" moves 
    of length 2 ps, that bypass walls.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
                          The character '#' represents a wall.

    Returns:
        list[list[tuple[int, int], tuple[int, int]]]: A list of pairs, where each pair consists of
        two tuples representing coordinates in the grid. Each pair indicates a move from a wall
        to a viable path position.
    """
    cheats = []
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            for direction in directions:
                delta_x, delta_y = direction
                next_x = x + delta_x
                next_y = y + delta_y
                # Check cheat is within bounds
                if validate_position(grid, (x, y)) and \
                    validate_position(grid, (next_x, next_y)):
                    cheat = [(x, y), (next_x, next_y)]
                    # Check cheat goes from wall to non-wall and hasn't been done before
                    if posn == '#' and grid[next_y][next_x] != '#' and cheat not in cheats:
                        cheats.append(cheat)

    return cheats

def add_cheat(grid: list[str], 
              start: tuple[int, int], 
              end: tuple[int, int], 
              cheat: list[tuple[int, int], tuple[int, int]]
              ) -> int | None:
    """
    Modifies a grid by applying a "cheat" move to potentially reduce the path length between two 
    points.

    This function replaces specified "cheat" positions in the grid with passable terrain ('.') and
    uses breadth-first search (BFS) to find a path from the start to the end position. It checks 
    that the path includes a direct step from the first to the second cheat position, indicating a 
    successful shortcut, and returns the length of the path if successful.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.
        start (tuple[int, int]): The starting coordinates (x, y) for the pathfinding.
        end (tuple[int, int]): The ending coordinates (x, y) for the pathfinding.
        cheat (list[tuple[int, int], tuple[int, int]]): A list containing two tuples, each representing
                                                        the coordinates of the positions to be modified
                                                        for the cheat move.

    Returns:
        int: The length of the path from start to end if the cheat allows a direct step between
             the specified positions
        None: If the path does not include the cheat.
    """
    this_grid = grid[:]
    # Replace cheat0 position with '.'
    cheat0_x, cheat0_y = cheat[0]
    line = this_grid[cheat0_y]
    this_grid[cheat0_y] = line[:cheat0_x] + '.' + line[cheat0_x+1:]

    # Find shortest path within new grid
    path = bfs(this_grid, start, end)
    try:
        cheat0_index = path.index(cheat[0])
        cheat1_index = path.index(cheat[1])
    except ValueError: # The cheat wasn't included in the path
        return None
    if cheat1_index - cheat0_index == 1: # Stepped from Cheat 0 to Cheat 1
        return len(path) - 1 # Travel time in ps

def run(grid: list[str]) -> int:
    """
    Calculates the potential time savings from applying "cheats" in a grid and returns the total time
    saved for significant shortcuts.

    This function finds the shortest path from the start to the end of the grid without any cheats,
    then evaluates potential cheats to see how much time they save over the baseline path. It counts
    the number of significant time savings (100 ps or more) and returns the total count.

    Args:
        grid (list[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        int: The total number of significant time savings (100 ps or more) from applying cheats.
    """
    start, end = find_start_and_end(grid)
    baseline_path = bfs(grid, start, end) # Travel without cheating
    baseline = len(baseline_path) - 1 # Baseline travel time in ps

    results = []
    cheats = find_cheats(grid)
    for cheat in cheats:
        time = add_cheat(grid, start, end, cheat)
        if time:
            results.append(baseline - time)
    
    result_dict = {k: results.count(k) for k in sorted(results)}
    part1_result = sum(result_dict[x] for x in result_dict.keys() if x >= 100)

    return part1_result

directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

inputfile = Path(r"day20.txt")
data = read_inputfile(inputfile)
part1_result = run(data)

print('Part 1:', part1_result)
if part1_result == 1323:
    print('PASS')