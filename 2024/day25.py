from pathlib import Path

example = """#####
    .####
    .####
    .####
    .#.#.
    .#...
    .....

    #####
    ##.##
    .#.##
    ...##
    ...#.
    ...#.
    .....

    .....
    #....
    #....
    #...#
    #.#.#
    #.###
    #####

    .....
    .....
    #.#..
    ###..
    ###.#
    ###.#
    #####

    .....
    .....
    .....
    #....
    #.#..
    #.#.#
    #####""".replace('    ', '')
example = example.split('\n\n')

def read_inputfile(inputfile: Path) -> str:
    """
    Reads a text file and returns its contents.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        str: A string representing the file contents. 
    """
    with open(inputfile, 'rt') as fin:
        data = fin.read()

    return data

def parse_data(data: list[str]) -> tuple[list[str], list[str]]:
    """
    Parses a list of strings containing newlines into locks and keys, respectively 
    based on whether they're "full" ("#####") or empty ("....."), in the top row 
    of the list.

    This function processes each string in the input list, categorizing them into
    locks or keys. It then splits them by newline ("\n") into lists of smaller 
    strings, each list representing a lock or a key. 

    Args:
        data (list[str]): A list of strings, each representing either a lock or a key,
                          identified by their respective prefixes.

    Returns:
        tuple[list[list[str]], list[list[str]]]: A tuple containing:
            - A list of lists, where each sublist contains words from a lock line.
            - A list of lists, where each sublist contains words from a key line.
    """
    locks = []
    keys = []

    for item in data:
        if item.startswith('#####'): # Full at the top: it's a lock
            locks.append(item.split())
        elif item.startswith('.....'): # Empty at the top: it's a key
            keys.append(item.split())

    return locks, keys

def parse_keys(keys: list[list[str]]) -> list[list[int]]:
    """
    Analyzes a list of key patterns to determine the size of each key (heights of each tooth) by 
    counting full positions (marked with "#").

    This function processes each key represented as a list of strings, where each string is a row.
    It calculates the "size" of each key by counting the number of full positions ('#') in each
    column and returns these sizes as a list of lists.

    Args:
        keys (list[list[str]]): A list of keys, where each key is represented as a list of strings
                                (rows) with '#' indicating full positions.

    Returns:
        list[list[int]]: A list of lists, where each sublist contains integers representing the
                         heights of teeth (number of full positions) in each column of a key.
    """
    key_sizes = []
    for key in keys:
        # Get count of '#' character per column in the key
        key_size = [sum(row[column] == '#' for row in key) for column in range(len(key[0]))]
        key_sizes.append(key_size)

    return key_sizes

def get_lock_size(lock: list[str]) -> list[int]:
    """
    Calculates the size of a lock by counting empty positions ('.') in each column.

    This function processes a lock represented as a list of strings, where each string is a row.
    It calculates the "size" of the lock by counting the number of empty positions ('.') in each
    column and returns these counts as a list.

    Args:
        lock (list[str]): A lock represented as a list of strings (rows) with '.' indicating 
                          empty positions.

    Returns:
        list[int]: A list of integers representing the number of empty positions in each column 
                   of the lock.
    """
    # Get count of '.' character per column in the lock
    return [sum(row[column] == '.' for row in lock) for column in range(len(lock[0]))]

def does_key_fit(key_size, lock_size):
    """
    Determines if a key can fit into a lock based on their respective sizes.

    This function compares the sizes of a key and a lock, where each size is represented
    as a list of integers. It checks whether each element of the key (tooth height) does not
    exceed the corresponding element of the lock (pin height). If any tooth is too large for
    a pin, the key does not fit.

    Args:
        key_size (list[int]): A list of integers representing the height of each tooth on 
                              the key.
        lock_size (list[int]): A list of integers representing the height of each pin in 
                               the lock.

    Returns:
        bool: True if the key fits into the lock (all teeth are within the corresponding 
              heights), False if any tooth is too large for its corresponding pin.
    """
    for i, height in enumerate(key_size):
        # Check whether the key tooth is too big for the lock pin
        if lock_size[i] < height:
            return False
        
    return True # If they all fit

def run(data: list[str]) -> int:
    """
    Determines how many keys fit into the given locks based on their sizes.

    This function processes a list of lock and key data, calculates the size of each lock 
    and key, and counts how many keys can fit into each lock. A key is considered to fit 
    if all its teeth are within the corresponding pin heights of the lock.

    Args:
        data (list[str]): A list of strings, where each string represents either a lock 
                          or a key pattern. Locks and keys are distinguished by specific 
                          prefixes in the data.

    Returns:
        int: The total number of keys that fit into any of the locks.
    """
    # Parse the data into locks and keys, and predetermine the sizes of the keys
    locks, keys = parse_data(data)
    key_sizes = parse_keys(keys)

    keys_that_fit = 0
    # Check each lock against each key to see which ones fit
    for lock in locks:
        lock_size = get_lock_size(lock)
        for key_size in key_sizes:
            keys_that_fit += does_key_fit(key_size, lock_size)
    
    return keys_that_fit

inputfile = Path(r"day25.txt")
data = read_inputfile(inputfile)
data = data.split('\n\n')
part1_result = run(data)

print('Part 1:', part1_result)
if part1_result == 3291:
    print('PASS')