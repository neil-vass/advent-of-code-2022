
class Scan:
    def __init__(self, cubes):
        self.cubes = {c: 6 for c in cubes}

        for x,y,z in self.cubes.keys():
            touching = 0
            if (x-1,y,z) in self.cubes:
                touching += 1
            if (x+1,y,z) in self.cubes:
                touching += 1
            if (x,y-1,z) in self.cubes:
                touching += 1
            if (x,y+1,z) in self.cubes:
                touching += 1
            if (x,y,z-1) in self.cubes:
                touching += 1
            if (x,y,z+1) in self.cubes:
                touching += 1
            self.cubes[(x,y,z)] -= touching
    
    def surface_area(self):
        return sum(self.cubes.values())

    def exterior_surface_area(self):
        pass

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            x,y,z = [int(n) for n in ln.split(',')]
            yield (x,y,z)

#--------------------- tests -------------------------#

def test_2_touching_cubes():
    scan = Scan([(1,1,1), (2,1,1)])
    assert scan.cubes == {(1,1,1): 5, (2,1,1): 5}
    assert scan.surface_area() == 10

def test_fetch_data():
    data = fetch_data('sample_data/day18.txt')
    assert next(data) == (2,2,2)

def test_example_problem():
    data = fetch_data('sample_data/day18.txt')
    scan = Scan(data)
    assert scan.surface_area() == 64

def test_exterior_surface():
    data = fetch_data('sample_data/day18.txt')
    scan = Scan(data)
    assert scan.exterior_surface_area() == 58


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day18.txt')
    scan = Scan(data)
    print(scan.surface_area())
