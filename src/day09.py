
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

    def follow(self, leader):
        follower = self
        if abs(leader.x - follower.x) > 1 or abs(leader.y - follower.y) > 1:
            if leader.x > follower.x:
                follower = follower.move('U')
            elif leader.x < follower.x:
                follower = follower.move('D')

            if leader.y > follower.y:
                follower = follower.move('R')
            elif leader.y < follower.y:
                follower = follower.move('L')
        return follower


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            direction, distance = ln.rstrip().split()
            yield direction, int(distance)

def track_visits(data):
    head = tail = Pos(0,0)
    visited = {(0,0)}

    for direction, distance in data:
        for _ in range(distance):
            head = head.move(direction)
            tail = tail.follow(head)
            visited.add((tail.x, tail.y))
    return visited


def track_visits_part_2(data, knot_count):
    knots = [Pos(0,0)] * knot_count
    visited = {(0,0)}

    for direction, distance in data:
        for _ in range(distance):
            for idx, knot in enumerate(knots):
                if idx == 0:
                    new_position = knot.move(direction)
                else:
                    new_position = knot.follow(knots[idx-1])
                knots[idx] = new_position
            visited.add((knots[-1].x, knots[-1].y))
    return visited

#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day09.txt')
    assert next(data) == ('R', 4)

def test_track_visits():
    data = fetch_data('sample_data/day09.txt')
    assert len(track_visits(data)) == 13

def test_track_visits_part_2_original_data():
    data = fetch_data('sample_data/day09.txt')
    assert len(track_visits_part_2(data, knot_count=2)) == 13
    assert len(track_visits_part_2(data, knot_count=10)) == 1

def test_track_visits_part_2_larger_example():
    data = fetch_data('sample_data/day09-part2.txt')
    assert len(track_visits_part_2(data, knot_count=10)) == 36

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day09.txt')
    print(len(track_visits_part_2(data, knot_count=10)))
