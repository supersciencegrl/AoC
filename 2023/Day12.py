example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

example = example.split('\n')

def read_input(input_text):
    instructions = {k:v for v,k in [line.split() for line in input_text]}

    return instructions

def generate_possibilities(springs: str, runs: str):
    run_list = [int(run) for run in runs.split(',')]
    total_springs = sum(run_list)
    archetype = ('.').join(['#'*n for n in run_list])

    return archetype
