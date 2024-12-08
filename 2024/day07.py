from pathlib import Path

example = '''190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20'''
example = example.split('\n    ')

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

def evaluate_combinations(initial_results: list[int], 
                          values: list[int],
                          part2 = False
                          ) -> list[int]:
    """
    Evaluates all possible combinations of results using addition, multiplication, and optional 
    concatenation (Part 2 only).

    This function takes an initial list of results and a list of values, then generates new combinations
    by adding and multiplying each result with the first value. If `part2` is True, it also considers
    concatenating the result and value as a new integer.

    Args:
        initial_results (list[int]): A list of integers representing initial results to be 
                                     combined.
        values (list[int]): A list of integers to be used in the combination process.
        part2 (bool, optional): A flag indicating whether to include concatenation as a 
                                combination method. Defaults to False.

    Returns:
        list[int]: A list of combined results produced by applying addition, multiplication, and 
        optionally concatenation to the initial results with the first value from the values list.
    """
    if values:
        combinations = []
        for result in set(initial_results):
            combinations.append(result + values[0])
            combinations.append(result * values[0])
            # Also concatenate values for Part 2
            if part2: 
                concatenated = f'{result}{values[0]}'
                combinations.append(int(concatenated))

        return combinations

def is_equation_possible(result: int, values: list[int], part2 = False) -> int:
    """
    Determines if a specific result can be achieved using a sequence of values with specified 
    operations.

    This function attempts to calculate whether the given `result` can be obtained by performing
    a series of operations (addition, multiplication, and optional concatenation) on the `values` 
    list. It iteratively combines values until no values are left to process.

    Args:
        result (int): The target result that needs to be achieved.
        values (list[int]): A list of integers used for generating possible results through operations.
        part2 (bool, optional): A flag that, when True, includes concatenation as an operation in addition
                                to addition and multiplication. Defaults to False.

    Returns:
        int: The original `result` if it can be achieved using the operations; otherwise, 0 if 
             it is not possible.
    """
    results_so_far = values[:1] # Value with index 0, as a 1-membered list
    values_left = values[1:]
    while values_left:
        if not part2: # Part 1
            results_so_far = evaluate_combinations(results_so_far, 
                                                   values_left,
                                                   part2 = False
                                                   )
        else: #Part 2
            results_so_far = evaluate_combinations(results_so_far,
                                                   values_left,
                                                   part2 = True
                                                   )
        values_left = values_left[1:]

    if result in results_so_far: # Works for Part 1 and Part 2
        return result
    else: # Never works
        return 0

def parse_equation(equation: str) -> tuple[int, list[int]]:
    """
    Parses an equation string into a target result and a list of values.

    This function splits the input string into a result and a series of values.
    The expected format of the input string is "result: value1 value2 ...",
    where the result is separated from the values by ": ".

    Args:
        equation (str): An input string representing an equation, with specific formatting. 

    Returns:
        tuple[int, list[int]]: A tuple containing:
            - An integer representing the target result.
            - A list of integers representing the values to be used in calculations.
    """
    # Split the equation into result and values
    result, _, values = equation.partition(': ')
    # Convert the number strings to integers
    result = int(result)
    values = [int(v) for v in values.split()]

    return result, values

def run(data):
    """
    Processes a list of equations to calculate results based on two different sets of operations.

    This function iterates over each equation in the input data, parses it to extract the target 
    result and values, and then checks if the target result can be achieved using specified 
    operations. It calculates results for two scenarios: one with basic operations and another 
    with additional operations enabled.

    Args:
        data (list[str]): A list of strings, each representing an equation formatted as 
                          "result: value1 value2 ...".

    Returns:
        tuple[int, int]: A tuple containing:
            - The cumulative result of all equations processed with basic operations 
              (part1_result).
            - The cumulative result of all equations processed with additional operations 
              (part2_result).
    """
    part1_result = 0
    part2_result = 0
    for equation in data:
        result, values = parse_equation(equation)
        # There's totally a better way than doing it twice, but it ain't in this script
        part1_calibration = is_equation_possible(result, values, part2 = False)
        part2_calibration = is_equation_possible(result, values, part2 = True)
        part1_result += part1_calibration
        part2_result += part2_calibration

    return part1_result, part2_result

inputfile = Path('day07.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 2314935962622:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 401477450831495:
    print('PASS')