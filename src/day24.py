import numpy as np
import math
import cProfile
from collections import namedtuple
from collections import deque

Pos = namedtuple("Pos", "x y")

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.rstrip()

def to_str(row):
    return ''.join(c if len(c) == 1 else len(c) for c in row)

class Valley:
    def __init__(self, data):
        self.map = np.array([[c for c in ln] for ln in data])
        self.height = self.map.shape[0] -2
        self.width = self.map.shape[1] -2
        self.repeats_after = math.lcm(self.height, self.width)
        self.entrance = Pos(0, np.where(self.map[0] == '.')[0][0])
        self.exit = Pos(self.map.shape[0]-1, np.where(self.map[-1] == '.')[0][0])

        self.futures = np.zeros((self.repeats_after+1, self.map.shape[0], self.map.shape[1]), dtype=bool)
        for x in range(self.map.shape[0]):
            for y in range(self.map.shape[1]):
                if self.map[x,y] in '<>^v':
                    for t in range(self.repeats_after+1):
                        if self.map[x,y] == '<':
                            self.futures[t, x, ((y -1 -t) % self.width +1)] = True
                        elif self.map[x,y] == '>':
                            self.futures[t, x, ((y -1 +t) % self.width +1)] = True
                        elif self.map[x,y] == '^':
                            self.futures[t, ((x -1 -t) % self.height +1), y] = True
                        elif self.map[x,y] == 'v':
                            self.futures[t, ((x -1 +t) % self.height +1), y] = True
    

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
        if self.futures[t, pos.x, pos.y]:
            return False
        return True
        
        # Check the map. Are there any blizzards that will hit pos at time t?
        right_bliz = ((pos.y -2 - t) % self.width) + 2
        if self.map[pos.x, right_bliz] == '>':
            return False

        left_bliz = ((pos.y -2 + t) % self.width) + 2
        if self.map[pos.x, left_bliz] == '<':
            return False

        down_bliz = ((pos.x -2 - t) % self.height) + 2
        if self.map[down_bliz, pos.y] == 'v':
            return False
            
        up_bliz = ((pos.x -2 + t) % self.height) + 2
        if self.map[up_bliz, pos.y] == '^':
            return False

        return True


    def choices_at(self, pos, t):
        for choice in self.adjacent_positions(pos):
            if self.will_be_clear(choice, t+1):
            #if self.futures[t+1, choice.x, choice.y]:
                    yield choice

    def shortest_path(self):   
        explored = {(self.entrance, 0)}
        queue = deque([(self.entrance, 0, 0)])
        while queue:
            pos, pattern, path_length = queue.popleft()
            if pos == self.exit:
                return path_length
            next_pattern = (path_length+1) % self.repeats_after
            for neighbour in self.choices_at(pos, next_pattern-1):
                if (neighbour, next_pattern) not in explored:
                    explored.add((neighbour, next_pattern))
                    queue.append((neighbour, next_pattern, path_length+1))
        raise Exception('No path found')


#--------------------- tests -------------------------#

def test_create_valley():
    data = fetch_data('sample_data/day24-simple.txt')
    valley = Valley(data)
    assert to_str(valley.map[0]) == '#.#####'
    assert valley.map[2,1] == '>'
    assert to_str(valley.map[-1]) == '#####.#'
    assert valley.entrance == (0,1)
    assert valley.exit == (6,5)

def test_choices_at_t_0():
    data = fetch_data('sample_data/day24-simple.txt')
    valley = Valley(data)
    assert set(valley.choices_at(valley.entrance, t=0)) == {(0,1), (1,1)}
    # Blizzard will move and we can also move down to (2,1).
    assert set(valley.choices_at(Pos(1,1), t=0)) == {(1,1), (0,1), (1,2), (2,1)}

def test_choices_at_t_1():
    data = fetch_data('sample_data/day24-simple.txt')
    valley = Valley(data)
    # Can't stand still, a blizzard will wrap off the bottom and hit us.
    assert set(valley.choices_at(Pos(1,4), t=1)) == {(1,3), (1,5), (2,4)}
    # Standing to the right of that, can't move onto blizzard.
    assert set(valley.choices_at(Pos(1,5), t=1)) == {(1,5), (2,5)}

def test_edge_cases():
    valley = Valley([
        '#.###',
        '#...#',
        '#.>>#',
        '###.#'])
    assert valley.shortest_path() == 6

def test_check_work():
    data = fetch_data('data/day24.txt')
    valley = Valley(data)
    assert valley.will_be_clear(Pos(9,25), t=4)
    

def test_shortest_path():
    #data = fetch_data('data/day24.txt')
    data = fetch_data('sample_data/day24-complex.txt')
    valley = Valley(data)
    assert valley.shortest_path() == 18

#-----------------------------------------------------#

def shortest_path():
    data = fetch_data('data/day24.txt')
    valley = Valley(data)
    print(valley.shortest_path())

if __name__ == "__main__":
    cProfile.run('shortest_path()', sort='cumulative')
    # 217 is too low