import numpy as np

def fetch_data(path):
    with open(path, 'r') as f:
        return np.array([[int(n) for n in ln.rstrip()] for ln in f])

def is_visible(data, x, y):
    return (
        max(data[x,:y], default=-1) < data[x,y] or
        max(data[x,y+1:], default=-1) < data[x,y] or
        max(data[:x,y], default=-1) < data[x,y] or
        max(data[x+1:,y], default=-1) < data[x,y]
    )

def count_visible(data):
    max_x, max_y = data.shape
    count = 0
    for x in range(max_x):
        for y in range(max_y):
            count += is_visible(data, x, y)
    return count



#--------------------- tests -------------------------#

# Let's make sure I understand how arrays work.
def test_basics():
    data = fetch_data('sample_data/day08.txt')
    assert data[0,0] == 3
    assert data[4,3] == 9
    assert max(data[1,3:]) == 2
    assert data.shape == (5,5)

def test_is_visible():
    data = fetch_data('sample_data/day08.txt')
    assert is_visible(data, 0, 0)
    assert is_visible(data, 1, 1)
    assert not is_visible(data, 1, 3)
    assert not is_visible(data, 2, 2)

def test_count_visible():
    data = fetch_data('sample_data/day08.txt')
    assert count_visible(data) == 21

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day08.txt')
    print(count_visible(data))
