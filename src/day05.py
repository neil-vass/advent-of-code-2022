from collections import defaultdict, deque
import re

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

def get_cols_and_crates(ln):
    return [(m.start(), m.group()) for m in re.finditer(r'\w', ln)]

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

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day05.txt')
    print('Hello, World!')
