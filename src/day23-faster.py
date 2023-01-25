import cProfile
from collections import Counter

def fetch_data(path):
    with open(path, 'r') as f:
        elf_positions = []
        for x, ln in enumerate(f):
            for y, char in enumerate(ln):
                if char == '#':
                    elf_positions.append((x,y))
    return elf_positions

class Elf: 
    direction_order = 'NSWE'

    direction_checks = {
        'N': {'N', 'NE', 'NW'},
        'S': {'S', 'SE', 'SW'},
        'W': {'W', 'NW', 'SW'},
        'E': {'E', 'NE', 'SE'}
    }
    
    def __init__(self, pos):
        self.set_position(*pos)
        self.neighbours = set()
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.adjacent_positions = {
            'N': (x-1, y),
            'NE': (x-1, y+1),
            'E': (x, y+1),
            'SE': (x+1, y+1),
            'S': (x+1, y),
            'SW': (x+1, y-1),
            'W': (x, y-1),
            'NW': (x-1, y-1)
        }
        self.adjacent_directions = {v:k for k,v in self.adjacent_positions.items()}

    def pos(self):
        return (self.x, self.y)

    def add_neighbour(self, elf):
        dir = self.adjacent_directions[elf.pos()]
        self.neighbours.add(dir)

    def remove_neighbour(self, elf):
        dir = self.adjacent_directions[elf.pos()]
        self.neighbours.remove(dir)

    def propose_move(self, direction_idx):
        if len(self.neighbours):
            for _ in range(len(Elf.direction_order)):
                dir = Elf.direction_order[direction_idx]
                if self.neighbours.isdisjoint(Elf.direction_checks[dir]):
                    return self.adjacent_positions[dir]
                direction_idx = (direction_idx + 1) % len(Elf.direction_order)


class Field:
    def __init__(self, elf_positions):
        self.elves = {pos: Elf(pos) for pos in elf_positions}
        self.elves_with_neighbours = set()
        for elf in self.elves.values():
            for adj in elf.adjacent_positions.values():
                adjacent_elf = self.elves.get(adj) 
                if adjacent_elf:
                    elf.add_neighbour(adjacent_elf)
                    self.elves_with_neighbours.add(elf)
              

    def play(self, max_rounds=None):
        rounds = 0
        first_direction = 0
        while True:
            rounds += 1

            proposals = [(elf, elf.propose_move(first_direction)) for elf in self.elves_with_neighbours]
            elves_proposing = Counter(dest for elf, dest in proposals)
            moves = [(elf, dest) for elf, dest in proposals if dest is not None and elves_proposing[dest] == 1]

            if not moves:
                break
            
            for elf, dest in moves:
                # Delete this elf and re-add it in the right position
                for dir in elf.neighbours:
                    neighbour_elf = self.elves[elf.adjacent_positions[dir]]
                    neighbour_elf.remove_neighbour(elf)
                    if not neighbour_elf.neighbours:
                        self.elves_with_neighbours.discard(neighbour_elf)
                del self.elves[elf.pos()]
                self.elves_with_neighbours.discard(elf)
                self.elves[dest] = Elf(dest)
            
            # Set neighbours for the moved elves!
            for _, dest in moves:
                moved_elf = self.elves[dest]
                for adj in moved_elf.adjacent_positions.values():
                    adjacent_elf = self.elves.get(adj) 
                    if adjacent_elf:
                        moved_elf.add_neighbour(adjacent_elf)
                        adjacent_elf.add_neighbour(moved_elf)
                        self.elves_with_neighbours.add(moved_elf) 
                        self.elves_with_neighbours.add(adjacent_elf)

            first_direction = (first_direction + 1) % len(Elf.direction_order)
            
            if rounds == max_rounds:
                break
        return rounds

    def empty_ground(self):
        x, y = zip(*self.elves.keys())
        area = (max(x) - min(x) + 1) * (max(y) - min(y) + 1)
        return area - len(self.elves)

# max(x)
# 8
# min(x)
# -2
# max(y)
# 9
# min(y)
# -2

#[(1, 0), (-1, 4), (7, 1), (7, 4), (2, 8), (4, -2), (3, 0), (6, -1), (0, 7), (4, 7), (6, 7), (0, 2), (5, 3), (5, 5), (2, 6), (3, 6), (6, 2), (4, 4), (4, 3), (4, 2), (1, 4), (2, 4)]
#[(-2, 4), (0, 1), (1, 3), (2, 6), (-1, 8), (0, -1), (0, 4), (2, 9), (2, 0), (3, 6), (5, 8), (3, -2), (4, 2), (4, 3), (3, 5), (5, -1), (6, 1), (6, 3), (6, 6), (8, 7), (8, 1), (8, 4)]
#--------------------- tests -------------------------#

def test_fetch_elves():
    elf_positions = fetch_data('sample_data/day23-small.txt')
    assert len(elf_positions) == 5
    assert elf_positions[0] == (1,2)

def test_play_round():
    elf_positions = fetch_data('sample_data/day23-small.txt')
    field = Field(elf_positions)
    field.play(max_rounds=1)
    assert field.elves.keys() == {(0,2), (0,3), (2,2), (3,3), (4,2)}

def test_play_2_rounds_considers_new_direction():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play(max_rounds=2)
    assert field.elves.keys() == {(1,2), (1,3), (2,1), (3,4), (5,2)}

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
    rounds = field.play()
    print(rounds)

if __name__ == "__main__":
    cProfile.run('play()', sort='cumulative')

