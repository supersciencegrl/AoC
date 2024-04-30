import sys

sys.setrecursionlimit(1_000_000)

example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
example = example.split('\n')

def take_step(grid, initial_pos):
    ix,iy = initial_pos

    if grid[iy][ix] == '<':
        return [(ix-1,iy)]
    elif grid[iy][ix] == 'v':
        return [(ix,iy+1)]
    elif grid[iy][ix] == '>':
        return [(ix+1,iy)]
    elif grid[iy][ix] == '^':
        return [(ix,iy-1)]
    else:
        positions = []
        directions = [(ix-1,iy),(ix,iy+1),(ix+1,iy),(ix,iy-1)]
        next_positions = []
        for (dx,dy) in directions:
            try:
                if grid[dy][dx] != '#':
                    next_positions.append((dx,dy))
            except IndexError:
                pass

        return next_positions

def find_paths(grid, all_paths, final_paths, end):
    if not all_paths:
        return final_paths
    new_paths = []
    print(len(final_paths))
    for path in all_paths:
        if end in path:
            final_paths.append(path)
        else:
            #print(path[-1])
            next_steps = take_step(grid, path[-1]) # Take a step from the last known position
            if next_steps:
                for (nx,ny) in next_steps:
                    if grid[ny][nx] != '#' and (nx,ny) not in path:
                        new_paths.append(path + [(nx,ny)])

    return find_paths(grid, new_paths, final_paths, end)

def find_termini(grid):
    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), len(grid))

    return start, end

def run(grid):
    start, end = find_termini(grid)
    all_paths = find_paths(grid, [[start]], [], end)

    return all_paths

all_paths = run(example)
print('All paths:', all_paths)
