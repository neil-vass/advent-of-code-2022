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
        farthest_move = next((w-1 for w in self.walls if w > current_pos), self.end) - current_pos
        dist = min(tiles, farthest_move) 
        new_pos = current_pos + dist
        remaining_move = (tiles - dist) if new_pos == self.end else 0
        return new_pos, remaining_move


    def move_startward(self, current_pos, tiles):
        farthest_move = current_pos - next(reversed(w+1 for w in self.walls if w < current_pos), self.start)
        dist = min(tiles, farthest_move)
        new_pos = current_pos - dist
        remaining_move = (tiles - dist) if new_pos == self.start else 0
        return new_pos, remaining_move


# Class Cube, very like the Board
# Rows and cols work the same, EXCEPT we need new wrapping rules
# For wrap past the end: 
#    - which line do you pop out onto? 
#    - And which position (start or end)
#    - Interesting: the lines don't care about facing, but we'll need to track that.
#    - (e.g. sample_data: if you leave a row in 4 facing >, you appear in a col in 6 facing v)
# Special consideration: if there's a wall in the line you're wrapping onto ... you don't wrap.
# (so need to look ahead just to the start or end).
# WOW there's a lot.
# Actually! Instead of trying to wrap, let's just move as far as we can on each line,
# Then back to Cube to consider next steps. 
class Cube:
    def __init__(self, maplines, folding='sample'):
        self.rows, self.cols = Cube._create_map(maplines)
        self._create_wrapping_rules(folding)

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

    # Cols
    # 1^ to 2v, map reversed
    # 2^ to 1v, map reversed
    # 2v to 5^, map reversed
    # 3^ to 1> (Row!)
    # 3v to 5> (Row!), map reversed
    # 5v to 2^, map reversed
    # 6^ to 4< (Row!), map reversed
    # 6v to 2> (Row!), map reversed

    # Rows
    # 1< to 3v (Col!)
    # 1> to 6<, map reversed 
    # 2< to 6^ (Col!), map reversed
    # 4> to 6v (Col!), map reversed
    # 5< to 3^ (Col!), map reversed
    # 6> to 1<, map reversed
    def _create_wrapping_rules(self, folding):
        if folding == 'sample':
            face_size = 4
            
            for row_idx in range(1, face_size+1):
                offset = 0
                # 1< to 3v (Col!)
                wrap_idx = face_size + row_idx
                self.rows[offset+row_idx].startward_wrap = (self.cols[wrap_idx], 'v')
                # 1> to 6<, map reversed 
                wrap_idx = 2 * face_size + (1 + face_size - row_idx)
                self.rows[offset+row_idx].endward_wrap = (self.rows[wrap_idx], '<')
                
                offset += face_size
                # 2< to 6^ (Col!), map reversed
                wrap_idx = 3 * face_size + (1 + face_size - row_idx)
                self.rows[offset+row_idx].startward_wrap = (self.cols[wrap_idx], '^')
                # 4> to 6v (Col!), map reversed
                wrap_idx = 3 * face_size + (1 + face_size - row_idx)
                self.rows[offset+row_idx].endward_wrap = (self.cols[wrap_idx], 'v')

                offset += face_size
                # 5< to 3^ (Col!), map reversed
                wrap_idx = 3 * face_size + (1 + face_size - row_idx)
                self.rows[offset+row_idx].startward_wrap = (self.cols[wrap_idx], '^')
                # 6> to 1<, map reversed
                wrap_idx = (1 + face_size - row_idx)
                self.rows[offset+row_idx].endward_wrap = (self.rows[wrap_idx], '<')
            
            for col_idx in range(1, face_size+1):
                offset = 0
                # 2^ to 1v, map reversed
                wrap_idx = 2 * face_size + (1 + face_size - col_idx)
                self.cols[offset+col_idx].startward_wrap = (self.cols[wrap_idx], 'v')
                # 2v to 5^, map reversed
                wrap_idx = 2 * face_size + (1 + face_size - col_idx)
                self.cols[offset+col_idx].endward_wrap = (self.cols[wrap_idx], '^')

                offset += face_size
                # 3^ to 1> (Row!)
                wrap_idx = col_idx
                self.cols[offset+col_idx].startward_wrap = (self.rows[wrap_idx], '>')
                # 3v to 5> (Row!), map reversed
                wrap_idx = 2 * face_size + (1 + face_size - col_idx)
                self.cols[offset+col_idx].endward_wrap = (self.rows[wrap_idx], '>')

                offset += face_size
                # 1^ to 2v, map reversed
                wrap_idx = (1 + face_size - col_idx)
                self.cols[offset+col_idx].startward_wrap = (self.cols[wrap_idx], 'v')
                # 5v to 2^, map reversed
                wrap_idx = (1 + face_size - col_idx)
                self.cols[offset+col_idx].endward_wrap = (self.cols[wrap_idx], '^')

                offset += face_size
                # 6^ to 4< (Row!), map reversed
                wrap_idx = face_size + (1 + face_size - col_idx)
                self.cols[offset+col_idx].endward_wrap = (self.rows[wrap_idx], '<')
                # 6v to 2> (Row!), map reversed
                wrap_idx = face_size + (1 + face_size - col_idx)
                self.cols[offset+col_idx].endward_wrap = (self.rows[wrap_idx], '>')


    # TODO: lines now return how far the move still has to go.
    # Check the line's 'starward_wrap' or 'endward_wrap'
    # If there's no wall blocking, advance to new line, call move with new params.
    # At end: return dir as well as pos.
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

def test_move_round_cube():
    maplines, path = fetch_data('sample_data/day22.txt')
    cube = Cube(maplines)
    assert cube.move(((6,12),'>'), 1) == ((9,15),'v') # A to B puzzle example
    assert cube.move(((8,2),'^'), 1) == ((9,15),'v') # C to D puzzle example

def test_wall_blocks_moving_round():
    maplines, path = fetch_data('sample_data/day22.txt')
    cube = Cube(maplines)
    assert cube.move(((5,7),'^'), 1) == ((5,7),'^') # E puzzle example

def _test_follow_path():
    maplines, path = fetch_data('sample_data/day22.txt')
    board = Board(maplines)
    assert board.follow_path(path) == ((6,8), '>')

def _test_final_password():
    assert final_password('sample_data/day22.txt') == 6032

#-----------------------------------------------------#

if __name__ == "__main__":
    print(final_password('data/day22.txt'))



