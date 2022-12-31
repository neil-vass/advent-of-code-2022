
import numpy as np

class Rock:
    horizontal = np.ones((1,4), int)

    plus = np.array([
        [0,1,0],
        [1,1,1],
        [0,1,0]], int)

    L = np.array([
        [0,0,1],
        [0,0,1],
        [1,1,1]], int)

    vertical = np.ones((4,1), int)

    box = np.ones((2,2), int)

    def cycle():
        while True:
            yield Rock.horizontal
            yield Rock.plus
            yield Rock.L
            yield Rock.vertical
            yield Rock.box


movements = { 'v': (+1, 0), '<': (0, -1), '>': (0, +1) }

class Chamber:
    width = 7
    def __init__(self, jets):
        self.content = np.zeros((1000, Chamber.width), int)
        self.jets = jets

    def tower_height(self):
        height = self.content.shape[0]
        for i in range(height):
            if self.content[i].any():
                break
            else:
                height -= 1
        return height

    def _can_move(self, rock, rock_pos_x, rock_pos_y, direction):
        rock_height, rock_width = rock.shape
        if direction == 'v':
            if rock_pos_x + rock_height == self.content.shape[0]:
                return False
        elif direction == '<':
            if rock_pos_y == 0:
                return False
        elif direction == '>':
            if rock_pos_y + rock_width == Chamber.width:
                return False

        move_x, move_y = movements[direction]
        for x in reversed(range(rock_height)):
            for y in range(rock_width):
                moving_to_x = rock_pos_x + x + move_x
                moving_to_y = rock_pos_y + y + move_y
                if rock[x,y] and self.content[moving_to_x, moving_to_y]:
                    return False
        return True
        

    def drop(self, rock):
        # Rock appears, add rows to chamber as needed (3 blanks above tower height, plus space for rock)
        rock_height, rock_width = rock.shape

        rock_from_floor = self.tower_height() + 3 + rock_height
        if rock_from_floor > self.content.shape[0]:
            self.content = np.vstack([np.zeros((1000, Chamber.width), int), self.content])

        rock_pos_x = self.content.shape[0] - rock_from_floor
        rock_pos_y = 2

        # while not at rest:
        while True:
            # Jet tries to move rock (if we bang into something, we can't)
            jet_direction = next(self.jets)
            if self._can_move(rock, rock_pos_x, rock_pos_y, jet_direction):
                rock_pos_y = rock_pos_y-1 if jet_direction == '<' else rock_pos_y+1

            # Rock tries to drop (if we bang into something, exit loop)
            if self._can_move(rock, rock_pos_x, rock_pos_y, 'v'):
                rock_pos_x +=1
            else:
                # If we can't drop: add 1's to the chamber
                self.content[rock_pos_x:rock_pos_x+rock_height, rock_pos_y:rock_pos_y+rock_width] = rock
                # Then break.
                break



def fetch_jets(path):
    with open(path, 'r') as f:
        ln = f.readline().rstrip()
    while True:
        for c in ln:
            yield c

#--------------------- tests -------------------------#

def test_fetch_jets():
    data = fetch_jets('sample_data/day17.txt')
    assert next(data) == '>'
    assert next(data) == '>'
    assert next(data) == '>'
    assert next(data) == '<'
    for _ in range(40):
        next(data)
    assert next(data) == '<'
    

def test_drop_rock():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    chamber.drop(Rock.horizontal)
    assert chamber.tower_height() == 1
    assert np.array_equal(chamber.content[-4:], np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0]], int))

def test_drop_2_rocks():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    chamber.drop(Rock.horizontal)
    chamber.drop(Rock.plus)
    assert chamber.tower_height() == 4
    assert np.array_equal(chamber.content[-5:], np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0]], int))

def test_rock_cycle():
    cycle = Rock.cycle()
    assert np.array_equal(next(cycle), Rock.horizontal)
    assert np.array_equal(next(cycle), Rock.plus)
    assert np.array_equal(next(cycle), Rock.L)
    assert np.array_equal(next(cycle), Rock.vertical)
    assert np.array_equal(next(cycle), Rock.box)
    assert np.array_equal(next(cycle), Rock.horizontal)

def test_drop_rocks_with_cycle():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    rocks = Rock.cycle()
    for _ in range(3):
        chamber.drop(next(rocks))
    assert chamber.tower_height() == 6
    chamber.drop(next(rocks))
    assert chamber.tower_height() == 7
    chamber.drop(next(rocks))
    assert chamber.tower_height() == 9
    chamber.drop(next(rocks))
    assert chamber.tower_height() == 10
    chamber.drop(next(rocks))
    assert chamber.tower_height() == 13
    chamber.drop(next(rocks))
    assert np.array_equal(chamber.content[-14], [0,0,0,0,0,1,0])
    
    assert chamber.tower_height() == 15

    # assert np.array_equal(chamber.content[-15], [0,0,0,0,0,1,0])

def test_drop_2022_rocks():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    rocks = Rock.cycle()
    for _ in range(2022):
        chamber.drop(next(rocks))
    assert chamber.tower_height() == 3068
    

#-----------------------------------------------------#

if __name__ == "__main__":
    jets = fetch_jets('data/day17.txt')
    chamber = Chamber(jets)
    rocks = Rock.cycle()
    for _ in range(2022):
        chamber.drop(next(rocks))
    print(chamber.tower_height())
    # Gets 3120, that's too low.