import numpy as np
from collections import namedtuple
from collections import deque

class Heightmap:
    Pos = namedtuple("Pos", "x y")

    def __init__(self, grid, start, target):
        self.grid = np.array(grid)
        self.start = Heightmap.Pos(*start)
        self.target = Heightmap.Pos(*target)

    def can_move_to(self, explore_from):
        neighbours = []
        if explore_from.x > 0:
            neighbours.append(Heightmap.Pos(explore_from.x -1, explore_from.y))
        if explore_from.x < (self.grid.shape[0] -1):
            neighbours.append(Heightmap.Pos(explore_from.x +1, explore_from.y))
        if explore_from.y > 0:
            neighbours.append(Heightmap.Pos(explore_from.x, explore_from.y -1))
        if explore_from.y < (self.grid.shape[1] -1):
            neighbours.append(Heightmap.Pos(explore_from.x, explore_from.y +1))

        for n in neighbours:
            if 0 <= self.grid[n] <= self.grid[explore_from] + 1:
                yield n


    def shortest_path(self):
        return len(self._explore(self.start, [])) -1

    def _explore(self, explore_from, path_so_far):
        choices = []
        path_to_here = path_so_far + [explore_from]
        for neighbour in self.can_move_to(explore_from):
            if neighbour == self.target:
                return path_to_here + [neighbour]
            elif neighbour not in path_so_far:
                route_to_target = self._explore(neighbour, path_to_here)
                if route_to_target:
                    choices.append(route_to_target)
        if choices:
            return min(choices, key=len)
        else:
            return []

    def shortest_path_sooner(self):
        node, parent = self._depth_first_search()
        length = 0
        
        while parent:
            length += 1
            node, parent = parent
        return length

    def _depth_first_search(self):
        explored = set()
        Q = deque()
        explored.add(self.start)
        Q.append((self.start, None))
        while len(Q):
            v, parent = Q.popleft()
            if v == self.target:
                return v, parent
            for neighbour in self.can_move_to(explore_from=v):
                if neighbour not in explored:
                    explored.add(neighbour)
                    Q.append((neighbour, (v, parent)))

    

def fetch_data(path):
    with open(path, 'r') as f:
        grid = []
        for (x, ln) in enumerate(f):
            row = []
            for (y, c) in enumerate(ln.strip()):
                if c == 'S':
                    start = (x,y)
                    row.append(ord('a'))
                elif c == 'E':
                    target = (x,y)
                    row.append(ord('z'))
                else:
                    row.append(ord(c))
            grid.append(row)           
        return Heightmap(grid, start, target)

#--------------------- tests -------------------------#

def test_basics():
    heightmap = fetch_data('sample_data/day12.txt')
    assert heightmap.grid.shape == (5,8)
    assert heightmap.start == (0,0)
    assert heightmap.target == (2,5)

def test_can_move_to():
    heightmap = fetch_data('sample_data/day12.txt')
    assert list(heightmap.can_move_to(explore_from=Heightmap.Pos(0,0))) == [(1,0),(0,1)]
    assert len(list(heightmap.can_move_to(explore_from=heightmap.target))) == 4


def test_shortest_path_straight():
    heightmap = Heightmap(grid=[[0,0,1]], start=(0,0), target=(0,2))
    assert heightmap.shortest_path_sooner() == 2

def test_shortest_path_avoid_loops():
    grid = [
        [0, 0, 0],
        [0, 0, 1]
    ]
    heightmap = Heightmap(grid, start=(0,0), target=(1,2))
    assert heightmap.shortest_path_sooner() == 3

def test_find_shortest_path():
    heightmap = fetch_data('sample_data/day12.txt')
    assert heightmap.shortest_path_sooner() == 31


#-----------------------------------------------------#

if __name__ == "__main__":
    heightmap = fetch_data('data/day12.txt')
    print(heightmap.shortest_path_sooner())
