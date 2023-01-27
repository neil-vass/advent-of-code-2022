import numpy as np
from collections import namedtuple
from collections import deque

Pos = namedtuple("Pos", "x y")

def fetch_data(path):
    with open(path, 'r') as f:
        return np.array([[c for c in ln.rstrip()] for ln in f])

def to_str(row):
    return ''.join(c if len(c) == 1 else len(c) for c in row)

class Valley:
    def __init__(self, data):
        self.map = data
        self.height = data.shape[0] -2
        self.width = data.shape[1] -2
        self.entrance = Pos(0, np.where(data[0] == '.')[0][0])
        self.exit = Pos(data.shape[0]-1, np.where(data[-1] == '.')[0][0])

    def adjacent_positions(self, pos):
        yield pos
        if pos.x > 0:
            yield Pos(pos.x-1, pos.y)
        if pos.y > 0:
            yield Pos(pos.x, pos.y-1)
        if pos.x < self.map.shape[0] -1:
            yield Pos(pos.x+1, pos.y)
        if pos.y < self.map.shape[1] -1:
            yield Pos(pos.x, pos.y+1)
        

    def will_be_clear(self, pos, t):
        if self.map[pos] == '#':
            return False
        
        # Check the map. Are there any blizzards that will hit pos at time t?
        right_bliz = ((pos.y -2 - t) % self.width) + 2
        if self.map[pos.x, right_bliz] == '>':
            return False

        left_bliz = ((pos.y -2 + t) % self.width) + 2
        if self.map[pos.x, left_bliz] == '<':
            return False

        down_bliz = ((pos.x -2 - t) % self.width) + 2
        if self.map[down_bliz, pos.y] == 'v':
            return False
            
        up_bliz = ((pos.y -2 + t) % self.width) + 2
        if self.map[up_bliz, pos.y] == '^':
            return False

        return True


    def choices_at(self, pos, t):
        # About to step to t+1. Ignore blizzards moving for now.
        for choice in self.adjacent_positions(pos):
            if self.will_be_clear(choice, t+1):
                    yield choice


#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day24.txt')
    assert to_str(data[0]) == '#.#####'
    assert data[2,1] == '>'
    assert to_str(data[-1]) == '#####.#'

def test_create_valley():
    data = fetch_data('sample_data/day24.txt')
    valley = Valley(data)
    assert valley.entrance == (0,1)
    assert valley.exit == (6,5)

def test_choices_at_t_0():
    data = fetch_data('sample_data/day24.txt')
    valley = Valley(data)
    assert set(valley.choices_at(valley.entrance, t=0)) == {(0,1), (1,1)}
    # Blizzard will move and we can also move down to (2,1).
    assert set(valley.choices_at(Pos(1,1), t=0)) == {(1,1), (0,1), (1,2), (2,1)}

def test_choices_at_t_1():
    data = fetch_data('sample_data/day24.txt')
    valley = Valley(data)
    # Can't stand still, a blizzard will wrap off the bottom and hit us.
    assert set(valley.choices_at(Pos(1,4), t=1)) == {(1,3), (1,5), (2,4)}
    # Standing to the right of that, can't move onto blizzard.
    assert set(valley.choices_at(Pos(1,5), t=1)) == {(1,5), (2,5)}


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day24.txt')
    print('Hello, World!')
