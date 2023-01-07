
def fetch_data(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return [ln.rstrip() for ln in lines[:-2]], lines[-1].rstrip()

def neighbours(x,y):
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)


def create_board_map(maplines):
    board = {}
    for x, ln in enumerate(maplines):
        first = last = None
        for y, char in enumerate(ln.rstrip()):
            if char == ' ':
                continue
            elif char == '.':
                board[(x,y)] = set()
                for neighbour in neighbours(x,y):
                    if neighbour in board and board[neighbour] != 'wall':
                        board[(x,y)].add(neighbour)
                        board[neighbour].add((x,y))
            elif char == '#':
                board[(x,y)] = 'wall'

            if first is None:
                first = last = (x,y)
            elif y > last[1]:
                last = (x,y)
            
        # Check for wraparound
        if board[first] != 'wall' and board[last] != 'wall':
            board[first].add(last)
            board[last].add(first)

    return board




#--------------------- tests -------------------------#

def test_basics():
    maplines, path = fetch_data('sample_data/day22.txt')
    assert len(maplines) == 12
    assert maplines[0] == '        ...#'
    assert path == '10R5L5R10L4R5L5'

def test_create_simple_map():
    maplines = [
        '..',
        '.#'
    ]
    board = create_board_map(maplines)
    assert len(board) == 4
    assert board[0,0] == {(0,1), (1,0)}
    assert board[0,1] == {(0,0)}
    assert board[1,0] == {(0,0)}
    assert board[1,1] == 'wall'

def test_map_with_wraparound():
    maplines = [
        ' ....',
        '  ..#',
        ' .'
    ]
    board = create_board_map(maplines)
    assert len(board) == 8
    assert board[0,1] == {(0,2), (0,4), (2,1)}
    assert board[0,2] == {(0,1), (0,3), (1,2)}
    assert board[1,2] == {(0,2), (1,3)} # Wall bocks wraparound
    assert board[2,1] == {(0,1)}

    



#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day22.txt')
    print('Hello, World!')
