
class Cave:
    def __init__(self):
        self._content = dict()
        self._furthest_sand_can_fall = 0

    def add_rocks(self, from_x, from_y, to_x, to_y):
        start_x = min(from_x, to_x)
        end_x = max(from_x+1, to_x+1)
        for x in range(start_x, end_x):
            self._content[(x, from_y)] = 'rock'

        start_y = min(from_y, to_y)
        end_y = max(from_y+1, to_y+1)
        for y in range(start_y, end_y):
            self._content[(from_x, y)] = 'rock'

        self._furthest_sand_can_fall = max(self._furthest_sand_can_fall, end_y)


    def add_sand(self, x, y):
        while y < self._furthest_sand_can_fall:
            if (x, y+1) not in self._content:
                x, y = x, y+1
            elif (x-1, y+1) not in self._content:
                x, y = x-1, y+1
            elif (x+1, y+1) not in self._content:
                x, y = x+1, y+1
            else:
                break
        self._content[(x, y)] = 'sand'
        return x, y

    def add_sand_until_flowing(self):
        units = 1
        while self.add_sand(500, 0) != (500, 0):
            units += 1
        return units

    def __call__(self, x, y):
        return self._content.get((x,y), 'air')


def fetch_data(path):
    cave = Cave()
    with open(path, 'r') as f:
        for ln in f:
            from_x = from_y = None
            for token in ln.split():
                if token == '->':
                    continue
                to_x, to_y = [int(n) for n in token.split(',')]
                if from_x is not None:
                    cave.add_rocks(from_x, from_y, to_x, to_y)
                from_x, from_y = to_x, to_y
    return cave
    

#--------------------- tests -------------------------#

def test_cave_creation():
    cave = Cave()
    cave.add_rocks(498, 4, 498, 6)
    assert cave(494,0) == 'air'
    assert cave(498,4) == 'rock'

def test_fetch_data():
    cave = fetch_data('sample_data/day14.txt')
    assert cave(494,0) == 'air'
    assert cave(498,4) == 'rock'
    assert cave(495, 6) == 'air'
    assert cave(496, 6) == 'rock'

def test_add_sand():
    cave = fetch_data('sample_data/day14.txt')
    assert cave(500, 8) == 'air'
    assert cave.add_sand(500, 0) is not None
    assert cave(500, 8) == 'sand'
    assert cave.add_sand(500, 0) is not None
    assert cave(499, 8) == 'sand'

def test_add_sand_until_flowing():
    cave = fetch_data('sample_data/day14.txt')
    assert cave.add_sand_until_flowing() == 93


#-----------------------------------------------------#

if __name__ == "__main__":
    cave = fetch_data('data/day14.txt')
    print(cave.add_sand_until_flowing())
