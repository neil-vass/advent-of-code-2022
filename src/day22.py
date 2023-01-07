
def fetch_data(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return [ln.rstrip() for ln in lines[:-2]], lines[-1].rstrip()


def create_map(maplines):
    for x, ln in enumerate(maplines):
            for y, char in enumerate(ln.rstrip()):
                if char == '.':
                    map[(x,y)] = []




#--------------------- tests -------------------------#

def test_basics():
    maplines, path = fetch_data('sample_data/day22.txt')
    assert len(maplines) == 12
    assert maplines[0] == '        ...#'
    assert path == '10R5L5R10L4R5L5'

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day22.txt')
    print('Hello, World!')
