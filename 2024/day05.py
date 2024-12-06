from pathlib import Path

example = '''47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47'''
example = example.split()

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

def parse_protocol(data: list[str]) -> tuple[list[list[str, str]], list[str]]:
    """
    Parses protocol data into two sections based on line formats.

    The function divides the input data into two sections:
    - Section 1: Lines containing the '|' character, parsed into lists of strings.
    - Section 2: Lines containing the ',' character, collected as strings.

    Args:
        data (list[str]): A list of strings, each representing a line of protocol data.

    Returns:
        Tuple[list[list[str]], list[str]]: A tuple containing two elements:
            - The first element is a list of lists, where each sublist represents a rule
              from Section 1 (two pages in correct order), split by the '|' character.
            - The second element is a list of strings representing updates from Section 2.
    """
    section1_unparsed = []
    section2 = []
    for line in data:
        if '|' in line: # it's a "rule"
            section1_unparsed.append(line)
        elif ',' in line: # it's an "update"
            section2.append(line)

    # Parse Section 1 to give a list of lists describing page ordering rules
    section1 = [rule.split('|') for rule in section1_unparsed]
    
    return section1, section2

def find_middle_page(pages: list[str]) -> int:
    """
    Finds the middle page number from a list of page numbers.

    This function calculates the middle index of the given list of pages and returns
    the page number at that index as an integer.

    Args:
        pages (list[str]): A list of strings, each representing a page number.

    Returns:
        int: The middle page number from the list, converted to an integer.
    """
    middle_index = int((len(pages) - 1) / 2)
    
    return int(pages[middle_index])

def check_update_order(section1: list[list[str, str]], pages: list[str]) -> int:
    """
    For Part 1. 
    Checks the update order of pages against specified ordering rules and returns the middle page 
    if valid. 

    The function iterates through a list of pages and checks if each page adheres to ordering rules
    specified in `section1`. If any page violates the rule by appearing before a required preceding 
    page, the function returns 0. Otherwise, it returns the middle page number.

    Args:
        section1 (list[list[str]]): A list of lists, where each sublist represents a page ordering 
                                    rule in the form [current_page, required_previous_page].
        pages (list[str]): A list of page numbers as strings, representing the order of pages to be 
                           checked.

    Returns:
        int: The middle page number if the order is valid; otherwise, 0 if any ordering rule is 
             violated.
    """
    for i, page in enumerate(pages):
        page_rules = [rule for rule in section1 if rule[0] == page]
        for previous_page in pages[:i]:
            # If the page is out of order, the list is incorrect so return 0
            if previous_page in [rule[1] for rule in page_rules]:
                return 0

    # If the list is correctly ordered, return the middle page as an integer
    middle_page = find_middle_page(pages)
    return middle_page

def fix_misordered_update(pages: list, section1: list[list]) -> int:
    """
    For Part 2. 
    Identifies the correct middle page in a potentially misordered list of pages using ordering 
    rules.

    The function examines each page and determines if it is the middle page by checking its
    relationships with other pages based on the rules in `section1`. It assumes all possible
    page relationships are present in `section1`.

    Args:
        pages (list): A list of page numbers as strings, representing the pages to be checked.
        section1 (list[list[str]]): A list of lists, where each sublist represents a page ordering 
                                    rule.

    Returns:
        int: The page number of the middle page.

    Raises:
        ValueError: If there is an issue and no middle page was identified (this should not happen). 
    """
    middle_index = (len(pages) - 1) / 2
    for this_page in pages: # Assumes all page relationship combinations are in Section 1
        page_is_after = [rule[0] for rule in section1 if rule[1] == this_page and rule[0] in pages]
        # If this is the middle page, return the page number
        if len(page_is_after) == middle_index:
            return int(this_page)
    
    # If no correct order could be obtained so no middle page is found
    raise ValueError

def check_all_updates(section1: list[list[str, str]], section2: list[str]) -> tuple[int, int]:
    """
    Evaluates updates against ordering rules and calculates results for both initially-correct and 
    fixed updates. 

    This function processes a list of updates, checking each against a set of ordering rules
    from `section1`. It calculates a result for correctly ordered updates and attempts to fix
    and, separately, recalculate results for initially-misordered updates.

    Args:
        section1 (list[list[str]]): A list of lists representing page ordering rules.
        section2 (list[str]): A list of update strings, where each string contains comma-separated
                              page numbers representing an update.

    Returns:
        tuple[int, int]: A tuple containing two integers:
            - The first integer is the cumulative result of correctly ordered updates only.
            - The second integer is the cumulative result after fixing misordered updates only.
    """
    part1_result = 0
    part2_result = 0
    for update in section2:
        pages = update.split(',')
        # Add middle page number to Part 1 only if initial order is correct
        result_from_update = check_update_order(section1, pages)
        part1_result += result_from_update
        if not result_from_update:
            # Add corrected middle page number to Part 2 only if initial order was incorrect
            new_middle_page = fix_misordered_update(pages, section1)
            part2_result += new_middle_page
    
    return part1_result, part2_result

inputfile = Path('day05.txt')
data = read_inputfile(inputfile)

section1, section2 = parse_protocol(data)
part1_result, part2_result = check_all_updates(section1, section2)

print('Day 1:', part1_result)
if part1_result == 6242:
    print('PASS')
print('Day 2:', part2_result)
if part2_result == 5169:
    print('PASS')
