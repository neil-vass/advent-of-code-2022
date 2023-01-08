
def fetch_data(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return [ln.rstrip() for ln in lines[:-2]], lines[-1].rstrip()

def neighbours(x,y):
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)

class Line:
    def __init__(self):
        self.start = None
        self.end = None
        self.walls = []

    def move_endward(self, current_pos, tiles):
        raise Exception('todo')

    def move_startward(self, current_pos, tiles):
        raise Exception('todo')


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

    def move_right(self, current_pos, tiles):
        pass

    def move_left(self, current_pos, tiles):
        pass

    def move_down(self, current_pos, tiles):
        pass

    def move_up(self, current_pos, tiles):
        pass



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
    assert board.move_right((1,1), 2) == (1,3) # Can step right
    assert board.move_right((2,1), 2) == (2,1) # Blocked by wall
    assert board.move_left((1,3), 1) == (1,2) 
    assert board.move_down((1,1), 1) == (2,1)
    assert board.move_down((1,2), 1) == (1,2) # Blocked by wall
    assert board.move_up((2,3), 1) == (1,3)
    

def test_map_with_wraparound():
    board = Board([
        ' ....',
        '  ..#',
        ' .'
    ])
    

    



#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day22.txt')
    print('Hello, World!')
