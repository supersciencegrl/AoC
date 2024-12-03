from pathlib import Path

example1 = '''7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9'''
example1 = example1.split('\n    ')

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

def calculate_safety(levels: list[int]) -> bool:
    """
    Determines whether a list of levels is considered safe based on specified conditions.

    A list is considered safe if it is sorted in either ascending or descending order,
    and the difference between consecutive levels is between 1 and 3, inclusive.

    Args:
        levels (list[int]): A list of integers representing safety levels.

    Returns:
        bool: True if the list is considered safe according to the criteria; False otherwise.
    """
    # Check whether levels are in ascending or descending order
    if levels == sorted(levels) or levels == sorted(levels, reverse = True):
        for i in range(len(levels)-1):
            delta = abs(levels[i] - levels[i+1])
            # Check whether difference between this level and the following is within limits
            if not 1 <= delta <= 3:
                return False # Part 1: no level in report must be "bad"
    else:
        return False
    
    # If nothing has been found to indicate unsafe
    return True

def calculate_safety_part2(levels: list[int]) -> bool:
    """
    Determines whether a list of safety levels can be made safe by removing one element.

    A list is considered potentially safe if removing any single element results
    in a list that meets the safety criteria defined in `calculate_safety`.

    Args:
        levels (list[int]): A list of integers representing safety levels.

    Returns:
        bool: True if the list can be made safe by removing one element; False otherwise.
    """
    for i in range(len(levels)):
        # Remove each element in turn and recalculate the safety level without it
        new_levels = levels[:i] + levels[i+1:]
        result = calculate_safety(new_levels)
        if result:
            return True
    
    # If there is no way to make the report safe
    return False

def calculate_result(data: list[str]) -> tuple[int, int]:
    """
    Evaluates a list of safety reports and counts how many are safe based on two criteria.

    The function processes each report to determine if it is safe according to two parts:
    - Part 1: A report is safe if it meets the safety criteria defined in `calculate_safety`.
    - Part 2: A report is also considered safe if it can be made safe by "dampening": removing 
        one element, as determined by `calculate_safety_part2`.

    Args:
        data (list[str]): A list of strings, where each string contains space-separated
                          numerical values representing levels of a report.

    Returns:
        Tuple[int, int]: A tuple containing two integers:
            - The first integer is the count of reports that are safe according to Part 1.
            - The second integer is the count of reports that are safe according to Part 2.
    """
    safe_reports_part1 = 0
    safe_reports_part2 = 0
    for report in data:
        # Split report into levels
        levels = [int(n) for n in report.split()]
        # Check whether report is inherently safe (before dampening)
        report_is_safe_part1 = calculate_safety(levels)
        if report_is_safe_part1:
            safe_reports_part1 += 1
            safe_reports_part2 += 1 # If safe in Part1, always safe in Part2
        else: # Check whether report can be made safe by dampening
            report_is_safe_part2 = calculate_safety_part2(levels)
            if report_is_safe_part2:
                safe_reports_part2 += 1
    
    return safe_reports_part1, safe_reports_part2

inputfile = Path('day02.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = calculate_result(data)

print('Day 1:', part1_result)
if part1_result == 269:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 337:
    print('PASS')