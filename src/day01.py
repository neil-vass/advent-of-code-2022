def fetch_data(path):
    with open(path, 'r') as f:
        accumulator = 0
        for ln in f:
            if len(ln.rstrip()):
                accumulator += int(ln)
            else:
                yield accumulator
                accumulator = 0
        yield accumulator

def get_sum_of_top_elves(data, n):
    return sum(sorted(data)[-n:])

#--------------------- tests -------------------------#

def test_fetch_data_gives_calorie_sums():
    data = fetch_data('sample_data/day01.txt')
    assert [c for c in data] == [6000, 4000, 11000, 24000, 10000]

def test_get_sum_of_top_elves():
    data = fetch_data('sample_data/day01.txt')
    assert get_sum_of_top_elves(data, 3) == 45000


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day01.txt')
    print(get_sum_of_top_elves(data, 3))
