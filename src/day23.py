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

    def propose_move(self, elf):
        x,y = elf
        directions = {
            'N': (x-1, y),
            'NE': (x-1, y+1),
            'E': (x, y+1),
            'SE': (x+1, y+1),
            'S': (x+1, y),
            'SW': (x+1, y-1),
            'W': (x, y-1),
            'NW': (x-1, y-1)
        }

        neighbours = {k for k,v in directions.items() if v in self.elves}

        if len(neighbours): 
            if {'N', 'NE', 'NW'}.isdisjoint(neighbours):
                return directions['N']
            if {'S', 'SE', 'SW'}.isdisjoint(neighbours):
                return directions['S']
            if {'W', 'NW', 'SW'}.isdisjoint(neighbours):
                return directions['W']
            if {'E', 'NE', 'SE'}.isdisjoint(neighbours):
                return directions['E']
        return elf


    def play_round(self):
        # Propose moves
        proposals = [(elf, self.propose_move(elf)) for elf in self.elves]

        # Move
        destinations = list(zip(*proposals))[1]
        new_positions = []
        for src, dest in proposals:
            if destinations.count(dest) == 1:
                new_positions.append(dest)
            else:
                new_positions.append(src)
        self.elves = new_positions


#--------------------- tests -------------------------#

def test_fetch_elves():
    elves = fetch_data('sample_data/day23-small.txt')
    assert len(elves) == 5
    assert elves[0] == (1,2)

def test_play_round():
    elves = fetch_data('sample_data/day23-small.txt')
    field = Field(elves)
    field.play_round()
    assert set(field.elves) == {(0,2), (0,3), (2,2), (3,3), (4,2)}

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day23.txt')
    print('Hello, World!')
