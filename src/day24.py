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

def pos_at(width, initial, t, backwards=False):
    if backwards: 
        t = -t
    return ((initial -1 + t) % width) +1

def test_moving_blizzards_forwards():
    row = '#.>....#'
    width = 6 # clear area to move in
    initial = row.index('>')
    assert pos_at(width, initial, t=3) == 5
    assert pos_at(width, initial, t=width) == initial
    assert pos_at(width, initial, t=5) == 1


def test_moving_blizzards_backwards():
    row = '#.<....#'
    width = 6 # clear area to move in
    initial = row.index('<')
    assert pos_at(width, initial, t=1, backwards=True) == 1
    assert pos_at(width, initial, t=width, backwards=True) == initial
    assert pos_at(width, initial, t=5, backwards=True) == 3

def will_be_blocked(row, width, pos, t):
    blizzard_will_move_right_from = ((pos -2 - t) % width) + 2
    if row[blizzard_will_move_right_from] == '>':
        return True
    blizzard_will_move_left_from = ((pos -2 + t) % width) + 2
    if row[blizzard_will_move_left_from] == '<':
        return True
    return False

def test_check_if_blocked():
    # The real question! I'm thinking of moving to a pos, will it be free?
    row = '#.>....#'
    width = 6 # clear area to move in
    initial = row.index('>')
    assert will_be_blocked(row, width, pos=5, t=3)
    row = '#.<....#'
    assert will_be_blocked(row, width, pos=5, t=3)
    assert will_be_blocked(row, width, pos=5, t=1) == False
  


def test_choices_at_t_0():
    data = fetch_data('sample_data/day24.txt')
    valley = Valley(data)
    assert set(valley.choices_at(valley.entrance, t=0)) == {(0,1), (1,1)}
    # Blizzard will move and we can also move down to (2,1).
    assert set(valley.choices_at(Pos(1,1), t=0)) == {(1,1), (0,1), (1,2), (2,1)}



#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day24.txt')
    print('Hello, World!')
