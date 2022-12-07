import re

class Dir:
    def __init__(self, name):
        self.name = name
        self._contents = []
    
    def size(self, sizelist=None):
        my_size = sum(c.size(sizelist) for c in self._contents)
        
        if sizelist is not None:
            sizelist.append(my_size)
        return my_size


    def add(self, child):
        child._parent = self
        self._contents.append(child)
    
    def find(self, arg):
        val = None
        if arg == '..':
            val = self._parent
        else:
            val = next(c for c in self._contents if c.name == arg)
        
        if not val:
            raise ValueError(f"Can't move to {arg} from {self.name}")
        return val


class File:
    def __init__(self, size, name):
        self.name = name
        self._size = int(size)

    def size(self, *ignored):
        return self._size


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'^\$ (cd) (.+)$', ln)
            if m:
                yield [m[1], m[2]]
            elif ln.startswith('$ ls'):
                continue
            else:
                yield ln.rstrip().split()


def build_filesystem_from_terminal_output(data):
    filesystem = cwd = None
    
    for arg1, arg2 in data:
        if arg1 == 'cd':
            if not filesystem:
                filesystem = cwd = Dir(arg2)
            else:
                cwd = cwd.find(arg2) 
        elif arg1 == 'dir':
            cwd.add(Dir(arg2))
        else:
            cwd.add(File(arg1, arg2))
    return filesystem


def solve_part_one(data):
    filesystem = build_filesystem_from_terminal_output(data)
    sizelist = []
    filesystem.size(sizelist)
    return sum(s for s in sizelist if s <= 100000)

def solve_part_two(data):
    filesystem = build_filesystem_from_terminal_output(data)
    sizelist = []
    total_used_space = filesystem.size(sizelist)
    space_needed = total_used_space - 40000000
    return sorted(s for s in sizelist if s >= space_needed)[0]

#--------------------- tests -------------------------#

def test_build_filesystem():
    sut = Dir('/')
    assert sut.name == '/'
    assert sut.size() == 0

    sut.add(Dir('a'))
    sut.add(File('14848514', 'b.txt'))
    assert sut.size() == 14848514

def test_navigate_filesystem():
    sut = Dir('/')
    subfolder = Dir('a')
    sut.add(subfolder)
    assert sut.find('a').name == 'a'
    assert subfolder.find('..').name == '/'


def test_read_terminal_output():
    data = fetch_data('sample_data/day07.txt')
    assert next(data) == ['cd', '/']
    # skip over 'ls', we just want the listings that come after.
    assert next(data) == ['dir', 'a']
    assert next(data) == ['14848514', 'b.txt']


def test_build_filesystem_from_terminal_output():
    data = fetch_data('sample_data/day07.txt')
    sut = build_filesystem_from_terminal_output(data)
    assert sut.name == '/'
    assert len(sut._contents) == 4
    assert sut.size() == 48381165

def test_get_total_sizes():
    data = fetch_data('sample_data/day07.txt')
    sut = build_filesystem_from_terminal_output(data)
    sizelist = []
    sut.size(sizelist)
    assert sizelist == [584, 94853, 24933642, 48381165]

def test_solve_part_one():
    data = fetch_data('sample_data/day07.txt')
    assert solve_part_one(data) == 95437

def test_solve_part_two():
    data = fetch_data('sample_data/day07.txt')
    assert solve_part_two(data) == 24933642

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day07.txt')
    print(solve_part_two(data))
    # 10618286 is too high. What's gone wrong?