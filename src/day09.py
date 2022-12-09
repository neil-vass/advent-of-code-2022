
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 'U':
            return Pos(self.x+1, self.y)
        if direction == 'D':
            return Pos(self.x-1, self.y)
        if direction == 'L':
            return Pos(self.x, self.y-1)
        if direction == 'R':
            return Pos(self.x, self.y+1)

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            direction, distance = ln.rstrip().split()
            yield direction, int(distance)

def follow(head, tail):
    if abs(head.x - tail.x) > 1 or abs(head.y - tail.y) > 1:
        if head.x > tail.x:
            tail = tail.move('U')
        elif head.x < tail.x:
            tail = tail.move('D')

        if head.y > tail.y:
            tail = tail.move('R')
        elif head.y < tail.y:
            tail = tail.move('L')
    return tail


def track_visits(data):
    head = Pos(0,0)
    tail = Pos(0,0)
    visited = {(0,0)}

    for direction, distance in data:
        for _ in range(distance):
            head = head.move(direction)
            tail = follow(head, tail)
            visited.add((tail.x, tail.y))
    return visited

#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day09.txt')
    assert next(data) == ('R', 4)

def test_track_visits():
    data = fetch_data('sample_data/day09.txt')
    assert len(track_visits(data)) == 13

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day09.txt')
    print(len(track_visits(data)))
