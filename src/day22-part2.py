import re

def fetch_data(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        maplines = [ln.rstrip() for ln in lines[:-2]]
        path = lines[-1].rstrip()
        if len(path) == 0:
            raise Exception('Path has no instructions!')
        return maplines, path


class Line:
    def __init__(self):
        self.start = self.end = None
        self.walls = []
        self.startward_wrap = self.endward_wrap = None
    
    def move_endward(self, current_pos, tiles):  
        farthest_move = next((w-1 for w in self.walls if w > current_pos), self.end) - current_pos
        dist = min(tiles, farthest_move) 
        new_pos = current_pos + dist
        remaining_move = (tiles - dist) if (new_pos == self.end and self.endward_wrap is not None) else 0
        return new_pos, remaining_move


    def move_startward(self, current_pos, tiles):
        farthest_move = current_pos - next(reversed([w+1 for w in self.walls if w < current_pos]), self.start)
        dist = min(tiles, farthest_move)
        new_pos = current_pos - dist
        remaining_move = (tiles - dist) if (new_pos == self.start and self.startward_wrap is not None) else 0
        return new_pos, remaining_move


class Cube:
    def __init__(self, maplines, folding='sample'):
        self.rows, self.cols = Cube._create_map(maplines)
        if folding == 'sample':
            self.face_size = 4
            self._create_wrapping_rules_for_sample()
        else:
            self.face_size = 50
            self._create_wrapping_rules_for_actual()

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


    def set_wrap_rule_for_face(self, from_face_pos, from_dir, to_face_pos, to_dir, map_reversed=False):
        from_lines = self.rows if from_dir in '<>' else self.cols
        to_lines = self.rows if to_dir in '<>' else self.cols

        for line_num in range(1, self.face_size+1):
            from_idx = (from_face_pos * self.face_size) + line_num
            if map_reversed:
                to_idx = (to_face_pos * self.face_size) + (1 + self.face_size - line_num)
            else:
                to_idx = (to_face_pos * self.face_size) + line_num

            # Set wrapping mapping, unless we're going to immediately hit a wall.
            first_pos_on_wrapped_line = to_lines[to_idx].start if to_dir in '>v' else to_lines[to_idx].end
            if first_pos_on_wrapped_line in to_lines[to_idx].walls:
                continue

            if to_dir == '>':
                wrapping_mapping = ((to_idx, to_lines[to_idx].start), to_dir)
            elif to_dir == '<':
                wrapping_mapping = ((to_idx, to_lines[to_idx].end), to_dir)
            elif to_dir == 'v':
                wrapping_mapping = ((to_lines[to_idx].start, to_idx), to_dir)
            elif to_dir == '^':
                wrapping_mapping = ((to_lines[to_idx].end, to_idx), to_dir)

            if from_dir in '<^':
                from_lines[from_idx].startward_wrap = wrapping_mapping
            else:
                from_lines[from_idx].endward_wrap = wrapping_mapping


    # We're wrapping this cube 
    # ..1.
    # 234.
    # ..56 
    def _create_wrapping_rules_for_sample(self):
        # "From" for all the rows
        # 1< to 3v (col)
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='<', to_face_pos=1, to_dir='v')
        # 1> to 6<, map reversed 
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='>', to_face_pos=2, to_dir='<', map_reversed=True)
        # 2< to 6^ (col), map reversed
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='<', to_face_pos=3, to_dir='^', map_reversed=True)
        # 4> to 6v (col), map reversed
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='>', to_face_pos=3, to_dir='v', map_reversed=True)
        # 5< to 3^ (col), map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='<', to_face_pos=1, to_dir='^', map_reversed=True)
        # 6> to 1<, map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='>', to_face_pos=0, to_dir='<', map_reversed=True)

        
        # "From" for all the columns
        # 2^ to 1v, map reversed
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='^', to_face_pos=2, to_dir='v', map_reversed=True)
        # 2v to 5^, map reversed
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='v', to_face_pos=2, to_dir='^', map_reversed=True)
        # 3^ to 1> (row)
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='^', to_face_pos=0, to_dir='>')
        # 3v to 5> (row), map reversed
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='v', to_face_pos=2, to_dir='>', map_reversed=True)
        # 1^ to 2v, map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='^', to_face_pos=0, to_dir='v', map_reversed=True)
        # 5v to 2^, map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='v', to_face_pos=0, to_dir='^', map_reversed=True)
        # 6^ to 4< (row), map reversed
        self.set_wrap_rule_for_face(from_face_pos=3, from_dir='^', to_face_pos=1, to_dir='<', map_reversed=True)


    # We're wrapping this cube 
    # .12
    # .3.
    # 45.
    # 6.. 
    def _create_wrapping_rules_for_actual(self):
        # Rows
        # 1< to 4>, map reversed
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='<', to_face_pos=2, to_dir='>', map_reversed=True)
        # 2> to 5<, map reversed
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='>', to_face_pos=2, to_dir='<', map_reversed=True)
        # 3< to 4v (col)
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='<', to_face_pos=0, to_dir='v')
        # 3> to 2^ (col)
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='>', to_face_pos=2, to_dir='^')
        # 4< to 1>, map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='<', to_face_pos=0, to_dir='>', map_reversed=True)
        # 5> to 2<, map reversed
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='>', to_face_pos=0, to_dir='<', map_reversed=True)
        # 6< to 1v (col)
        self.set_wrap_rule_for_face(from_face_pos=3, from_dir='<', to_face_pos=1, to_dir='v')
        # 6> to 5^ (col)
        self.set_wrap_rule_for_face(from_face_pos=3, from_dir='>', to_face_pos=1, to_dir='^')

        # Cols
        # 4^ to 3> (row)
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='^', to_face_pos=1, to_dir='>')
        # 6v to 2v
        self.set_wrap_rule_for_face(from_face_pos=0, from_dir='v', to_face_pos=2, to_dir='v')
        # 1^ to 6> (row)
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='^', to_face_pos=3, to_dir='>')
        # 5v to 6< (row)
        self.set_wrap_rule_for_face(from_face_pos=1, from_dir='v', to_face_pos=3, to_dir='<')
        # 2^ to 6^
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='^', to_face_pos=0, to_dir='^')
        # 2v to 3< (row)
        self.set_wrap_rule_for_face(from_face_pos=2, from_dir='v', to_face_pos=1, to_dir='<')
    

    def move(self, current_pos, dir, tiles):
        x,y = current_pos
        if dir == '>':
            y, remaining_move = self.rows[x].move_endward(y, tiles)
            if remaining_move:
                wrap_pos, dir = self.rows[x].endward_wrap
                ((x,y), dir) = self.move(wrap_pos, dir, remaining_move-1)
        elif dir == '<':
            y, remaining_move = self.rows[x].move_startward(y, tiles)
            if remaining_move:
                wrap_pos, dir = self.rows[x].startward_wrap
                ((x,y), dir) = self.move(wrap_pos, dir, remaining_move-1)
        elif dir == 'v':
            x, remaining_move = self.cols[y].move_endward(x, tiles)
            if remaining_move:
                wrap_pos, dir = self.cols[y].endward_wrap
                ((x,y), dir) = self.move(wrap_pos, dir, remaining_move-1)
        elif dir == '^':
            x, remaining_move = self.cols[y].move_startward(x, tiles)
            if remaining_move:
                wrap_pos, dir = self.cols[y].startward_wrap
                ((x,y), dir) = self.move(wrap_pos, dir, remaining_move-1)
        return ((x,y), dir)


    def follow_path(self, path):
        directions = '>v<^'
        current_pos = (1, self.rows[1].start)
        facing = '>'
        for instruction in re.findall(r'(\d+|L|R)', path):
            if instruction.isdigit():
                current_pos, facing = self.move(current_pos, dir=facing, tiles=int(instruction))
            elif instruction == 'L':
                facing = directions[(directions.index(facing) - 1) % len(directions)]
            elif instruction == 'R':
                facing = directions[(directions.index(facing) + 1) % len(directions)]
        return current_pos, facing


def final_password(path, folding='sample'):
    maplines, path = fetch_data(path)
    cube = Cube(maplines, folding)
    ((row, col), facing) = cube.follow_path(path)
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
    assert cube.move((6,12),'>', 1) == ((9,15),'v') # A to B puzzle example
    assert cube.move((12,11),'v', 1) == ((8,2),'^') # C to D puzzle example

def test_wall_blocks_moving_round():
    maplines, path = fetch_data('sample_data/day22.txt')
    cube = Cube(maplines)
    assert cube.move((5,7),'^', 1) == ((5,7),'^') # E puzzle example

def test_follow_path():
    maplines, path = fetch_data('sample_data/day22.txt')
    cube = Cube(maplines)
    assert cube.follow_path(path) == ((5,7), '^')

def test_final_password():
    assert final_password('sample_data/day22.txt') == 5031

#-----------------------------------------------------#

if __name__ == "__main__":
    print(final_password('data/day22.txt', folding='actual'))



