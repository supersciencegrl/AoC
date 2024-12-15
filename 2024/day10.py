example = '''89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732'''
example = example.split()

def take_step(grid, current_posn):
    x, y = current_posn
    score = 0
    elevation = int(grid[y][x])

    if elevation == 9: # Summit
        score += 1

    for delta_x, delta_y in directions:
        next_x = x + delta_x
        next_y = y + delta_y

        in_grid = (0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid))

        if in_grid and int(grid[next_y][next_x]) == elevation + 1: 
            return take_step(grid, (next_x, next_y))
        
    return score

def find_trailheads(grid: list[str]) -> dict[tuple[int, int], int]:
    trailheads = {}
    for y, line in enumerate(grid):
        for x, posn in enumerate(line):
            if posn == '0':
                trailheads[(x,y)] = 0
    
    return trailheads

directions = [(-1, 0),
              (0, -1),
              (1, 0),
              (0, 1)
              ]

def run(grid):
    trailheads = find_trailheads(grid)
    for trailhead in trailheads.keys():
        trailheads[trailhead] = take_step(grid, trailhead)
    
    return trailheads