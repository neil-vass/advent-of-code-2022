import operator

operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}

def fetch_monkeys(path):
    with open(path, 'r') as f:
        monkeys = {}
        for ln in f:
            name, job = ln.rstrip().split(': ')
            if job.isdecimal():
                job = int(job)
            else:
                a, op, b = job.split()
                op = operators[op]
                job = (a, op, b)
            monkeys[name] = job
    return monkeys


def yell(monkeys, name):
    job = monkeys[name]
    if type(job) is not int:
        a, op, b = job
        job = op(yell(monkeys, a), yell(monkeys, b))
    return job
    
def yell_part_2(monkeys, name):
    pass

#--------------------- tests -------------------------#

def test_fetch_monkeys():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert monkeys['root'] == ('pppw', operator.add, 'sjmn')
    assert monkeys['hmdt'] == 32

def test_find_root():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert yell(monkeys, 'root') == 152

def test_yell_part_2():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert yell_part_2(monkeys) == 301

#-----------------------------------------------------#

if __name__ == "__main__":
    monkeys = fetch_monkeys('data/day21.txt')
    print(yell(monkeys, 'root'))
