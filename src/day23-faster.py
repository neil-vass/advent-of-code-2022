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

    def pos(self):
        return (self.x, self.y)

    def add_neighbour(self, elf):
        dir = next(k for k,v in self.adjacent_positions.items() if v == elf.pos())
        self.neighbours.add(dir)

    def remove_neighbour(self, elf):
        dir = next(k for k,v in self.adjacent_positions.items() if v == elf.pos())
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
                # Delete this elf
                for dir in elf.neighbours:
                    neighbour_pos = elf.adjacent_positions[dir]
                    self.elves[neighbour_pos].remove_neighbour(elf)
                del self.elves[elf.pos()]
                self.elves_with_neighbours.remove(elf)
                
                # New elf in right position
                # WAIT
                # We need to move them all _first_ then update neighbours
                new_elf = Elf(dest)
                for adj in new_elf.adjacent_positions:
                    adjacent_elf = self.elves.get(adj) 
                    if adjacent_elf:
                        new_elf.add_neighbour(adjacent_elf)
                        adjacent_elf.add_neighbour(new_elf)
                        self.elves_with_neighbours.add(new_elf) 
                    self.elves[dest] = new_elf

            first_direction = (first_direction + 1) % len(Elf.direction_order)
            
            if rounds == max_rounds:
                break
        return rounds


    def empty_ground(self):
        x, y = zip(*self.elves)
        area = (max(x) - min(x) + 1) * (max(y) - min(y) + 1)
        return area - len(self.elves)


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
    rounds = field.play(30)
    print(rounds)

if __name__ == "__main__":
    cProfile.run('play()', sort='cumulative')


# Runs in 18.75 minutes, can we improve?
# 22169768 function calls in 1125.186 seconds

#    Ordered by: cumulative time

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000 1125.186 1125.186 {built-in method builtins.exec}
#         1    0.000    0.000 1125.186 1125.186 <string>:1(<module>)
#         1    0.000    0.000 1125.186 1125.186 day23.py:119(play)
#         1    1.602    1.602 1125.183 1125.183 day23.py:53(play)
#      1003    1.305    0.001 1000.396    0.997 day23.py:58(<listcomp>)
#   2595764    5.451    0.000  999.091    0.000 day23.py:28(propose_move)
#   2595764  992.575    0.000  992.575    0.000 day23.py:41(<setcomp>)
#   2595764  123.019    0.000  123.019    0.000 {method 'count' of 'tuple' objects}
    

# For stopping after 30 rounds: 28s
#          1038891 function calls in 28.635 seconds

#    Ordered by: cumulative time

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000   28.635   28.635 {built-in method builtins.exec}
#         1    0.000    0.000   28.635   28.635 <string>:1(<module>)
#         1    0.000    0.000   28.635   28.635 day23-faster.py:120(play)
#         1    0.052    0.052   28.631   28.631 day23-faster.py:54(play)
#        30    0.046    0.002   24.907    0.830 day23-faster.py:59(<listcomp>)
#     77640    0.272    0.000   24.861    0.000 day23-faster.py:29(propose_move)
#     77640   24.524    0.000   24.524    0.000 day23-faster.py:42(<setcomp>)
#     77640    3.667    0.000    3.667    0.000 {method 'count' of 'tuple' objects}

def test_this():
    assert 1 == 1
