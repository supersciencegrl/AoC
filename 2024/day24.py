from itertools import combinations
from pathlib import Path

example = """x00: 1
    x01: 0
    x02: 1
    x03: 1
    x04: 0
    y00: 1
    y01: 1
    y02: 1
    y03: 1
    y04: 1

    ntg XOR fgs -> mjb
    y02 OR x01 -> tnw
    kwq OR kpj -> z05
    x00 OR x03 -> fst
    tgd XOR rvg -> z01
    vdt OR tnw -> bfw
    bfw AND frj -> z10
    ffh OR nrd -> bqk
    y00 AND y03 -> djm
    y03 OR y00 -> psh
    bqk OR frj -> z08
    tnw OR fst -> frj
    gnj AND tgd -> z11
    bfw XOR mjb -> z00
    x03 OR x00 -> vdt
    gnj AND wpb -> z02
    x04 AND y00 -> kjc
    djm OR pbm -> qhw
    nrd AND vdt -> hwm
    kjc AND fst -> rvg
    y04 OR y02 -> fgs
    y01 AND x02 -> pbm
    ntg OR kjc -> kwq
    psh XOR fgs -> tgd
    qhw XOR tgd -> z09
    pbm OR djm -> kpj
    x03 XOR y03 -> ffh
    x00 XOR y04 -> ntg
    bfw OR bqk -> z06
    nrd XOR fgs -> wpb
    frj XOR qhw -> z04
    bqk OR frj -> z07
    y03 OR x01 -> nrd
    hwm AND bqk -> z03
    tgd XOR rvg -> z12
    tnw OR pbm -> gnj"""
example = example.split('\n    ')

example2 = """x00: 0
    x01: 1
    x02: 0
    x03: 1
    x04: 0
    x05: 1
    y00: 0
    y01: 0
    y02: 1
    y03: 1
    y04: 0
    y05: 1

    x00 AND y00 -> z05
    x01 AND y01 -> z02
    x02 AND y02 -> z01
    x03 AND y03 -> z03
    x04 AND y04 -> z04
    x05 AND y05 -> z00"""
example2 = example2.split('\n    ')

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

def parse_gate(line: str) -> dict[str, str | list[str, str]]:
    """
    Parses a string representing a logic gate operation into its components.

    This function processes a line describing a logic gate operation, identifying the gate type,
    its input wires, and its output wire. It supports XOR, OR, and AND gate types and returns
    a dictionary containing the parsed components.

    Args:
        line (str): A string representing a logic gate operation in the format 
                    "input1 GATE input2 -> output", where GATE is one of "XOR", "OR", or "AND".

    Returns:
        dict[str, str | list[str]]: A dictionary with the following keys:
            - 'gate_type': A string representing the type of gate ("XOR", "OR", "AND").
            - 'inputs': A list of two strings representing the input wires for the gate.
            - 'output': A string representing the output wire.
    """
    combination, _, wire = line.partition(' -> ')
    for gate_type in [' XOR ', ' OR ', ' AND ']:
        if gate_type in combination:
            # Get the input wires and create dictionary
            gate_inputs = combination.split(gate_type)
            gate = {'gate_type': gate_type.strip(),
                    'inputs': gate_inputs,
                    'output': wire
                    }
            
    return gate

def parse_data(data: list[str]
               ) -> tuple[dict[str, str], list[dict[str, str | list[str, str]]]]:
    """
    Parses a list of strings into inputs and gates for a logic circuit.

    This function processes a list of strings where each string represents either a wire 
    assignment or a logic gate operation. Wire assignments are parsed into an inputs 
    dictionary, while logic gate operations are parsed into a list of gate dictionaries.

    Args:
        data (list[str]): A list of strings where each string is a wire assignment 
                          "wire: value" or a logic gate operation 
                          "input1 GATE input2 -> output".

    Returns:
        tuple[dict[str, str], list[dict[str, str | list[str]]]]: A tuple containing:
            - A dictionary with wire names as keys and their assigned values as strings.
            - A list of dictionaries, each representing a parsed logic gate with keys 
              'gate_type', 'inputs', and 'output'.
    """
    inputs = {}
    gates = []

    for line in data:
        if ':' in line: # It's an input wire
            wire, _, output = line.partition(': ')
            inputs[wire] = output.strip()
        elif '->' in line: # It's a gate
            gate = parse_gate(line)
            gates.append(gate)
    
    return inputs, gates

def evaluate_output(gate: dict[str, str | list[str, str]]) -> str:
    """
    Evaluates the output of a logic gate based on its type and input values.

    This function determines the output of a logic gate by checking its type and the values 
    of its inputs. It supports AND, XOR, and OR gate types, and returns '1' for a true 
    output and '0' for false, based on standard logic gate behavior.

    Args:
        gate (dict): A dictionary representing a logic gate with keys:
            - 'gate_type': A string indicating the type of gate ('AND', 'XOR', 'OR').
            - 'input_values': A list of strings ('0' or '1') representing the input values 
              to the gate.

    Returns:
        str: A string ('0' or '1') representing the output value of the gate.
    """
    gate_type = gate['gate_type']
    values = gate['input_values']
    if gate_type == 'AND' and values.count('1') == 2:
        return '1'
    elif gate_type == 'XOR' and values.count('1') == 1:
        return '1'
    elif gate_type == 'OR' and values.count('1') >= 1:
        return '1'
    else:
        return '0'

