from pathlib import Path

example = """1
    10
    100
    2024"""
example = example.split()

def read_inputfile(inputfile: Path) -> list[str]:
    """
    Reads a text file and returns its contents as a list of strings, with leading/trailing 
    whitespace removed from each string.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        list[str]: A list of strings representing the file contents, with leading/trailing 
                   whitespace removed from each string. 
    """
    with open(inputfile, 'rt') as fin:
        data = fin.readlines()

    return [line.strip() for line in data]

def get_next_number(number: str) -> int:
    """
    Computes a transformed number through a series of bitwise and arithmetic operations.

    This function takes an input secret number as a string, converts it to an integer, 
    and applies a series of transformations involving multiplication, bitwise XOR, and 
    modulus operations. The transformation is designed to produce a new number within 
    a specified range.

    Args:
        number (str): A string representing the initial secret number to be transformed.

    Returns:
        int: The final secret number after applying the series of operations.
    """
    number = int(number)

    given = number * 64
    mixed = number ^ given
    pruned = mixed % 16777216

    step2 = pruned // 32
    mixed2 = pruned ^ step2
    pruned2 = mixed2 % 16777216

    step3 = pruned2 * 2048
    mixed3 = pruned2 ^ step3
    pruned3 = mixed3 % 16777216

    return pruned3

def run(data: list[str]) -> int:
    """
    Processes a list of seret numbers through iterative transformations and calculates 
    their sum after 2000 iterations of transforming each secret number.

    This function takes a list of secret numbers as strings, applies a transformation 
    function `get_next_number` to each number in a loop for 2000 iterations, collects 
    the final transformed secret numbers, and returns their sum.

    Args:
        data (list[str]): A list of strings, where each string represents a number to be 
                          transformed.

    Returns:
        int: The sum of the final transformed numbers after applying the transformation 
             for each number in the list over 2000 iterations.
    """
    results = []
    for number in data:
        i = 0
        while i < 2000:
            number = get_next_number(number)
            i += 1
        results.append(number)

    result = sum(results)
    
    return result

inputfile = Path(r"day22.txt")
data = read_inputfile(inputfile)
part1_result = run(data)

print('Part 1:', part1_result)
if part1_result == 13429191512:
    print('PASS')