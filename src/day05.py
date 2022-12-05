from collections import defaultdict, deque
import re

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

def get_cols_and_crates(ln):
    return [(m.start(), m.group()) for m in re.finditer(r'\w', ln)]

# Advances 'data' past the stack setup, leaves it ready to run steps.
def get_starting_stacks(data):
    starting_stacks = defaultdict(deque)
    while True:
        ln = next(data)
        if ln.lstrip()[0] == '[':
            for col, crate in get_cols_and_crates(ln):
                starting_stacks[col].appendleft(crate)
        else:
            # We're at the crate labels. Use these instead of col positons as dict keys.
            for col, stack_name in get_cols_and_crates(ln):
                starting_stacks[stack_name] = starting_stacks[col]
                del starting_stacks[col]
            
            # Skip past the empty line, then we're done.
            next(data)
            return starting_stacks


def run_step(ln, stacks):
    num_crates, from_stack, to_stack = re.match(r'move (\d+) from (\d+) to (\d+)', ln).groups()
    for _ in range(int(num_crates)):
        stacks[to_stack].append(stacks[from_stack].pop())

def run_step_part_2(ln, stacks):
    num_crates, from_stack, to_stack = re.match(r'move (\d+) from (\d+) to (\d+)', ln).groups()
    mover = deque()
    for _ in range(int(num_crates)):
        mover.append(stacks[from_stack].pop())
    for _ in range(int(num_crates)):
        stacks[to_stack].append(mover.pop())


def get_stack_tops(data, mover_fn=run_step):
    stacks = get_starting_stacks(data)

    for step in data:
        mover_fn(step, stacks)

    return ''.join(stack.pop() for stack in stacks.values()) 


#--------------------- tests -------------------------#

def test_get_crates_and_cols():
    data = fetch_data('sample_data/day05.txt')
    assert get_cols_and_crates(next(data)) == [(5,'D')]
    assert get_cols_and_crates(next(data)) == [(1,'N'),(5,'C')]

def test_get_starting_stacks():
    data = fetch_data('sample_data/day05.txt')
    stacks = get_starting_stacks(data)
    assert len(stacks.keys()) == 3
    assert list(stacks['1']) == ['Z', 'N']
    assert stacks['2'].pop() == 'D'

def test_run_step():
    data = fetch_data('sample_data/day05.txt')
    stacks = get_starting_stacks(data)
    run_step(next(data), stacks)
    assert list(stacks['1']) == ['Z', 'N', 'D']
    assert list(stacks['2']) == ['M', 'C']
    assert list(stacks['3']) == ['P']

def test_get_stack_tops():
    data = fetch_data('sample_data/day05.txt')
    assert get_stack_tops(data) == 'CMZ'

def test_get_stack_tops_part_2():
    data = fetch_data('sample_data/day05.txt')
    assert get_stack_tops(data, run_step_part_2) == 'MCD'


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day05.txt')
    print('Part 1: ' + get_stack_tops(data))
    data = fetch_data('data/day05.txt')
    print('Part 2: ' + get_stack_tops(data, run_step_part_2))