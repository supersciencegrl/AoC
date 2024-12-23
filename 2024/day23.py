from itertools import combinations
from pathlib import Path

example = """kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn"""
example = example.split()

def read_inputfile(inputfile: Path) -> list[str]:
    """
    Reads a text file and returns its contents, with leading/trailing whitespace removed.

    Args:
        inputfile (Path): The path to the input file to be read.

    Returns:
        str: A string representing the file contents, with leading/trailing whitespace removed. 
    """
    with open(inputfile, 'rt') as fin:
        data = fin.readlines()

    return [line.strip() for line in data]

def add_computers_to_dict(computers: tuple[str, str],
                          groups: dict[str, set[str]]
                          ) -> dict[str, set[str]]:
    """
    Adds a pair of connected computers to a dictionary, updating their respective connection sets.

    This function takes a tuple of two computers and a dictionary representing groups of connected
    computers. It ensures that each computer has an entry in the dictionary with a set of its
    connected partners. If a computer is already in the dictionary, its partner is added to its
    connection set.

    Args:
        computers (tuple[str, str]): A tuple containing two computer identifiers that are 
                                     connected.
        groups (dict[str, set[str]]): A dictionary where keys are computer identifiers and values
                                      are sets of computers they are connected to.

    Returns:
        dict[str, set[str]]: The updated dictionary with the new connections added.
    """
    for computer, partner in [(computers[0], computers[1]), (computers[1], computers[0])]:
        if computer not in groups:
            # Create a dict item for the computer and a set of its connections
            groups[computer] = set([partner])
        else: # Add partner to the existing set in the dict
            groups[computer].add(partner)
    
    return groups

def find_groups(data) -> dict[str, set[str]]:
    """
    Constructs a dictionary of connected computer groups from a list of connections.

    This function processes a list of connection strings, where each string represents a
    connection between two computers in the format "computer1-computer2". It uses these
    connections to build a dictionary where each key is a computer identifier and each value
    is a set of computers it is directly connected to.

    Args:
        data (list[str]): A list of strings, each representing a connection between two
                          computers in the format "computer1-computer2".

    Returns:
        dict[str, set[str]]: A dictionary representing groups of connected computers, where
                             each key is a computer identifier and each value is a set of
                             directly connected computers.
    """
    groups = {}
    for connection in data:
        # Parse the connection to retrieve the computers
        computer1, _, computer2 = connection.partition('-')
        groups = add_computers_to_dict((computer1, computer2), groups)

    return groups

def find_cliques(graph: dict[str, set[str]]) -> list[set]:
    """
    Identifies all cliques within a given graph.

    A clique is a subnetwork where all nodes are directly connected to each other. This function
    uses a backtracking approach to find all such cliques in the input graph, which is 
    represented as a dictionary of nodes and their connections.

    Args:
        graph (dict[str, set[str]]): A dictionary where keys are node identifiers and values are
                                     sets of nodes they are directly connected to.

    Returns:
        list[set]: A list of sets, each representing a clique found in the graph. Each set contains
                   node identifiers that form a clique.
    """
    def backtrack(possible_clique: set, remaining_nodes: set, skip_nodes: set):
        """
        Recursive helper function to explore potential cliques.

        Args:
            possible_clique (set): Current nodes that form a potential clique.
            remaining_nodes (set): Nodes that can be added to the current clique.
            skip_nodes (set): Nodes that should not be considered for the current clique
                              to avoid duplicates.
        """
        # If no remaining nodes or nodes to skip, we have completed finding the full clique
        if not remaining_nodes and not skip_nodes:
            cliques.append(possible_clique)
            return
        
        for node in list(remaining_nodes):
            # Attempt to add current node to possible clique
            new_clique = possible_clique | {node} # `|` is set union operator
            # Determine remaining nodes that can form a clique with current node
            new_remaining = remaining_nodes & graph[node] # `&` is set intersection operator
            # Determine the new nodes to skip to avoid duplicates
            new_skip = skip_nodes & graph[node]
            # Recursively explore further cliques
            backtrack(new_clique, new_remaining, new_skip)
            # Move the node from remaining to skip so it won't get processed again
            remaining_nodes.remove(node)
            skip_nodes.add(node)
    
    cliques = []
    all_nodes = set(graph)
    backtrack(set(), all_nodes, set())

    return cliques

def find_triangles(cliques: list[set]) -> list[tuple]:
    """
    Identifies all triangles within a list of cliques.

    This function processes each clique from the input list and generates all possible
    combinations of three nodes (triangles) within each clique. A triangle is a subset
    of three nodes where each node is directly connected to both others.

    Args:
        cliques (list[set]): A list of sets, where each set represents a clique of connected nodes.

    Returns:
        list[tuple]: A list of tuples, each containing three nodes that form a triangle within 
                     the cliques.
    """
    triangles = []
    for clique in cliques:
        triangles += list(combinations(clique, 3))

    return triangles

def run(data: list[str]) -> tuple(int, str):
    """
    Processes a list of connections to find specific network patterns and generates a password.

    This function analyzes a list of computer network connections to identify cliques and triangles.
    It filters triangles to find those (without duplicates) with at least one computer starting with 
    't' (Part 1), and constructs a password from the largest clique (Part 2).

    Args:
        data (list[str]): A list of strings, each representing a connection between two computers
                          in the format "computer1-computer2".

    Returns:
        tuple[int, str]: A tuple containing:
            - The number of unique triangles where at least one computer starts with 't'.
            - A password string formed by joining the sorted members of the largest clique.
    """
    groups = find_groups(data)
    cliques = find_cliques(groups)
    triangles = find_triangles(cliques)

    # Part 1: only return triangles where one computer starts with 't'
    chief_subnetworks = tuple(triangle for triangle in triangles if any([item.startswith('t') for item in triangle]))
    # Remove duplicates
    chief_subnetworks = set(tuple(tuple(sorted(network)) for network in chief_subnetworks))

    # Part 2
    party = sorted(list(max(cliques, key = len)))
    password = (',').join(party)

    return len(chief_subnetworks), password

inputfile = Path(r"day23.txt")
data = read_inputfile(inputfile)
part1_result, part2_result = run(data)

print('Part 1:', part1_result)
if part1_result == 1476:
    print('PASS')
print('Part 2:', part2_result)
if part2_result == 'ca,dw,fo,if,ji,kg,ks,oe,ov,sb,ud,vr,xr':
    print('PASS')