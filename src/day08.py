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

def count_trees(li, height_limit):
    count = 0
    for tree in li:
        count += 1
        if tree >= height_limit:
            return count
    return count

def scenic_score(data, x, y):
    my_height = data[x,y]
    up = count_trees(data[:x,y][::-1], my_height)
    left = count_trees(data[x,:y][::-1], my_height)
    right = count_trees(data[x,y+1:], my_height)
    down = count_trees(data[x+1:,y], my_height)
    return up * left * right * down

def max_scenic_score(data):
    max_x, max_y = data.shape
    best_seen = 0
    for x in range(max_x):
        for y in range(max_y):
            best_seen = max(scenic_score(data, x, y), best_seen)
    return best_seen

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

def test_scenic_score():
    data = fetch_data('sample_data/day08.txt')
    assert scenic_score(data, 1, 2) == 4
    assert scenic_score(data, 3, 2) == 8

def test_max_scenic_score():
    data = fetch_data('sample_data/day08.txt')
    assert max_scenic_score(data) == 8

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day08.txt')
    print(max_scenic_score(data))
