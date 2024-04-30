example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
example = example.split('\n')

with open('Day21.txt', 'rt') as fin:
    input_text = fin.readlines()

def find_S(grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 'S':
                return (x,y)

def take_step(init_coord, grid) -> set:
    (ix,iy) = init_coord

    next_positions = [(ix,iy-1),(ix+1,iy),(ix,iy+1),(ix-1,iy)]
    final_positions = set()
    for next_position in next_positions:
        (nx,ny) = next_position
        try:
            if grid[ny][nx] != '#':
                final_positions.add((nx,ny))
        except IndexError:
            pass

    return final_positions

def run(grid, num_steps: int):
    initial_positions = set((find_S(grid),)) # Initial position

    for step in range(num_steps):
        final_positions = set()
        for coord in initial_positions:
            current_positions = take_step(coord, grid)
            final_positions.update(current_positions)
            initial_positions = final_positions

    result = len(final_positions)

    return result

part1_result = run(input_text, 64)
print('Part 1 result:', part1_result)
if part1_result == 3639:
    print('PASS')
