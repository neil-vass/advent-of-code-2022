import re

def fetch_data(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return [ln.rstrip() for ln in lines[:-2]], lines[-1].rstrip()

class Line:
    def __init__(self):
        self.start = None
        self.end = None
        self.walls = []
    
    def move_endward(self, current_pos, tiles):     
        width = self.end - self.start + 1 
        if self.walls:
            wrapped_walls = self.walls + [(w + width) for w in self.walls]
            farthest_move = (next(w for w in wrapped_walls if w > current_pos) -1) - current_pos
            tiles = min(tiles, farthest_move)
        return ((current_pos - self.start + tiles) % width) + self.start


    def move_startward(self, current_pos, tiles):
        width = self.end - self.start + 1
        if self.walls:
            wrapped_walls = reversed([(w - width) for w in self.walls] + self.walls)
            farthest_move = current_pos - (next(w for w in wrapped_walls if w < current_pos) +1)
            tiles = min(tiles, farthest_move)
        return ((current_pos - self.start - tiles) % width) + self.start


class Board:
    def __init__(self, maplines):
        self.rows, self.cols = Board._create_map(maplines)

    def _create_map(maplines):
        rows = {}
        cols = {}
        for x, ln in enumerate(maplines, start=1):
            rows[x] = Line()
            for y, char in enumerate(ln.rstrip(), start=1):
                if y not in cols:
                    cols[y] = Line()
                if char == ' ':
                    continue
                if rows[x].start is None:
                    rows[x].start = rows[x].end = y
                if cols[y].start is None:
                    cols[y].start = cols[y].end = x

                rows[x].end = max(y, rows[x].end)
                cols[y].end = max(x, cols[y].end)
                
                if char == '#':
                    rows[x].walls.append(y)  
                    cols[y].walls.append(x)

        return rows, cols

    def move(self, current_pos, tiles, dir):
        x,y = current_pos
        if dir == '>':
            y = self.rows[x].move_endward(y, tiles)
        if dir == '<':
            y = self.rows[x].move_startward(y, tiles)
        if dir == 'v':
            x = self.cols[y].move_endward(x, tiles)
        if dir == '^':
            x = self.cols[y].move_startward(x, tiles)
        return (x,y)


    def follow_path(self, path):
        directions = '>v<^'
        current_pos = (1, self.rows[1].start)
        facing = '>'
        history = [(current_pos, facing)]
        for instruction in re.findall(r'(\d+|L|R)', path):
            if instruction.isdigit():
                current_pos = self.move(current_pos, int(instruction), facing)
            elif instruction == 'L':
                facing = directions[(directions.index(facing) - 1) % len(directions)]
            elif instruction == 'R':
                facing = directions[(directions.index(facing) + 1) % len(directions)]
            history.append((current_pos, facing))
        return current_pos, facing


def final_password(path):
    maplines, path = fetch_data(path)
    board = Board(maplines)
    ((row, col), facing) = board.follow_path(path)
    return 1000 * row + 4 * col + '>v<^'.index(facing)

#--------------------- tests -------------------------#

def test_basics():
    maplines, path = fetch_data('sample_data/day22.txt')
    assert len(maplines) == 12
    assert maplines[0] == '        ...#'
    assert path == '10R5L5R10L4R5L5'

def test_create_simple_map():
    board = Board([
        '..',
        '.#'])
    assert len(board.rows) == 2
    assert board.rows[1].start == 1
    assert board.rows[1].walls == []
    assert len(board.cols) == 2
    assert board.cols[2].start == 1
    assert board.cols[2].end == 2
    assert board.cols[2].walls == [2]

    
def test_move_within_board_limits():
    board = Board([
        '...',
        '.#.'])
    assert board.move((1,1), 2, '>') == (1,3) # Can step right
    assert board.move((2,1), 2, '>') == (2,1) # Blocked by wall
    assert board.move((1,3), 1, '<') == (1,2) 
    assert board.move((1,1), 1, 'v') == (2,1)
    assert board.move((1,2), 1, 'v') == (1,2) # Blocked by wall
    assert board.move((2,3), 1, '^') == (1,3)
    
def test_map_with_wraparound():
    board = Board([
        ' ....',
        '  ..#',
        '    .'
    ])
    assert board.move((1,2), 8, '>') == (1,2) # Move a multiple of width
    assert board.move((2,3), 1, 'v') == (1,3) # Pop out at top
    assert board.move((1,5), 5, 'v') == (1,5) # Blocked immediately

def test_hit_walls_after_wraparound():
    maplines, path = fetch_data('sample_data/day22.txt')
    board = Board(maplines)
    assert board.move((6,4), 5, 'v') == (8,4) # Wall at top blocks wraparound
    assert board.move((6,3), 5, '^') == (8,3) # Wrap off top, then wall below where you started blocks
    assert board.move((7,10), 20, '>') == (7,2) # Wrap and make sure we hit first wall
    assert board.move((7,2), 20, '<') == (7,9) # As above, other way


def test_follow_path():
    maplines, path = fetch_data('sample_data/day22.txt')
    board = Board(maplines)
    assert board.follow_path(path) == ((6,8), '>')

def test_final_password():
    assert final_password('sample_data/day22.txt') == 6032

#-----------------------------------------------------#

if __name__ == "__main__":
    print(final_password('data/day22.txt'))