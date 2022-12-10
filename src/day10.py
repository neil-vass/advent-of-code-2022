def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            vals = ln.rstrip().split()
            if vals[0] == 'noop':
                yield 'noop', None, 1
            else:
                yield 'addx', int(vals[1]), 2

def execute(data):
    X = 1
    for op, arg, cycles in data:
        for _ in range(cycles):
            yield X
        if op == 'addx':
            X += arg
    yield X
           
def get_signal_strengths(data):
    system = execute(data)
    sample_during = [20, 60, 100, 140, 180, 220]
    signal_strengths = []
    for cycle in range(220):
        register = next(system)
        if cycle+1 in sample_during:
            strength = (cycle+1) * register
            signal_strengths.append(strength)
    return signal_strengths




#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day10-small.txt')
    assert next(data) == ('noop', None, 1)
    assert next(data) == ('addx', 3, 2)
    assert next(data) == ('addx', -5, 2)

def test_small_program():
    data = fetch_data('sample_data/day10-small.txt')
    assert list(execute(data)) == [1, 1, 1, 4, 4, -1]

def test_larger_program():
    data = fetch_data('sample_data/day10.txt')
    signal_strengths = get_signal_strengths(data)
    assert signal_strengths == [420, 1140, 1800, 2940, 2880, 3960]
    assert sum(signal_strengths) == 13140

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day10.txt')
    print(sum(get_signal_strengths(data)))
