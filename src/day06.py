def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

#--------------------- tests -------------------------#

def test_basics():
    data = fetch_data('sample_data/day06.txt')
    assert data == 0

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day06.txt')
    print('Hello, World!')
