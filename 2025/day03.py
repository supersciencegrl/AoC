from pathlib import Path

example = """987654321111111
    811111111111119
    234234234234278
    818181911112111"""
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

def max_joltage(battery_str: str) -> int:
    """
    Compute the highest possible two-digit “joltage” from the digits of a string of batteries 
    whilst preserving the order.
    NOTE: This function is no longer used, since `safety_override()` can perform the same role. 

    This heuristic selects two digits from the input string of digits to form the
    largest possible two-digit number, subject to the order of the original sequence:
      - It finds the two highest-valued digits overall.
      - If the index of the highest digit appears before the index of the second
        highest digit, it uses those two in descending order.
      - If the highest digit is the final character in the string, it reverses
        the top two digits.
      - Otherwise, it pairs the highest digit with the maximum digit after it. 

    Args:
        battery_str (str): A non-empty string of decimal digits ('0'–'9') from
            which to derive the two-digit joltage value.

    Returns:
        int: The largest two-digit number (10–99 or possibly 00 as 0) determined by the 
            described selection logic.

    Raises:
        IndexError: If battery_str has fewer than 2 characters.
        ValueError: If battery_str contains any non-digit characters.
    """
    battery = list(battery_str) # Force list of characters
    ordered_digits = sorted(battery, reverse = True)
    
    highest = battery.index(ordered_digits[0])
    second = battery.index(ordered_digits[1])
    if highest < second:
        joltage = ('').join(ordered_digits[:2])
    elif highest == len(battery) - 1:
        joltage = ('').join((ordered_digits[1], ordered_digits[0]))
    else:
        tail = battery[highest+1:]
        joltage = ('').join((ordered_digits[0], max(tail)))
    
    return int(joltage)

def safety_override(battery_str: str, num_batteries: int = 12) -> int:
    """
    Select the numerically largest subsequence of digits (as int) of a given length.

    Extracts the largest possible number (as an order-preserving subsequence) of length 
    `num_batteries` from `battery_str`. Scans left-to-right and pops smaller trailing digits 
    from the chosen `keep` stack when a larger digit appears, provided there are enough 
    remaining characters to still reach the required length.

    Args:
        battery_str (str): String of decimal digits ('0'–'9') from which to
            select the subsequence.
        num_batteries (int): Desired length of the resulting subsequence
            (default: 12).

    Returns:
        int: The integer value of the resulting subsequence of length
            `num_batteries`. Leading zeros (if any) are preserved in the subsequence
            construction but will not affect the integer conversion semantics.

    Raises:
        ValueError: If `battery_str` contains non-digit characters.
    """
    len_str = len(battery_str)
    keep = []

    for idx, digit in enumerate(battery_str):
        while keep and keep[-1] < digit and (len(keep) - 1 + len_str - idx) >= num_batteries:
            keep.pop()
        if len(keep) < num_batteries:
            keep.append(digit)
        # print(keep)
    
    joltage = ('').join(keep[:num_batteries])

    return int(joltage)

def run(batteries: list[str]) -> tuple[int, int]:
    """
    Compute aggregate joltage scores for two subsequence lengths across inputs.

    For each input battery string, this function computes two order-preserving
    maximal numbers using safety_override:
    - A two-digit maximum (num_batteries=2) for Part 1.
    - A twelve-digit maximum (num_batteries=12) for Part 2.
    It sums these per-battery results separately and returns both totals.

    Args:
        batteries (list[str]): A list of strings composed of decimal digits
            representing battery readings.

    Returns:
        tuple[int, int]: A pair (part1_result, part2_result) where:
            - part1_result is the sum of the 2-digit maxima across all batteries.
            - part2_result is the sum of the 12-digit maxima across all batteries.

    Raises:
        ValueError: Propagated from safety_override if a battery contains
            non-digit characters.
    """
    part1_result = 0
    part2_result = 0

    for battery in batteries:
        part1_joltage = safety_override(battery, num_batteries = 2)
        part2_joltage = safety_override(battery, num_batteries = 12)
        part1_result += part1_joltage
        part2_result += part2_joltage
    
    return part1_result, part2_result

inputfile = Path('day03.txt')
data = read_inputfile(inputfile)

part1_result, part2_result = run(data)

print('Day 1:', part1_result)
if part1_result == 17155:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 169685670469164:
    print('PASS')