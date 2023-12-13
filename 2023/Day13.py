example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

with open('Day13.txt', 'rt') as fin:
    input_text = fin.read()

def resolve_patterns(input_string):
    patterns = [pattern.split('\n') for pattern in input_string.split('\n\n')]

    return patterns

def resolve_possible_sigma(possible_sigma):
    if len(possible_sigma) > 1:
        raise
    elif len(possible_sigma) == 1:
        sigma = possible_sigma[0]
    else:
        sigma = None

    return sigma

def find_vertical_sigma(pattern):
    possible_sigma = list(range(1, len(pattern[0])))
    for line in pattern:
        for i in possible_sigma[::-1]:
            if i < (len(line)+1)/2:
                chunk = line[:i]
                if not line.startswith(f'{chunk}{chunk[::-1]}'):
                    possible_sigma.remove(i)
            else:
                chunk_length = len(line) - i
                chunk = line[-chunk_length:]
                if not line.endswith(f'{chunk[::-1]}{chunk}'):
                    possible_sigma.remove(i)

    sigma = resolve_possible_sigma(possible_sigma)

    return sigma

def find_horizontal_sigma(pattern):
    possible_sigma = list(range(1, len(pattern)))
    width = len(pattern[0])
    for i in range(width):
        column = ('').join([line[i] for line in pattern])
        for i in possible_sigma[::-1]:
            if i < (len(pattern)+1)/2:
                chunk = column[:i]
                if not column.startswith(f'{chunk}{chunk[::-1]}'):
                    possible_sigma.remove(i)
            else:
                chunk_length = len(pattern) - i
                chunk = column[-chunk_length:]
                if not column.endswith(f'{chunk[::-1]}{chunk}'):
                    possible_sigma.remove(i)

    sigma = resolve_possible_sigma(possible_sigma)

    return sigma

def run(input_string):
    patterns = resolve_patterns(input_string)

    horizontals = []
    verticals = []
    for pattern in patterns:
        if '' in pattern:
            pattern.remove('')
        sigma = find_horizontal_sigma(pattern)
        if sigma:
            horizontals.append(sigma)
        sigma = find_vertical_sigma(pattern)
        if sigma:
            verticals.append(sigma)

    result = sum(verticals) + 100*sum(horizontals)

    return result

part1_result = run(input_text)
print('Part 1 result:', part1_result)
if part1_result = 32035:
    print('PASS')
