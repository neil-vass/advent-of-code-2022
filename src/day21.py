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
    

class HumnExpression:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        if self.expr == 'humn': 
            return 'humn'
        a, op, b = self.expr
        op = next(k for k,v in operators.items() if v == op)
        if op == '/': 
            op = '//'
        return f'({repr(a)} {op} {repr(b)})'


def invert(op):
    if op == operator.add: return operator.sub
    if op == operator.sub: return operator.add
    if op == operator.mul: return operator.floordiv
    if op == operator.floordiv: return operator.mul


def evaluate(humn_expression, target):
    if humn_expression.expr == 'humn':
        return target
    
    a, op, b = humn_expression.expr
    inverse_op = invert(op)
    if type(a) is HumnExpression:
        new_target = inverse_op(target, b)
        new_expr = a
    else:
        if op in (operator.sub, operator.floordiv):
            new_target = op(a, target)
        else:
            new_target = inverse_op(target, a)
        new_expr = b
    return evaluate(new_expr, new_target)


def yell_unless_humn(monkeys, name):
    if name == 'humn':
        return HumnExpression('humn')
    
    job = monkeys[name]
    if type(job) is int:
        return job

    a, op, b = job
    a, b = yell_unless_humn(monkeys, a), yell_unless_humn(monkeys, b)
    if type(a) is int and type(b) is int:
        return op(a, b)
    else:
        return HumnExpression((a, op, b))
    

def humn_needs_to_yell(monkeys):
    left, _, right = monkeys['root']
    left_result = yell_unless_humn(monkeys, left)
    right_result = yell_unless_humn(monkeys, right)
    target = left_result if type(left_result) is int else right_result
    humn_expression = left_result if type(left_result) is HumnExpression else right_result
    return evaluate(humn_expression, target)

#--------------------- tests -------------------------#

def test_fetch_monkeys():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert monkeys['root'] == ('pppw', operator.add, 'sjmn')
    assert monkeys['hmdt'] == 32

def test_find_root():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert yell(monkeys, 'root') == 152

def test_simple_humn_needs_to_yell():
    monkeys = {
        'root': ('humn', operator.add, 'aaaa'),
        'humn': 2,
        'aaaa': 5
    }
    assert humn_needs_to_yell(monkeys) == 5

def test_humn_needs_to_yell():
    monkeys = fetch_monkeys('sample_data/day21.txt')
    assert humn_needs_to_yell(monkeys) == 301

#-----------------------------------------------------#

if __name__ == "__main__":
    monkeys = fetch_monkeys('data/day21.txt')
    print(humn_needs_to_yell(monkeys))


