import math
from pathlib import Path

import pandas as pd

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
example = example.split('\n')

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
    
    return [line.replace('\n', '') for line in data]

def parse_formulae_humans(data: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """
    Parse lines of mixed numeric rows and a trailing operations line into a DataFrame and tokens.

    Interprets all but the last input line as whitespace-separated integers and
    loads them into a pandas DataFrame (one row per line). The final line is
    parsed as a sequence of whitespace-separated operation tokens.

    Args:
        data (list[str]): Input lines where:
            - data[:-1] are rows of integers separated by whitespace.
            - data[-1] is a whitespace-separated list of operation strings.

    Returns:
        tuple[pd.DataFrame, list[str]]:
            - A DataFrame with integer values parsed from data[:-1].
            - A list of operation tokens parsed from data[-1].

    Raises:
        ValueError: If any of the lines other than the last contain non-integer tokens.

    Notes:
        - Leading/trailing spaces are stripped from numeric lines before parsing.
        - All numeric rows should have the same number of columns for a
        rectangular DataFrame; otherwise, pandas will align columns by
        position and may introduce missing values.
    """
    # Parse numerical values
    rows = [line.strip() for line in data[:-1]]
    df = pd.DataFrame([list(map(int, row.split())) for row in rows])

    # Parse operations
    operations = data[-1].split()

    return df, operations

def parse_formulae_cephalopods(data: list[str]):
    """
    Parse right-aligned, columnar numeric components into grouped terms for cephalopods.

    Treats all but the last input line as a fixed-width, right-aligned grid of
    characters. Each column (from rightmost to leftmost) is read vertically to
    form a token by concatenating its characters (stripping whitespace) and
    attempting to convert to an integer. Columns that fail integer conversion
    act as separators between groups (terms). Consecutive numeric columns are
    collected into a term as a list of integers. The scan proceeds from the
    rightmost column to the leftmost, preserving that order within each term.

    Args:
        data (list[str]): Input lines where data[:-1] are the rows to parse.
            The rows are treated as right-aligned columns; the parser pads rows
            with spaces to the width of the longest line to allow vertical reads.

    Returns:
        list[list[int]]: A list of terms, each term being a list of integers
        parsed from consecutive numeric columns. Terms are produced in the
        order discovered during the right-to-left scan.

    Notes:
        - Rows are right-padded with spaces to the length of the longest row so
        that each column index is valid across all rows.
    """
    rows = data[:-1]
    rightmost = max((len(row) for row in rows)) - 1

    # Right-pad rows
    padded_rows = [row.ljust(rightmost) for row in rows]

    terms = []
    numbers = []
    for col in range(rightmost, -1, -1): # Stop at 0
        try:
            value = int(('').join(char.strip() for char in [row[col] for row in padded_rows]))
        except ValueError:
            terms.append(numbers)
            numbers = []
        else: # If there's a value
            numbers.append(value) # Append to end of list; list is right-to-left
    terms.append(numbers)

    return terms

def run(data: list[str]) -> tuple[int, int]:
    """
    Evaluate two formula interpretations (human and cephalopod) and return their totals.

    Human parsing:
    - Parses data into a DataFrame of integer rows (all but the last line) and a list of
    operation tokens (last line).
    - For each column i, runs '+' or '*' operations and adds the result to total. 

    Cephalopod parsing:
    - Parses right-aligned columnar components into grouped terms (lists of integers).
    - Iterates operations in reverse. For each i-th reversed operation, applies '+' or '*' 
        operations and adds the result to total.

    Args:
        data (list[str]): Input lines. All but the last line are numeric rows 
            (whitespace-separated integers) for human parsing. The last line contains 
            whitespace-separated operation tokens consisting of '+' and/or '*'. 

    Returns:
        tuple[int, int]: (total, part2) where:
            - total is the human interpretation result (sum of per-column sums/products as 
                specified).
            - part2 is the cephalopod interpretation result (sum of per-term sums/products per 
                reversed operations).

    Raises:
        ValueError: If rows other than the last contain non-integer tokens.
    """
    df, operations = parse_formulae_humans(data)

    total = 0 # Default
    for i, operation in enumerate(operations):
        if operation == '+':
            total += df[i].sum()
        elif operation == '*':
            total += df[i].prod()
    
    part2 = 0
    terms = parse_formulae_cephalopods(data)
    for i, operation in enumerate(reversed(operations)):
        term = terms[i]
        if operation == '+':
            part2 += sum(term)
        elif operation == '*':
            part2 += math.prod(term)
    
    return total, part2

inputfile = Path('day06.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 4878670269096:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 8674740488592:
    print('PASS')