import re
import operator

class Monkey:
    def __init__(self, items, op, test_div, on_true, on_false):
        self.items = [int(i) for i in items]
        self.inspect = Monkey.create_operation(*op)
        self.test_div = int(test_div)
        self.on_true =  int(on_true)
        self.on_false =  int(on_false)
        self.inspected = 0

    def create_operation(symbol, argument):
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul}
        if argument == 'old':
            return lambda x: ops[symbol](x, x)
        else:
            return lambda x: ops[symbol](x, int(argument))
    
    def inspect_and_throw(self, item):
        item = self.inspect(item)
        self.inspected += 1
        item //= 3
        to_monkey = self.on_false if item % self.test_div else self.on_true
        return item, to_monkey

    def take_turn(self):
        for item in self.items:
            yield self.inspect_and_throw(item)
        self.items = []


def fetch_monkeys(path):
    pack = []
    with open(path, 'r') as f:
        for ln in f: 
            if ln.startswith('Monkey'):
                pack.append(Monkey(
                    items = re.findall('(\d+)', next(f)),
                    op = next(f).split()[-2:],
                    test_div = next(f).split()[-1],
                    on_true = next(f).split()[-1],
                    on_false = next(f).split()[-1]
            ))
    return pack

#--------------------- tests -------------------------#

def test_fetch_monkeys():
    pack = fetch_monkeys('sample_data/day11.txt')
    assert len(pack) == 4
    assert pack[0].items == [79, 98]
    assert pack[0].test_div == 23
    assert pack[3].items == [74]
    assert pack[3].on_true == 0
    assert pack[3].on_false == 1

def test_inspection():
    pack = fetch_monkeys('sample_data/day11.txt')
    assert pack[0].inspect(2) == 38 # multiply by 19
    assert pack[1].inspect(2) == 8 # + 6

def test_inspect_and_throw():
    pack = fetch_monkeys('sample_data/day11.txt')
    assert pack[0].inspect_and_throw(79) == (500, 3)

def test_play_round():
    pack = fetch_monkeys('sample_data/day11.txt')
    #assert pack[0].take_turn() == 0

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_monkeys('data/day11.txt')
    print('Hello, World!')
