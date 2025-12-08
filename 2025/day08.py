from deprecation import deprecated
from itertools import combinations
import math
from pathlib import Path

example = """162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    542,29,236
    431,825,988
    739,650,466
    52,470,668
    216,146,977
    819,987,18
    117,168,530
    805,96,715
    346,949,466
    970,615,88
    941,993,340
    862,61,35
    984,92,344
    425,690,689"""
example = [line.strip() for line in example.split('\n')]

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

def parse_coords(data: list[str]) -> list[tuple[int, int, int]]:
    """
    Parse a list of comma-separated coordinate strings into 3D integer tuples.

    Converts each input string like "x,y,z" into a tuple of three integers
    (x, y, z). 

    Args:
        data (list[str]): List with each item containing three int-like strings
            separated by commas, e.g., ["10,11,12", "1,2,4"].

    Returns:
        list[tuple[int, int, int]]: List of 3D coordinate tuples.

    Raises:
        ValueError: If any string does not contain exactly three comma-separated
            parts or if any part cannot be converted to int.
    """
    return [tuple(map(int, coords.split(','))) for coords in data]

@deprecated
def euclidean_distance(box1: tuple[int, int, int], box2: tuple[int, int, int]) -> float:
    """
    Compute the Euclidean distance between two 3D points.
    NOTE: Deprecated because apparently you can just use `math.dist`. 

    Args:
        box1 (tuple[int, int, int]): First point (x1, y1, z1).
        box2 (tuple[int, int, int]): Second point (x2, y2, z2).

    Returns:
        float: The Euclidean distance between box1 and box2.
    """
    x1, y1, z1 = box1
    x2, y2, z2 = box2

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

def sort_junction_pairs(coords: list[tuple[int, int, int]]
                        ) -> list[tuple[tuple[int, int], float]]:
    """
    Generate all unique index pairs of coordinates with their Euclidean distances, 
    sorted ascending.

    For a list of 3D coordinates, computes the distance for every unordered
    pair (i, j) with i < j, and returns a list of ((i, j), distance) tuples
    sorted by distance from smallest to largest.

    Args:
        coords (list[tuple[int, int, int]]): List of 3D integer coordinates.

    Returns:
        list[tuple[tuple[int, int], float]]: A list where each element is
            ((i, j), d), with i < j the indices in coords and 
            d = math.dist(coords[i], coords[j]), sorted by ascending d.
    """
    pairs = []
    for idx1, idx2 in combinations(range(len(coords)), 2):
        box1, box2 = coords[idx1], coords[idx2]
        distance = math.dist(box1, box2)
        pairs.append(((idx1, idx2), distance))
    
    pairs.sort(key = lambda x: x[1]) # Sort by distance

    return pairs

def connect_junctions(coords: list[tuple[int, int, int]], 
                      part2: bool, 
                      max_connections: int = 1000,
                      ) -> tuple[
                          list[set[tuple[int, int, int]]], 
                          tuple[int, int]
                          ]:
    """
    Connect junctions by merging nearest pairs into circuits and return the result.
    NOTE: The puzzle asks for number of connections in Part 1; it actually wants number of 
        attempted connections (`trials`). 

    Processes all unordered pairs of coordinate indices sorted by ascending Euclidean
    distance. Each junction starts in its own circuit (a set of indices). For each pair, 
    if the two junctions belong to different circuits, merges the smaller circuit into the 
    larger and updates membership. The loop stops when:
    - if part2 is True: all junctions are connected in one non-empty circuit, or
    - if part2 is False: the number of pair trials reaches max_connections.

    Args:
        coords (list[tuple[int, int, int]]): 3D junction coordinates.
        part2 (bool): If True, keep merging until a single circuit remains.
            If False, stop after max_connections pair trials.
        max_connections (int): Maximum number of pair trials to consider when
            part2 is False. The function breaks after this many trials, even if
            some trials do not result in a merge.

    Returns:
        tuple[list[set[tuple[int, int, int]]], tuple[int, int]]:
            - circuits: List of circuits, each a set of coordinate tuples. 
            - last_pair: The last processed pair of junction indices (i, j).
    """
    # Each junctions starts off as its own circuit (a set)
    len_coords = len(coords)
    pairs = sort_junction_pairs(coords)
    circuits: list[set[int]] = [{x} for x in range(len_coords)]
    junction_circuit_map = {i:i for i in range(len_coords)} # node: circuit_index

    trials = 0
    for (box1, box2), _ in pairs:
        trials += 1
        last_pair = (box1, box2)
        circuit1, circuit2 = junction_circuit_map[box1], junction_circuit_map[box2]
        if circuit1 == circuit2: # Already connected
            continue

        elif len(circuits[circuit1]) < len(circuits[circuit2]):
            circuit1, circuit2 = circuit2, circuit1 # Put larger first for fewer moves

        # Merge circuit2 into circuit1
        for junction in circuits[circuit2]:
            circuits[circuit1].add(junction)
            junction_circuit_map[junction] = circuit1
        circuits[circuit2].clear() # Circuit 2 is now empty of junctions

        if part2:
            non_empty = sum(1 for c in circuits if c)
            if non_empty == 1: # If 1 circuit contains every junction, stop working
                break
        else: # Part 1
            if trials >= max_connections: # Stop working after max_connections trials
                break

    return circuits, last_pair

def part1(circuits: list[set[int]]) -> int:
    """
    Compute the product of the sizes of the three largest circuits.

    Takes a list of circuits (each a set of junction indices), determines their sizes, and 
    returns the product of the three largest sizes.

    Args:
        circuits (list[set[int]]): Circuits represented as sets of junction indices.

    Returns:
        int: The product of the sizes of the three largest circuits. 
    """
    circuit_lengths = [len(circuit) for circuit in circuits]
    sorted_lengths = sorted(circuit_lengths, reverse = True)

    return math.prod(sorted_lengths[:3])

def run(data: list[str], max_connections: int = 1_000) -> tuple[int, int]:
    """
    Parse coordinates, connect junctions under two modes, and return both results.

    Workflow:
    - Parses the input strings into 3D integer coordinates via parse_coords.
    - Part 1: Connects junctions considering up to `max_connections` pair trials
    (nearest-first) and computes the product of the sizes of the three largest
    resulting circuits using part1.
    - Part 2: Connects junctions until the entire set is in a single circuit,
    then returns the product of the x-coordinates of the last processed pair
    of indices (box1, box2).

    Args:
        data (list[str]): Lines of "x,y,z" coordinate strings.
        max_connections (int): Upper bound on the number of pair trials to
            consider for Part 1 when connecting junctions.

    Returns:
        tuple[int, int]: (part1_result, part2_result) where:
            - part1_result is the product of the three largest circuit sizes
            after at most `max_connections` trials.
            - part2_result is coords[box1][0] * coords[box2][0], where (box1, box2)
            is the last pair processed when connecting until a single circuit remains.

    Raises:
        ValueError: If input lines cannot be parsed as three comma-separated ints.
    """
    coords = parse_coords(data)

    circuits_part1, _ = connect_junctions(coords, part2 = False, max_connections = max_connections)
    part1_result = part1(circuits_part1)

    _, (box1, box2) = connect_junctions(coords, part2 = True)
    part2_result = coords[box1][0] * coords[box2][0]

    return part1_result, part2_result

inputfile = Path('day08.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(example)

print('Day 1:', part1_result)
if part1_result == 121770:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 7893123992:
    print('PASS')