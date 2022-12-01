def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

#--------------------- tests -------------------------#

def test_basics():
    assert 1 == 0

#-----------------------------------------------------#

if __name__ == "__main__":
    print('Hello, World!')
