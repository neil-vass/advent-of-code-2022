
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
            yield ('-', Rock.horizontal)
            yield ('+', Rock.plus)
            yield ('L', Rock.L)
            yield ('|', Rock.vertical)
            yield ('o', Rock.box)


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
        

    def drop(self, rock_info):
        # Rock appears, add rows to chamber as needed (3 blanks above tower height, plus space for rock)
        rock_name, rock = rock_info
        rock_height, rock_width = rock.shape

        rock_from_floor = self.tower_height() + 3 + rock_height
        if rock_from_floor > self.content.shape[0]:
            self.content = np.vstack([np.zeros((1000, Chamber.width), int), self.content])

        rock_pos_x = self.content.shape[0] - rock_from_floor
        rock_pos_y = 2

        # while not at rest:
        while True:
            # Jet tries to move rock (if we bang into something, we can't)
            jet_idx, jet_direction = next(self.jets)
            if self._can_move(rock, rock_pos_x, rock_pos_y, jet_direction):
                rock_pos_y = rock_pos_y-1 if jet_direction == '<' else rock_pos_y+1

            # Rock tries to drop (if we bang into something, exit loop and return)
            if self._can_move(rock, rock_pos_x, rock_pos_y, 'v'):
                rock_pos_x +=1
            else:
                self.content[rock_pos_x:rock_pos_x+rock_height, rock_pos_y:rock_pos_y+rock_width] += rock
                break

        return f'{rock_name}, {jet_idx}, {self.tower_height()}\n'

def fetch_jets(path):
    with open(path, 'r') as f:
        ln = f.readline().rstrip()
    while True:
        for jet in enumerate(ln):
            yield jet

#--------------------- tests -------------------------#

def test_fetch_jets():
    data = fetch_jets('sample_data/day17.txt')
    assert next(data) == (0, '>')
    assert next(data) == (1, '>')
    assert next(data) == (2, '>')
    assert next(data) == (3, '<')
    for _ in range(40):
        next(data)
    assert next(data) == (4, '<')
    

def test_drop_rock():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    chamber.drop(('-', Rock.horizontal))
    assert chamber.tower_height() == 1
    assert np.array_equal(chamber.content[-4:], np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0]], int))

def test_drop_2_rocks():
    jets = fetch_jets('sample_data/day17.txt')
    chamber = Chamber(jets)
    chamber.drop(('-', Rock.horizontal))
    chamber.drop(('+', Rock.plus))
    assert chamber.tower_height() == 4
    assert np.array_equal(chamber.content[-5:], np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0]], int))

def test_rock_cycle():
    cycle = Rock.cycle()
    assert np.array_equal(next(cycle)[1], Rock.horizontal)
    assert np.array_equal(next(cycle)[1], Rock.plus)
    assert np.array_equal(next(cycle)[1], Rock.L)
    assert np.array_equal(next(cycle)[1], Rock.vertical)
    assert np.array_equal(next(cycle)[1], Rock.box)
    assert np.array_equal(next(cycle)[1], Rock.horizontal)

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
    patterns = []
    for _ in range(10000):
        state = chamber.drop(next(rocks))
        patterns.append(state)
    with open('patterns.txt', 'w') as f:
        f.writelines(patterns)    
    print(chamber.tower_height())

    # Having a look in Excel :) 

    #---------------------------------------------------#
    # For sample data: 
    # Pattern starts at 40th rock
    # Pattern length is 35 rocks
    # Pattern adds 53 to tower hieght
    # We get to 66 before pattern starts

    # So for 2022 rocks, we'd get:
    ## 39 rocks, 66 height
    ## 56 full patterns, 53 height each
    ## The first 23 rocks of a pattern, which is 34 height
    ## Total: 3068 .... Great, that's right!

    # And for 1 trillion rocks, we'd get:
    # 1514285714288 ... Amazing! 

    #---------------------------------------------------#
    # For real data:
    # I see (box, 2966) at rock 510, 2255, 4000. So repeats every 1745.
    # Before the pattern starts, the first 71 rocks gets tower of 104
    # Pattern length is 1745. Looks like:
    #   first pattern adds 2737, and later ones add 2738 to tower height

    # So for 2022 rocks (right answer is 3135), we get that right!
    # And for 1 trillion ... Gold star!



    