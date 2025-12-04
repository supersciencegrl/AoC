from pathlib import Path

from deprecation import deprecated

example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def read_inputfile(inputfile: Path) -> str:
    """
    Reads a text file and returns it as a string, with leading/trailing whitespace removed.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        str: The data string from the file, with whitespace removed
    """
    with open(inputfile, 'rt') as fin:
        data = fin.read()
    
    return data.strip()

def parse_data(data: str) -> list[tuple[int, int]]:
    """Parses a comma-separated list of hyphen-delimited ranges.

    Expects input like "1-3, 4-7, 10-12" and returns a list of (start, end)
    integer tuples.

    Args:
        data: A string containing one or more ranges separated by commas. Each
            range must be in the form "start-end".

    Returns:
        A list of (start, end) tuples representing the parsed ranges.

    Raises:
        TypeError: If `data` is not a string.
        ValueError: If a segment is missing a hyphen or contains non-integer bounds.
    """
    ranges = data.split(',')
    parsed = [(first, last) for first, sep, last in [r.partition('-') for r in ranges]]

    return parsed

@deprecated
def has_repeat(value: str) -> bool:
    """Checks whether a string contains any immediate repeated substring.
    NOTE: This function is deprecated because you should always read the question and not 
    answer a completely different puzzle instead. 

    The function scans all possible substring lengths up to half the string and detects whether 
    any substring is immediately repeated (i.e., two identical adjacent blocks). It returns True 
    on the first detected repeat, otherwise False.

    Args: 
        value: The input to check. It will be coerced to a string.

    Returns: 
        bool: True if an immediate repeated substring is found; False otherwise.

    Examples: 
        - "1212" -> True
        - "1111" -> True
        - "1231234" -> True
        - "1234" -> False
    """
    value = str(value) # Ensure string
    
    substrings = []
    len_value = len(value)
    max_len_repeat = len_value // 2 # Repeating section can have up to half the length
    for i in range(max_len_repeat):
        for j in range(len_value - i):
            print(i, '\t', j, '\t', value[j:j+i+1])
            substring = value[j : j+i+1]
            try:
                if substrings[-(i+1)] == substring:
                    print(substring, substrings)
                    return True
            except IndexError:
                pass
            substrings.append(substring)
    
    return False

def is_repeated(value: str) -> bool:
    """
    Determine whether the input string is composed of two identical halves.

    The input is coerced to a string and only even-length strings can qualify.
    For even-length strings, the function checks if the first half repeated twice
    equals the original string.

    Args:
        value: The input to evaluate. It will be coerced to a string.

    Returns:
        True if the string consists of two identical halves; otherwise, False.

    Examples:
        - "1919" -> True
        - "1111" -> True
        - "576576" -> True
        - "57657" -> False
        - "1234" -> False
    """
    value = str(value) # Ensure str

    len_substring = len(value) / 2
    if len_substring != int(len_substring): # Odd-length value
        return False
    
    elif value == value[:int(len_substring)] * 2:
        return True
    else:
        return False

def has_repeat(value: str) -> bool:
    """
    Check whether a string is composed of repeated blocks.

    The input is coerced to a string and the function tests all possible block lengths
    up to half the string length. For any block length that evenly divides the total
    length, it checks whether repeating a candidate substring the required number of
    times reconstructs the original string.

    Args:
        value: A string representing digits (e.g., "5757"). It will be coerced to str.

    Returns:
        bool: True if the string equals some substring repeated an integer number of times; 
            otherwise, False.

    Examples:
        - "5757" -> True
        - "121212" -> True
        - "1234" -> False
    """
    value = str(value) # Ensure string
    
    len_value = len(value)
    max_len_repeat = len_value // 2 # Repeating section can have up to half the length
    for len_substring in range(max_len_repeat):
        quotient = len_value / (len_substring+1)
        if quotient == int(quotient): # It's a factor
            for j in range(len_value - len_substring):
                # print(len_substring, '\t', j, '\t', value[j:j+len_substring+1])
                substring = value[j : j+len_substring+1]
                if value == substring * int(quotient):
                    return True
    
    return False

def check_for_invalid_ids(parsed: list[tuple[int, int]], part2: bool) -> list[int]:
    """
    Identify invalid IDs within parsed ranges based on repetition rules.

    Iterates over all IDs within each (start, end) tuple in `parsed`. For Part 1
    (`part2` is False), an ID is invalid if it is composed of two identical halves
    (`is_repeated`). For Part 2 (`part2` is True), an ID is invalid if it can be
    represented as a repeated substring (`has_repeat`). IDs are treated as strings
    of digits for these checks.

    Args:
        parsed: A list of (start, end) integer tuples defining inclusive ID ranges.
        part2: If True, use `has_repeat` to flag invalid IDs; if False, use
            `is_repeated`.

    Returns:
        A list of IDs (as integers) deemed invalid according to the selected rule.
    """
    invalid = []
    for start, end in parsed:
        start_int = int(start)
        end_int = int(end)
        for this_id in range(start_int, end_int+1):
            if part2 is False:
                if is_repeated(this_id):
                    invalid.append(this_id)
            else:
                if has_repeat(this_id):
                    invalid.append(this_id)
    
    return invalid

def run(data: str) -> tuple[int, int]:
    """
    Run the full evaluation pipeline and compute both results.

    This function parses the input string into ranges, identifies invalid IDs under
    two different criteria, and returns the sums of those invalid IDs for each part.

    Processing steps:
    - Parse the input data into (start, end) ranges using `parse_data`.
    - For Part 1, find IDs invalid under `is_repeated` and sum them.
    - For Part 2, find IDs invalid under `has_repeat` and sum them.

    Args:
        data: A comma-separated string of hyphen-delimited ranges (e.g., "1-3,4-7").

    Returns:
        A tuple of two integers: (sum of invalid IDs for Part 1, sum of invalid IDs for Part 2).
    """
    parsed = parse_data(data)
    invalid = check_for_invalid_ids(parsed, part2 = False)
    day1_result = sum(invalid)

    invalid_part2 = check_for_invalid_ids(parsed, part2 = True)
    day2_result = sum(invalid_part2)

    return day1_result, day2_result

inputfile = Path('day02.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 30608905813:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 31898925685:
    print('PASS')