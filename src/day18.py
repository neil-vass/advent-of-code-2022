from collections import namedtuple
from collections import deque

Pos = namedtuple("Pos", "x y z")


class Scan:
    def __init__(self, cubes):
        self.cubes = set(cubes)
        
         # Find extents
        all_x, all_y, all_z = zip(*self.cubes)
        self.max_x = max(all_x)
        self.min_x = min(all_x)
        self.max_y = max(all_y)
        self.min_y = min(all_y)
        self.max_z = max(all_z)
        self.min_z = min(all_z)
    
    def surface_area(self):
        surfaces = [6 - self.sides_touching(c) for c in self.cubes]
        return sum(surfaces)

    def sides_touching(self, target_cube):
        touching = [n for n in Scan.get_neighbours(target_cube) if n in self.cubes]
        return len(touching)

    def get_neighbours(point):
        x,y,z = point
        return [(x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)]

    def can_move_to(self, explore_from):
        moves = []
        for neighbour in Scan.get_neighbours(explore_from):
            if ((self.min_x -1 <= neighbour[0] <= self.max_x +1) and
                (self.min_y -1 <= neighbour[1] <= self.max_y +1) and
                (self.min_z -1 <= neighbour[2] <= self.max_z +1) and
                (neighbour not in self.cubes)):
                moves.append(neighbour)
        return moves

    def exterior_surface_area(self):
        # Steam blast across the outside.
        # Start with a cube of steam touching one of the outside edges of one cube.
        # Mark any touched-with-steam edges as visited.
        # Steam expands in all directions that don't have cubes in ...
            # Max expansion is 1 extra past the extreme x/y/z vals in the scan, 
            # no need to go further than that.
            # Mark any touched-with-steam edges as visited.

       

        # Note visited steam cubes
        area = 0
        starting_point = (self.min_x-1, self.min_y-1, self.min_z-1)
        explored = {starting_point}
        queue = deque([starting_point])
        while queue:
            v = queue.popleft()
            area += self.sides_touching(v)
            for neighbour in self.can_move_to(explore_from=v):
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
