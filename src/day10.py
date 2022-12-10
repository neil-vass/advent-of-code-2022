def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            vals = ln.rstrip().split()
            if vals[0] == 'noop':
                yield 'noop', None, 1
            else:
                yield 'addx', int(vals[1]), 2

#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day10-small.txt')
    assert next(data) == ('noop', None, 1)
    assert next(data) == ('addx', 3, 2)
    assert next(data) == ('addx', -5, 2)

def test_small_program():
    pass

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day10.txt')
    print('Hello, World!')
