

class Chamber:
    def __init__(self, jets):
        self.tops = [0] * 7
        self.jets = jets
    
    def tower_height(self):
        return max(self.tops)

    def drop(self, rock):
        x, y = self.tower_height() + 3, 2

        stopped = False
        while not stopped:
            if next(self.jets) == '>':
                if y + len(rock) < len(self.tops):
                    y += 1
            else:
                if y > 0:
                    y -= 1

            for i in range(len(rock)):
                if self.tops[y+i] == (x+1) + rock[i][0]:
                    # stopped. Let's do sums
                    for j in range(len(rock)):
                        self.tops[y+j] += rock[j][1]
                    stopped = True
                    break
            x -= 1




def fetch_data(path):
    while True:
        with open(path, 'r') as f:
            for c in f.readline().rstrip():
                yield c

#--------------------- tests -------------------------#

def test_drop_rocks():
    jets = fetch_data('data/day17.txt')
    chamber = Chamber(jets)

    chamber.drop([(0,1), (0,1), (0,1), (0,1)])
    assert chamber.tower_height() == 1
    assert chamber.tops == [0, 0, 1, 1, 1, 1, 0]

    chamber.drop([(1,2), (0,3), (1,2)])
    #assert chamber.tower_height() == 4
    assert chamber.tops == [0, 0, 3, 4, 3, 1, 0]


def test_fetch_data():
    data = fetch_data('sample_data/day17.txt')
    assert next(data) == '>'

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day17.txt')
    print('Hello, World!')
