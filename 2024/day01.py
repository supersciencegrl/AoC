from pathlib import Path

example1 = '''3   4
    4   3
    2   5
    1   3
    3   9
    3   3'''
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

def parse_data(data: list[str]) -> tuple[tuple[str], tuple[str]]:
    """
    Parses a list of strings by splitting each string into two parts and returns
    two tuples containing the left and right parts, respectively.

    Args:
        data (list[str]): A list of strings, each expected to contain two whitespace-separated 
                          values.

    Returns:
        tuple[tuple[str, ...], tuple[str, ...]]: A tuple of two tuples; the first containing
                                                 the left parts and the second containing
                                                 the right parts of the split strings.
    """
    left, right = zip(*(n.split() for n in data))

    return left, right

def calculate_result(left: list[str], right: list[str]) -> int:
    """
    Calculates the sum of distances between corresponding elements of two lists after sorting 
    them.

    Args:
        left (list[str]): A list of strings representing numerical values to be sorted.
        right (list[str]): A list of strings representing numerical values to be sorted.

    Returns:
        int: The sum of the absolute differences between sorted elements of the two lists.
    """
    left_sorted = sorted(left)
    right_sorted = sorted(right)

    # Calculate the differences between values in each of the sorted lists
    results = [abs(int(x)-int(y)) for (x,y) in [(value,right_sorted[i]) for (i, value) in enumerate(left_sorted)]]
    # Sum the distances
    result = sum(results)

    return result

def calculate_similarity(left: list[str], right: list[str]) -> int:
    """
    Calculates a similarity score based on the frequency and value of entries in two lists.

    Args:
        left (list[str]): A list of strings representing numerical values.
        right (list[str]): A list of strings representing numerical values, some of which will 
                           be repeated from the left list

    Returns:
        int: The similarity score, calculated as the sum of each value in the 'left' list
             multiplied by the frequency of its occurrence in the 'right' list.
    """
    similarity = 0
    for entry in left:
        similarity_multiplier = right.count(entry)
        similarity += (int(entry) * int(similarity_multiplier))
    
    return similarity

inputfile = Path('day01.txt')
data = read_inputfile(inputfile)

left_list, right_list = parse_data(data)
part1_result = calculate_result(left_list, right_list)
part2_result = calculate_similarity(left_list, right_list)

print('Day 1:', part1_result)
if part1_result == 2970687:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 23963899:
    print('PASS')