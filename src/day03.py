import functools


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.rstrip()

def priority(item):
    if 'a' <= item <= 'z':
        return ord(item) - 96
    else:
        return ord(item) - 38


def priority_of_common_items(rucksack):
    halfway = len(rucksack) // 2
    common_items = set(rucksack[:halfway]).intersection(rucksack[halfway:])
    return sum(priority(c) for c in common_items)


def fetch_groups(path):
    rucksacks = fetch_data(path)
    while True:
        try:
            yield [next(rucksacks) for _ in range(3)]
        except StopIteration:
            return

def priorty_of_badge(group):
    badges = functools.reduce(set.intersection, (set(rucksack) for rucksack in group))
    return sum(priority(b) for b in badges)

#--------------------- tests -------------------------#

def test_priority():
    assert priority('p') == 16
    assert priority('L') == 38
    assert priority('P') == 42

def test_priority_of_common_items():
    data = fetch_data('sample_data/day03.txt')
    rucksack = next(data)
    assert rucksack == 'vJrwpWtwJgWrhcsFMMfFFhFp'
    assert priority_of_common_items(rucksack) == 16

def test_sum_priorities_for_rucksacks():
    data = fetch_data('sample_data/day03.txt')
    assert sum(priority_of_common_items(r) for r in data) == 157

def test_fetch_groups():
    groups = fetch_groups('sample_data/day03.txt')
    assert next(groups) == [
        'vJrwpWtwJgWrhcsFMMfFFhFp',
        'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
        'PmmdzqPrVvPwwTWBwg'
    ]

def test_priorty_of_badge():
    groups = fetch_groups('sample_data/day03.txt')
    assert priorty_of_badge(next(groups)) == 18
    assert priorty_of_badge(next(groups)) == 52

def test_sum_priorities_for_badges():
    groups = fetch_groups('sample_data/day03.txt')
    assert sum(priorty_of_badge(g) for g in groups) == 70

#-----------------------------------------------------#

if __name__ == "__main__":
    groups = fetch_groups('data/day03.txt')
    print(sum(priorty_of_badge(g) for g in groups))