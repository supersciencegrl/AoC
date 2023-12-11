square = """.....
.S-7.
.|.|.
.L-J.
....."""
square = square.split('\n')

complex_square = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
complex_square = complex_square.split('\n')

twist = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
twist = twist.split('\n')

complex_twist = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
complex_twist = complex_twist.split('\n')

import sys
sys.setrecursionlimit(100_000)

with open('Day10.txt', 'rt') as fin:
    input_text = [t.replace('\n', '') for t in fin.readlines()]

def get_adjacent_path(coord, char):
    x, y = coord

    if char == '.':
        return None
    elif char == '|':
        return (x,y-1),(x,y+1)
    elif char == '-':
        return (x-1,y),(x+1,y)
    elif char == 'L':
        return (x,y-1),(x+1,y)
    elif char == 'J':
        return (x-1,y),(x,y-1)
    elif char == '7':
        return (x-1,y),(x,y+1)
    elif char == 'F':
        return (x,y+1),(x+1,y)
    elif char == 'S':
        return 'end'

def get_next_position(coord, char, previous_coord):
    adjacent_path = get_adjacent_path(coord, char)

    if adjacent_path is None:
        return None

    if previous_coord not in adjacent_path:
        return None
    
    for possible_coord in adjacent_path:
        if possible_coord != previous_coord:
            return possible_coord

def find_S(grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 'S':
                return (x,y)

def walk(grid, coord, previous_coord, distances, distance):
    if coord is None: # not a loop
        return None, None
    
    if coord not in distances:
        next_position = get_next_position(coord,
                                          grid[coord[1]][coord[0]],
                                          previous_coord
                                          )
        if next_position is None:
            return None, None
        distances[coord] = distance
        return walk(grid, next_position, coord, distances, distance+1)
    else:
        return distances, previous_coord

def find_paths(grid):
    (Sx,Sy) = find_S(grid)
    
    routes = {}
    route = 0
    completed_start_points = []
    for coord in [(Sx,Sy-1),(Sx+1,Sy),(Sx,Sy+1),(Sx-1,Sy)]:
        if coord not in completed_start_points:
            previous_coord = (Sx,Sy)
            if grid[coord[1]][coord[0]] != '.':
                distances, last_coord = walk(grid, coord, (Sx,Sy), {(Sx,Sy):0}, 1)
                if distances is not None:
                    completed_start_points.append(last_coord)
                    routes[route] = distances
                    route += 1

    furthest_point_distances = [len(v) for v in routes.values()]
    result = int(max(furthest_point_distances)/2)

    return routes, result

routes, part1_result = find_paths(input_text)
print('Part 1 result:', part1_result)
if part1_result == 7093:
    print('PASS')
