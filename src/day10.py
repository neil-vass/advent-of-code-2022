def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            # each instruction gives (cycles to wait, value to add)
            vals = ln.rstrip().split()
            if vals[0] == 'noop':
                yield 1, 0
            else:
                yield 2, int(vals[1])

def execute(data):
    X = 1
    for cycles, val in data:
        for _ in range(cycles):
            yield X
        X += val
    yield X
           
def get_signal_strengths(data):
    register_vals = execute(data)
    sample_during = [20, 60, 100, 140, 180, 220]
    signal_strengths = []
    for cycle in range(220):
        register = next(register_vals)
        if cycle+1 in sample_during:
            signal_strengths.append((cycle+1) * register)
    return signal_strengths


def draw_crt(data):
    draw_pos = 0
    row = ''
    register_vals = execute(data)
    for _ in range(241):
        if len(row) == 40:
            yield row
            draw_pos = 0
            row = ''
        reg = next(register_vals)
        row += '#' if (abs(reg - draw_pos) <= 1) else '.'
        draw_pos += 1


#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day10-small.txt')
    # 'noop': take 1 cycle, add nothing
    assert next(data) == (1, 0)
    # 'addx 3': take 2 cycles, add 3
    assert next(data) == (2, 3)
    # 'addx -5'
    assert next(data) == (2, -5)

def test_small_program():
    data = fetch_data('sample_data/day10-small.txt')
    assert list(execute(data)) == [1, 1, 1, 4, 4, -1]

def test_larger_program():
    data = fetch_data('sample_data/day10.txt')
    signal_strengths = get_signal_strengths(data)
    assert signal_strengths == [420, 1140, 1800, 2940, 2880, 3960]
    assert sum(signal_strengths) == 13140

def test_draw_crt():
    data = fetch_data('sample_data/day10.txt')
    assert list(draw_crt(data)) == [
        '##..##..##..##..##..##..##..##..##..##..',
        '###...###...###...###...###...###...###.',
        '####....####....####....####....####....',
        '#####.....#####.....#####.....#####.....',
        '######......######......######......####',
        '#######.......#######.......#######.....']


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day10.txt')
    for row in draw_crt(data):
        print(row)
