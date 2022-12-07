import re

class Dir:
    def __init__(self, name):
        self.name = name
        self._contents = []
    
    def size(self):
        return sum(c.size() for c in self._contents)

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

    def size(self):
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




#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day07.txt')
    print('Hello, World!')