def evaluate_inputs(inputs: dict[str, str],
                    gates: list[dict[str, str | list[str, str]]]
                    ) -> list[dict[str, str | list[str, str]]]:
    """
    Evaluates the outputs of a series of logic gates based on initial input values.

    This function iterates through a queue of logic gates, evaluating each gate's output once all
    its input wires have been assigned values. The output of each gate is then added to the inputs,
    and the process continues until all gates have been evaluated.

    Args:
        inputs (dict[str, str]): A dictionary where keys are wire names and values are their binary
                                 values ('0' or '1').
        gates (list[dict]): A list of dictionaries, each representing a logic gate with keys:
            - 'gate_type': A string indicating the type of gate ('AND', 'XOR', or 'OR').
            - 'inputs': A list of strings representing the input wire names for the gate.
            - 'output': A string representing the output wire name for the gate.

    Returns:
        list[dict]: A list of dictionaries representing the gates, each updated with evaluated
                    input values and output values.
    """
    queue = gates[:]
    while queue:
        for gate in list(queue):
            # If we know both input values, evaluate the output value
            if all(input_wire in inputs for input_wire in gate['inputs']):
                gate['input_values'] = [inputs[input_wire] for input_wire in gate['inputs']]
                gate['output_value'] = evaluate_output(gate)
                # Update the inputs dict so this output can be another input
                inputs[gate['output']] = gate['output_value']
                queue.remove(gate) # We now know all we need to about the gate
    
    return gates

def calculate_result(gates):
    """
    Calculates a decimal result from the outputs of specific logic gates.

    This function processes a list of logic gates, specifically those whose output names start
    with 'z'. It sorts these gates alphabetically by their output names, concatenates their 
    output values into a binary string, reverses this string, and converts it to a decimal number.

    Args:
        gates (list[dict]): A list of dictionaries representing logic gates. Each dictionary should
                            contain:
            - 'output': A string representing the output wire name.
            - 'output_value': A string ('0' or '1') representing the evaluated output value.

    Returns:
        int: The decimal representation of the concatenated binary output values from the sorted 
             gates.
    """
    result = ''
    # Sort all gates starting with 'z' into numerical (alphabetical) order
    result_gates = sorted([gate for gate in gates if gate['output'].startswith('z')], 
                          key = lambda g: g['output']
                          )
    for result_gate in result_gates:
        result += result_gate['output_value']
    
    decimal_result = int(result[::-1], 2) # Convert binary (in reverse) to decimal

    return decimal_result

def generate_pairs(swap_system):
    all_pairs = list(combinations(swap_system, 2))
    unique_pair_sets = []

    # Generate combinations of pairs
    def backtrack(current_set, remaining_pairs, remaining_items):
        if len(current_set) == 4:
            sorted_set = tuple(sorted(current_set))
            if sorted_set not in unique_pair_sets:
                unique_pair_sets.append(sorted_set)
            return
    
        for i, pair in enumerate(remaining_pairs):
            # Don't reuse items
            if not any([item in remaining_items for item in pair]):
                continue
            new_set = current_set + [pair]
            new_remaining_pairs = remaining_pairs[i+1:]
            new_remaining_items = remaining_items - set(pair)
            backtrack(new_set, new_remaining_pairs, new_remaining_items)
    
    backtrack([], all_pairs, set(swap_system))

    return unique_pair_sets

def part2(gates):
    gate_outputs = [gate['output'] for gate in gates]
    # Lol I was trying to brute force it, but MemoryError so fast
    possible_swap_systems = list(combinations(gate_outputs, 8))

    for system in possible_swap_systems:
        pairs = generate_pairs(system)
    
    return pairs

def run(data):
    """
    Processes a list of logic circuit data to evaluate gate outputs and calculate a final result.

    This function takes a list of strings representing wire inputs and logic gate operations,
    parses them, evaluates the outputs of the gates based on the inputs, and computes a final
    result by converting specific gate outputs from binary to decimal.

    Args:
        data (list[str]): A list of strings where each string represents a wire input assignment
                          or a logic gate operation.

    Returns:
        int: The decimal result calculated from the binary outputs of gates whose output names
             start with 'z', after evaluation and processing.
    """
    inputs, gates = parse_data(data)

    gates_part1 = evaluate_inputs(inputs, gates)
    part1_result = calculate_result(gates_part1)

    return part1_result

inputfile = Path(r"day24.txt")
data = read_inputfile(inputfile)
part1_result = run(data)

print('Part 1:', part1_result)
if part1_result == 55920211035878:
    print('PASS')