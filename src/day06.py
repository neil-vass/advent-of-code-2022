def fetch_data(path):
    with open(path, 'r') as f:
        return f.readline().rstrip()

def chars_to_marker(data, window_size):
    window_start = 0
    while True:
        window_end = window_start + window_size
        if len(set(data[window_start:window_end])) == window_size:
            return window_end
        window_start += 1

#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day06.txt')
    assert data == 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

def test_chars_to_marker():
    data = fetch_data('sample_data/day06.txt')
    assert chars_to_marker(data, window_size=14) == 19


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day06.txt')
    print(chars_to_marker(data, window_size=14))
