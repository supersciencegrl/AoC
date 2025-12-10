from collections import defaultdict
from itertools import combinations
from pathlib import Path

example = """7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3"""
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

def parse_coords(data: list[str]) -> list[tuple[int, int]]:
    """
    Parse a list of comma-separated "x,y" strings into 2D integer coordinate tuples.

    Args:
        data (list[str]): List of strings, each containing two integers separated by a comma,
            e.g., ["12,10", "9,7"].

    Returns:
        list[tuple[int, int]]: List of 2D coordinate tuples.

    Raises:
        ValueError: If any string does not contain exactly two comma-separated parts
            or if either part cannot be converted to an integer.
    """
    return [tuple(map(int, item.split(','))) for item in data]

def calculate_area(tile1: tuple[int, int], tile2: tuple[int, int]) -> int:
    """
    Compute the area (in grid tiles) of the axis-aligned rectangle spanned by two corners.

    Treats tile1 and tile2 as opposite corners of a rectangle on a discrete square
    grid where coordinates refer to tile centers. The area counts all tiles within
    the inclusive bounds from x1..x2 and y1..y2, hence the +1 terms.

    Args:
        tile1 (tuple[int, int]): One corner of the rectangle as (x1, y1).
        tile2 (tuple[int, int]): The opposite corner as (x2, y2).

    Returns:
        int: The area of the inclusive axis-aligned rectangle defined by the two corners.
    """
    x1, y1 = tile1
    x2, y2 = tile2

    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def get_max_area(red_tiles: list[tuple[int, int]],
                 green_spans: list[tuple[int, int]] | None
                 ) -> int:
    """
    Compute the maximum area of an axis-aligned rectangle defined by red-tile corners,
    optionally validating coverage against green spans (Part 2).

    For every unordered pair of red tiles, this function treats them as opposite corners
    and computes the inclusive rectangle area. It tracks the maximum area found. When
    green_tiles (row spans) are provided, candidate rectangles are accepted only if
    fully covered by the green spans (no white tiles).

    Args:
        red_tiles (list[tuple[int, int]]): List of red vertex coordinates (x, y).
            Each pair is treated as opposite corners of a rectangle.
        green_tiles (list[tuple[int, int]] | None): Optional list of row spans in the
            form (y, x_left, x_right), inclusive, representing green coverage per row.
            If provided, rectangles are validated against these spans (Part 2).

    Returns:
        int: The largest inclusive area among all candidate rectangles (when green spans 
        are provided, the largest that passes the coverage check.

    Notes:
        - This assumes a single continuous green span per row (no holes). If multiple
        spans per row are possible, adapt any_white_tiles accordingly.
        - Rectangles are axis-aligned; coordinates are integer grid positions.
    """
    # Sort pairs of coordinates
    max_area = 0 # Default
    spans_by_y = None
    if green_spans:
        spans_by_y = {y: (xl, xr) for (y, xl, xr) in green_spans}

    for idx1, idx2 in combinations(range(len(red_tiles)), 2):
        tile1, tile2 = red_tiles[idx1], red_tiles[idx2]
        area = calculate_area(tile1, tile2)
        if area <= max_area: # Not max area
            continue
        else: # Could be max area: check it doesn't have white tiles
            if green_spans: # Part 2
                reject = any_white_tiles(spans_by_y, tile1, tile2)
                if not reject: 
                    max_area = area
            else:
                max_area = area
    
    return max_area

