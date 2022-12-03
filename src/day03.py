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

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day03.txt')
    print(sum(priority_of_common_items(r) for r in data))