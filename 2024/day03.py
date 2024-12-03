import re

from pathlib import Path

example1 = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'''
example2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''

def read_inputfile(inputfile: Path) -> str:
    """
    Reads a text file and returns its content as a single string.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        str: The content of the file as a single string.
    """
    with open(inputfile, 'rt') as fin:
        data = fin.read()

    return data

def execute_multiplication_instruction(instruction: str) -> int:
    """
    Parses a multiplication instruction from a string and returns the product of the two numbers.

    The input string is expected to be in the format "mul(x,y)" where x and y are integers.

    Args:
        instruction (str): A string containing the multiplication instruction in the format "mul(x,y)".

    Returns:
        int: The product of the two integers extracted from the instruction.
    """
    # Parse the two numbers to be multiplied, as strings
    first = instruction.partition('mul(')[2].partition(',')[0]
    second = instruction.partition(',')[2].partition(')')[0]

    # Convert to integers and multiply them
    first = int(first)
    second = int(second)
    product = first * second

    return product

def follow_instructions(matches: list[str]):
    """
    Processes a list of instructions to calculate a result based on conditional execution.

    The function iterates over a list of instructions, enabling or disabling multiplication
    based on the control instructions ("don't()" and "do()"). Only when multiplication is 
    enabled, the function executes multiplication instructions and sums their results.

    Args:
        matches (list[str]): A list of strings containing instructions. These can include:
                             - Control instructions: "don't()" to disable multiplication,
                               and "do()" to enable it.
                             - Multiplication instructions in the format "mul(x,y)" where
                               x and y are integers.

    Returns:
        int: The cumulative result of executing enabled multiplication instructions.
    """
    result = 0 # Initial value
    multiplication_enabled = True
    for instruction in matches:
        # Ignore multiplication functions following a "don't()" instruction
        if instruction.startswith('don\'t('):
            multiplication_enabled = False
        # Enable multiplication function following a "do()" instruction
        elif instruction.startswith('do('):
            multiplication_enabled = True
        # If multiplication is enabled, run the multiplication instruction and add it to result
        elif multiplication_enabled:
            product = execute_multiplication_instruction(instruction)
            result += product
    
    return result

def calculate_results(data: str):
    """
    Calculates results based on multiplication instructions and control commands within a string.

    This function processes the input string to extract and execute multiplication instructions
    under two different scenarios:
    - Part 1: Only multiplication instructions are considered.
    - Part 2: Both multiplication instructions and control commands ("do()" and "don't()") are
              considered, affecting whether multiplication instructions are enabled.

    Args:
        data (str): A string containing instructions. Instructions can include:
                    - Multiplication instructions in the format "mul(x,y)".
                    - Control instructions "do()" to enable and "don't()" to disable multiplication.

    Returns:
        Tuple[int, int]: A tuple containing two integers:
            - The first integer is the result of executing only multiplication instructions (Part 1).
            - The second integer is the result of executing multiplication instructions with control 
              commands (Part 2).
    """
    part1_matches = re.findall(r"mul\(\d+,\d+\)", data)
    part2_matches = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data)

    part1_result = follow_instructions(part1_matches)
    part2_result = follow_instructions(part2_matches)

    return part1_result, part2_result

inputfile = Path('day03.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = calculate_results(data)

print('Day 1:', part1_result)
if part1_result == 175615763:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 74361272:
    print('PASS')