def find_green_spans(red_tiles: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """
    Compute inclusive horizontal coverage spans for each scanline inside an axis-aligned 
    polygon defined by its vertex coordinates.

    This function:
    - Closes the polygon defined by red_tiles.
    - Extracts all vertical edges.
    - For each integer scanline y between the polygon's min_y and max_y (inclusive),
        collects the x positions where that scanline intersects vertical edges.
    - Assumes a single continuous interior per scanline ("no holes") and records the
        inclusive span as (y, x_left, x_right), where x_left = min(x_values) and
        x_right = max(x_values) for that scanline.

    Args:
        red_tiles (list[tuple[int, int]]): Ordered polygon vertices (x, y). 

    Returns:
        list[tuple[int, int, int]]: A list of inclusive spans per scanline in the form
            (y, x_left, x_right). Each tuple indicates that all tiles (x, y) with
            x_left <= x <= x_right are covered. Rows without coverage are omitted.

    Notes:
        - Edges are assumed axis-aligned and the polygon non-degenerate.
        - This implementation assumes "no holes", ie: a single, continuous span per row.
        - The per-row spans are not converted to explicit coordinates to save memory.
    """
    red = red_tiles[:] # Work on a copy
    red.append(red[0]) # Close the loop
    verticals = []

    min_y = max_y = red[0][1] # Default
    for (x1, y1), (x2, y2) in zip(red, red[1:]):
        min_y = min(min_y, y1, y2)
        max_y = max(max_y, y1, y2)
        # All lines are horizontal or vertical, so restrict as such
        if x1 == x2 and y1 != y2:
            if y2 < y1: # Put larger y-value first
                y1, y2 = y2, y1
            verticals.append((x1, y1, y2))
    
    # Index verticals by y-range
    by_y = defaultdict(list)
    for x, y1, y2 in verticals:
        for y in range(y1, y2 + 1):
            by_y[y].append(x)

    get = by_y.get # Local binding for speed
    spans: list[tuple[int, int, int]] = []
    append = spans.append # Local binding for speed

    for y in range(min_y, max_y + 1):
        x_values = get(y)
        if not x_values:
            continue
        x_values.sort()

        # Assume no holes
        append((y, x_values[0], x_values[-1]))

    return spans

def any_white_tiles(spans_by_y: dict[int, tuple[int, int]],
                    corner1: tuple[int, int], 
                    corner2: tuple[int, int]) -> bool:
    """
    Determine whether the inclusive rectangle between two corners contains any white tiles.

    Coverage is represented by spans_by_y, which maps each row y to a tuple
    (x_left, x_right) indicating that all tiles (x, y) with x_left <= x <= x_right
    are red or green. The function normalizes the two corners to form an inclusive
    axis-aligned rectangle, then verifies that every row y in this range is fully covered by 
    its span. If any row is missing or its span fails to cover x1..x2, the rectangle contains 
    at least one "white" tile. White tiles are defined as those which are neither red nor 
    green.

    Args:
        spans_by_y (dict[int, tuple[int, int]]): Mapping from row y to an inclusive
            horizontal span (x_left, x_right) of covered tiles on that row. Boundaries
            are assumed to be included in the span.
        corner1 (tuple[int, int]): One rectangle corner as (x, y).
        corner2 (tuple[int, int]): The opposite rectangle corner as (x, y).

    Returns:
        bool: True if there exists at least one white tile within the inclusive
            rectangle; False if there are no white tiles. 

    Notes:
        - This assumes exactly one continuous span per row (no holes). 
    """
    x1, y1 = corner1
    x2, y2 = corner2
    x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1) # Ensure x1 is smaller
    y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1) # Ensure x2 is smaller

    # Edge checks: potential early exits
    for y in range(y1, y2 + 1):
        span = spans_by_y.get(y)
        xleft, xright = span if span else (None, None)
        if x1 < xleft or x2 > xright:
            return True # There is white in the span
            
    return False # There are no white tiles

def run(data: list[str]) -> tuple[int, int]:
    """
    Compute the largest axis-aligned rectangle area from red-tile vertices (Part 1),
    then recompute with coverage validation against green spans (Part 2).

    Workflow:
    1) Parses the input strings into 2D integer coordinates (red tiles).
    2) Part 1: Evaluates all rectangles spanned by pairs of red tiles and returns
        the maximum inclusive area without coverage constraints.
    3) Part 2: Builds per-row inclusive green coverage spans from the polygon
        defined by red tiles, then finds the maximum rectangle area whose interior
        and boundary are fully covered by these spans (no white tiles).

    Args:
        data (list[str]): Lines of "x,y" coordinate strings representing the red
            vertices that define the polygonal outline.

    Returns:
        tuple[int, int]: (max_area_part1, max_area_part2) where:
            - max_area_part1 is the largest inclusive area among all rectangles
            formed by pairs of red tiles (no coverage check).
            - max_area_part2 is the largest inclusive area among those rectangles
            that are fully covered by the green spans derived from the red outline.

    Notes:
        - Rectangles are axis-aligned; area counts tiles inclusively on both axes.
        - Green spans are inclusive per row and assume a single continuous span
        ("no holes). 
    """
    red_tiles = parse_coords(data)
    max_area = get_max_area(red_tiles, None) # Part 1

    green_spans = find_green_spans(red_tiles) # Find all green tiles
    part2 = get_max_area(red_tiles, green_spans)

    return max_area, part2

inputfile = Path('day09.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(example)

print('Day 1:', part1_result)
if part1_result == 4759420470:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 1603439684:
    print('PASS')