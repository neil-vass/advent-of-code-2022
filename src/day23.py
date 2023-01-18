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


    def play(self, rounds):
        first_direction = 0
        for _ in range(rounds):
            # Propose moves
            proposals = [(elf, self.propose_move(elf, first_direction)) for elf in self.elves]

            # Move
            destinations = list(zip(*proposals))[1]
            new_positions = []
            for src, dest in proposals:
                if destinations.count(dest) == 1:
                    new_positions.append(dest)
                else:
                    new_positions.append(src)
            self.elves = new_positions

            # Next time, consider from a new direction
            first_direction = (first_direction + 1) % len(Field.direction_order)


#--------------------- tests -------------------------#

def test_fetch_elves():
    elves = fetch_data('sample_data/day23-small.txt')
    assert len(elves) == 5
    assert elves[0] == (1,2)

def test_play_round():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play(rounds=1)
    assert set(field.elves) == {(0,2), (0,3), (2,2), (3,3), (4,2)}

def test_play_2_rounds_considers_new_direction():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play(rounds=2)
    assert set(field.elves) == {(1,2), (1,3), (2,1), (3,4), (5,2)}

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day23.txt')
    print('Hello, World!')
