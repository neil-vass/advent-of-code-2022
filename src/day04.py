import re

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield [int(n) for n in re.findall(r'\d+', ln)]

def is_contained(first_min, first_max, second_min, second_max):
    return ((first_min <= second_min and second_max <= first_max)
         or (second_min <= first_min and first_max <= second_max))

def has_partial_overlap(first_min, first_max, second_min, second_max):
    return ((first_min <= second_min <= first_max)
         or (first_min <= second_max <= first_max))

def has_overlap(first_min, first_max, second_min, second_max):
    return (is_contained(first_min, first_max, second_min, second_max) 
         or has_partial_overlap(first_min, first_max, second_min, second_max))

#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day04.txt')
    data = list(data)
    assert data[0] == [2, 4, 6, 8]
    assert len(data) == 6

def test_is_contained():
    assert not is_contained(2, 4, 6, 8)
    assert is_contained(2, 8, 3, 7)
    assert is_contained(6, 6, 3, 7)

def test_count_contained_pairs():
    data = fetch_data('sample_data/day04.txt')
    assert sum(is_contained(*p) for p in data) == 2

def test_has_overlap():
    assert not has_overlap(2, 4, 6, 8)
    assert not has_overlap(2, 3, 4, 5)
    assert has_overlap(5, 7, 7, 9)
    assert has_overlap(2, 8, 3, 7)

def test_count_overlapping_pairs():
    data = fetch_data('sample_data/day04.txt')
    assert sum(has_overlap(*p) for p in data) == 4

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day04.txt')
    print(sum(has_overlap(*p) for p in data))

