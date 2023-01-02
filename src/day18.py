from collections import namedtuple
from collections import deque

Pos = namedtuple("Pos", "x y z")


class Scan:
    def __init__(self, cubes):
        self.cubes = set(cubes)
        
         # Find extents
        all_x, all_y, all_z = zip(*self.cubes)
        self.min_extent = Pos(min(all_x)-1, min(all_y)-1, min(all_z)-1)
        self.max_extent = Pos(max(all_x)+1, max(all_y)+1, max(all_z)+1)
        
    
    def surface_area(self):
        surfaces = [6 - self.sides_touching(c) for c in self.cubes]
        return sum(surfaces)

    def sides_touching(self, target_cube):
        touching = [n for n in Scan.get_neighbours(target_cube) if n in self.cubes]
        return len(touching)

    def get_neighbours(point):
        x,y,z = point
        return [Pos(x-1,y,z), Pos(x+1,y,z), 
                Pos(x,y-1,z), Pos(x,y+1,z), 
                Pos(x,y,z-1), Pos(x,y,z+1)]

    def can_move_to(self, explore_from):
        moves = []
        for neighbour in Scan.get_neighbours(explore_from):
            if ((self.min_extent.x <= neighbour.x <= self.max_extent.x) and
                (self.min_extent.y <= neighbour.y <= self.max_extent.y) and
                (self.min_extent.z <= neighbour.z <= self.max_extent.z) and
                (neighbour not in self.cubes)):
                moves.append(neighbour)
        return moves

    def exterior_surface_area(self):
        area = 0
        starting_point = self.min_extent
        explored = {starting_point}
        queue = deque([starting_point])
        while queue:
            steam_point = queue.popleft()
            area += self.sides_touching(steam_point)
            for neighbour in self.can_move_to(explore_from=steam_point):
                if neighbour not in explored:
                    explored.add(neighbour)
                    queue.append(neighbour)
        return area


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            x,y,z = [int(n) for n in ln.split(',')]
            yield Pos(x,y,z)

#--------------------- tests -------------------------#

def test_2_touching_cubes():
    scan = Scan([Pos(1,1,1), Pos(2,1,1)])
    assert scan.surface_area() == 10

def test_fetch_data():
    data = fetch_data('sample_data/day18.txt')
    assert next(data) == (2,2,2)

def test_example_problem():
    data = fetch_data('sample_data/day18.txt')
    scan = Scan(data)
    assert scan.surface_area() == 64

def test_exterior_surface_2_cubes():
    scan = Scan([Pos(1,1,1), Pos(2,1,1)])
    assert scan.exterior_surface_area() == 10

def test_exterior_surface_example_problem():
    data = fetch_data('sample_data/day18.txt')
    scan = Scan(data)
    assert scan.exterior_surface_area() == 58


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day18.txt')
    scan = Scan(data)
    print(scan.exterior_surface_area())
