import cProfile


def fetch_data(path):
    with open(path, 'r') as f:
        elves = []
        for x, ln in enumerate(f):
            for y, char in enumerate(ln):
                if char == '#':
                    elves.append((x,y))
    return elves


class Field:
    def __init__(self, elves):
        self.elves = elves

    direction_order = 'NSWE'

    direction_checks = {
        'N': {'N', 'NE', 'NW'},
        'S': {'S', 'SE', 'SW'},
        'W': {'W', 'NW', 'SW'},
        'E': {'E', 'NE', 'SE'}
    }
    

    def propose_move(self, elf, direction_idx):
        x,y = elf
        adjacent_positions = {
            'N': (x-1, y),
            'NE': (x-1, y+1),
            'E': (x, y+1),
            'SE': (x+1, y+1),
            'S': (x+1, y),
            'SW': (x+1, y-1),
            'W': (x, y-1),
            'NW': (x-1, y-1)
        }

        neighbours = {k for k,v in adjacent_positions.items() if v in self.elves}

        if len(neighbours): 
            for _ in range(len(Field.direction_order)):
                dir = Field.direction_order[direction_idx]
                if neighbours.isdisjoint(Field.direction_checks[dir]):
                    return adjacent_positions[dir]

                direction_idx = (direction_idx + 1) % len(Field.direction_order)
        return elf


    def play(self, max_rounds=None):
        rounds = 0
        first_direction = 0
        while True:
            rounds += 1
            proposals = [(elf, self.propose_move(elf, first_direction)) for elf in self.elves]

            destinations = list(zip(*proposals))[1]
            new_positions = []
            for src, dest in proposals:
                if destinations.count(dest) == 1:
                    new_positions.append(dest)
                else:
                    new_positions.append(src)

            if set(self.elves) == set(new_positions):
                break
            
            self.elves = new_positions
            first_direction = (first_direction + 1) % len(Field.direction_order)
            
            if rounds == max_rounds:
                break
        return rounds
    

    def empty_ground(self):
        x, y = zip(*self.elves)
        area = (max(x) - min(x) + 1) * (max(y) - min(y) + 1)
        return area - len(self.elves)


#--------------------- tests -------------------------#

def test_fetch_elves():
    elves = fetch_data('sample_data/day23-small.txt')
    assert len(elves) == 5
    assert elves[0] == (1,2)

def test_play_round():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play(max_rounds=1)
    assert set(field.elves) == {(0,2), (0,3), (2,2), (3,3), (4,2)}

def test_play_2_rounds_considers_new_direction():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play(max_rounds=2)
    assert set(field.elves) == {(1,2), (1,3), (2,1), (3,4), (5,2)}

def test_play_10_rounds_with_large_example():
    elves = fetch_data('sample_data/day23-large.txt')
    field = Field(elves)
    field.play(max_rounds=10)
    assert len(field.elves) == 22
    assert field.empty_ground() == 110

def test_play_to_end_with_large_example():
    elves = fetch_data('sample_data/day23-large.txt')
    field = Field(elves)
    rounds = field.play()
    assert rounds == 20

#-----------------------------------------------------#

def play():
    elves = fetch_data('data/day23.txt')
    field = Field(elves)
    rounds = field.play(max_rounds=30)
    print(rounds)

if __name__ == "__main__":
    cProfile.run('play()', sort='cumulative')
    
