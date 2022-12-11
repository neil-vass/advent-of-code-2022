from functools import reduce
import re
import operator

class Monkey:
    def __init__(self, items, op, test_div, on_true, on_false):
        self.items = [int(i) for i in items]
        self.inspect = Monkey.create_operation(*op)
        self.test_div = int(test_div)
        self.on_true =  int(on_true)
        self.on_false =  int(on_false)
        self.manage_worry = lambda x: x // 3
        self.inspections = 0

    def create_operation(symbol, argument):
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul}
        if argument == 'old':
            return lambda x: ops[symbol](x, x)
        else:
            return lambda x: ops[symbol](x, int(argument))
    
    def inspect_and_throw(self, item):
        item = self.inspect(item)
        self.inspections += 1
        item = self.manage_worry(item)
        to_monkey = self.on_false if item % self.test_div else self.on_true
        return item, to_monkey

    def take_turn(self):
        for item in self.items:
            yield self.inspect_and_throw(item)
        self.items = []

    def catch(self, item):
        self.items.append(item)

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

def play_round(pack):
    for monkey in pack:
        for thrown_item, target_monkey in monkey.take_turn():
            pack[target_monkey].catch(thrown_item)

def find_active_monkeys(pack, rounds):
    for _ in range(rounds):
        play_round(pack)
    return sorted(m.inspections for m in pack)[-2:]


def manage_worries_for_part_2(monkeys):
    common_divisor = reduce(operator.mul, (m.test_div for m in monkeys))
    worry_manager = lambda x: x % common_divisor
    for m in monkeys:
        m.manage_worry = worry_manager

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

def test_take_turn():
    pack = fetch_monkeys('sample_data/day11.txt')
    assert list(pack[0].take_turn()) == [(500, 3), (620, 3)]
    assert len(pack[0].items) == 0
    assert pack[0].inspections == 2

def test_play_round():
    pack = fetch_monkeys('sample_data/day11.txt')
    play_round(pack)
    assert pack[0].items == [20, 23, 27, 26]
    assert pack[1].items == [2080, 25, 167, 207, 401, 1046]
    assert pack[2].items == []
    assert pack[3].items == []

def test_find_active_monkeys():
    pack = fetch_monkeys('sample_data/day11.txt')
    assert find_active_monkeys(pack, rounds=20) == [101, 105]

def test_part_2_early_rounds():
    pack = fetch_monkeys('sample_data/day11.txt')
    manage_worries_for_part_2(pack)
    play_round(pack)
    assert pack[0].inspections == 2
    assert pack[1].inspections == 4  

    find_active_monkeys(pack, rounds=19)
    assert pack[0].inspections == 99
    assert pack[1].inspections == 97  

def test_part_2_all_rounds():
    pack = fetch_monkeys('sample_data/day11.txt')
    manage_worries_for_part_2(pack)
    assert find_active_monkeys(pack, rounds=10000) == [52013, 52166]


#-----------------------------------------------------#

if __name__ == "__main__":
    pack = fetch_monkeys('data/day11.txt')
    manage_worries_for_part_2(pack)
    print(operator.mul(*find_active_monkeys(pack, rounds=10000)))
