example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
example = example.split('\n')

with open('Day11.txt', 'rt') as fin:
    input_text = fin.readlines()

def print_grid(grid):
    for row in grid:
        print(row)

def apply_gravity(grid):
    new_grid = grid[:]
    cols_to_expand = []
    row_length = len(new_grid[0])
    for x in range(row_length):
        if '#' not in [row[x] for row in new_grid]:
            cols_to_expand.append(x)

    rows_to_expand = []
    for y, row in enumerate(new_grid):
        for pos in cols_to_expand[::-1]:
            row = row[:pos] + '.' + row[pos:]
            new_grid[y] = row
        if '#' not in row:
            rows_to_expand.append(y)

    row_length += len(cols_to_expand)
    for pos in rows_to_expand[::-1]:
        new_grid = new_grid[:pos] + ['.' * row_length] + new_grid[pos:]

    return new_grid, rows_to_expand, cols_to_expand

def find_galaxies(grid):
    galaxies = []
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == '#':
                galaxies.append((x,y))

    return galaxies

def find_total_path_length(galaxy1, galaxy2, rows_to_expand, cols_to_expand, expansion):
    x1,y1 = galaxy1
    x2,y2 = galaxy2
    initial_distance = abs(x1-x2) + abs(y1-y2)

    x_range = list(range(*sorted([x1,x2])))
    x_expansion = len([x for x in cols_to_expand if x in x_range])
    

    y_range = list(range(*sorted([y1,y2])))
    y_expansion = len([y for y in rows_to_expand if y in y_range])

    distance = initial_distance + ((expansion-1) * (x_expansion + y_expansion))
    #print(f'{initial_distance=}, {galaxy1}, {galaxy2}, {x_expansion+y_expansion}')
    #print(f'{distance=}')

    return distance

def find_all_paths(grid, galaxies, rows_to_expand, cols_to_expand, expansion, part2=False):
    all_distances = []
    
    for n, galaxy in enumerate(galaxies):
        remaining = galaxies[n+1:]
        for galaxy2 in remaining:
            if not part2:
                distance = find_path_length(galaxy, galaxy2)
            else:
                distance = find_total_path_length(galaxy, galaxy2, rows_to_expand, cols_to_expand, expansion)
            all_distances.append(distance)

    return all_distances

def run(grid, expansion):
    new_grid, new_rows, new_cols = apply_gravity(grid)
    
    galaxies = find_galaxies(grid)
    all_distances_part2 = find_all_paths(grid, galaxies, new_rows, new_cols, expansion, part2=True)
    result = sum(all_distances_part2)

    return result

#part1_result, part2_result = run(input_text, expansion=1_000_000)
part1_result = run(input_text, expansion=2)
part2_result = run(input_text, expansion=1_000_000)
print('Part 1 result:', part1_result)
if part1_result == 9591768:
    print('PASS')
print('Part 2 result:', part2_result)
if part2_result >= 773686136407:
    print('NOPE')
