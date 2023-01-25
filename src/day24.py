import numpy as np

def fetch_data(path):
    with open(path, 'r') as f:
        return np.array([[c for c in ln.rstrip()] for ln in f])

class Valley:
    def __init__(self, data):
        self.map = data
        self.entrance = (0, np.where(data[0] == '.')[0][0])
        self.exit = (data.shape[0]-1, np.where(data[-1] == '.')[0][0])


#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day24.txt')
    assert ''.join(data[0]) == '#.#####'
    assert data[2,1] == '>'
    assert ''.join(data[-1]) == '#####.#'

def test_create_valley():
    data = fetch_data('sample_data/day24.txt')
    valley = Valley(data)
    assert valley.entrance == (0,1)
    assert valley.exit == (6,5)


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day24.txt')
    print('Hello, World!')
