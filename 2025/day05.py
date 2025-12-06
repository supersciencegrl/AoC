from pathlib import Path

example = """3-5
    10-14
    16-20
    12-18

    1
    5
    8
    11
    17
    32"""
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

def parse_input(data: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Parse input lines into inclusive integer ranges and a list of ingredient IDs.

    Expects a list of strings where an empty string "" separates two sections:
    - The top section contains range lines in the form "start-end" (inclusive).
    - The bottom section contains one integer per line representing ingredient IDs.

    Args:
        data (list[str]): Input lines. Must contain exactly one empty string
            delimiter between the ranges section and the ingredients section.

    Returns:
        tuple[list[tuple[int, int]], list[int]]:
            - fresh_ranges: A list of (start, end) integer tuples, inclusive.
            - available_ingredients: A list of integers parsed from the lines
              after the empty delimiter.

    Raises:
        ValueError: If the delimiter "" is missing, if a range line is malformed
            (not "start-end" with int-like strings), or if any ingredient line is not an
            int-like string.
    """
    input_split_index = data.index('')
    fresh_ranges = data[:input_split_index]
    available_ingredients = data[input_split_index+1:]

    # Take ingredient values as integers
    fresh_ranges = [(int(first), int(last)) 
                    for this_range in fresh_ranges 
                    for first, _, last in [this_range.partition('-')]
                    ]
    available_ingredients = [int(i) for i in available_ingredients]

    return fresh_ranges, available_ingredients

def usable_ingredients(fresh_ranges: list[tuple[int, int]], 
                       available_ingredients: list[int]
                       ) -> list[int]:
    """
Filter available ingredient IDs to those covered by any fresh range.

For each ingredient ID in available_ingredients, checks whether it falls
within at least one inclusive interval in fresh_ranges. Returns the list of
IDs that are usable (both available and fresh), preserving input order and 
removing duplicates.

Args:
    fresh_ranges (list[tuple[int, int]]): Inclusive intervals (start, end)
        representing fresh ingredient ID ranges.
    available_ingredients (list[int]): Ingredient IDs to be tested for
        usability.

Returns:
    list[int]: Ingredient IDs from available_ingredients that lie within
        at least one of the fresh_ranges.

Notes:
    - Ranges are inclusive: an ID i is usable if start <= i <= end.
"""
    usable = []
    for i in available_ingredients:
        for first, last in fresh_ranges:
            if first <= i <= last:
                usable.append(i)
                break
    
    return usable

def fresh_ingredients(fresh_ranges: list[tuple[int, int]]) -> int:
    """
    Count unique integers covered by inclusive ranges.

    Merges overlapping or contiguous ranges, then sums the lengths of the merged
    intervals to compute how many distinct integers are covered.

    Args:
        fresh_ranges (list[tuple[int, int]]): List of inclusive (start, end)
            integer ranges, which should follow start <= end ordering. 

    Returns:
        int: The total number of unique integers covered by the provided ranges.

    Raises:
        IndexError: If fresh_ranges is empty (accesses sorted_ingredients[0]).
            Provide a non-empty list or add a guard before calling.

    Notes:
        - Time complexity: O(n log n) for sorting + O(n) for merging; memory
        usage is O(n) for the merged list. 
        - Making a big set was much more inefficient. 
    """
    # Sort ranges
    sorted_ingredients = sorted(fresh_ranges, key = lambda x: (x[0], x[1]))

    # Merge overlapping or touching ranges
    merged = []
    this_start, this_end = sorted_ingredients[0]
    for start, end in sorted_ingredients[1:]:
        if start <= this_end + 1: # The ranges overlap or touch
            this_end = max(this_end, end)
        else:
            merged.append((this_start, this_end))
            this_start, this_end = start, end
    merged.append((this_start, this_end))

    num_ingredients = sum(end - start + 1 for start, end in merged)

    return num_ingredients

def run(data: list[str]) -> tuple[int, int]:
    """
    Compute the number of usable ingredients and the total unique fresh coverage.

    Parses the input into inclusive ranges and ingredient IDs, filters the
    available IDs to those covered by any fresh range (usable), and calculates
    the total count of distinct integers covered by all fresh ranges (part2).

    Args:
        data (list[str]): Input lines where an empty string separates a section
            of "start-end" range lines from a section of integer ingredient IDs.

    Returns:
        tuple[int, int]: A pair (len(usable), part2) where:
            - len(usable) is the count of usable ingredient IDs (fresh and available).
            - part2 is the total number of unique integers covered by the ranges.

    Raises:
        ValueError: Propagated from parse_input if the input format is invalid.
        ValueError: If non-digit content is found in ranges or ingredient lines.
    """
    fresh_ranges, available_ingredients = parse_input(data)
    usable = usable_ingredients(fresh_ranges, available_ingredients)
    
    part2 = fresh_ingredients(fresh_ranges)

    return len(usable), part2

inputfile = Path('day05.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 735:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 344306344403172:
    print('PASS')