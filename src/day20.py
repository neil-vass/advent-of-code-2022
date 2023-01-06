

def fetch_data(path):
    with open(path, 'r') as f:
        data = []
        for ln in f:
            data.append(int(ln))
    return data

# This is messy, due to how Python list inserts work and this puzzle's requirements
def mix_step(data, idx_in_data, remix):
    current_pos = remix.index(idx_in_data)
    distance_to_move = data[idx_in_data]
    if distance_to_move == 0:
        return

    remix.pop(current_pos)
    new_pos = (current_pos + distance_to_move) % len(remix)
    if new_pos == 0:
        new_pos = len(remix)
    remix.insert(new_pos, idx_in_data)

  
def decrypt_data_file(data, steps=None):
    if steps is None:
        steps = len(data)

    remix = list(range(len(data)))
    for idx in range(steps):
        mix_step(data, idx, remix)
       
    # Apply remix to data
    return [data[pos] for pos in remix]


def get_coordinates(decrypted):
    start_idx = decrypted.index(0)
    return (
        decrypted[(start_idx + 1000) % len(decrypted)],
        decrypted[(start_idx + 2000) % len(decrypted)],
        decrypted[(start_idx + 3000) % len(decrypted)])
    

#--------------------- tests -------------------------#

def test_basic_decryption():
     assert decrypt_data_file([1,0,0]) == [0,1,0]
     assert decrypt_data_file([3,0,0]) == [0,3,0]
     assert decrypt_data_file([-1,0,0]) == [0,-1,0]

def test_fetch_data():
    data = fetch_data('sample_data/day20.txt')
    assert data == [1, 2, -3, 3, -2, 0, 4]

def test_decrypt_data_step_by_step():
    data = fetch_data('sample_data/day20.txt')
    assert decrypt_data_file(data, steps=1) == [2, 1, -3, 3, -2, 0, 4]
    assert decrypt_data_file(data, steps=2) == [1, -3, 2, 3, -2, 0, 4]
    assert decrypt_data_file(data, steps=3) == [1, 2, 3, -2, -3, 0, 4]
    assert decrypt_data_file(data, steps=4) == [1, 2, -2, -3, 0, 3, 4]
    assert decrypt_data_file(data, steps=5) == [1, 2, -3, 0, 3, 4, -2]

def test_decrypt_data_file_completely():
    data = fetch_data('sample_data/day20.txt')
    assert decrypt_data_file(data) == [1, 2, -3, 4, 0, 3, -2]

def test_get_coordinates():
    data = fetch_data('sample_data/day20.txt')
    decrypted = decrypt_data_file(data)
    assert get_coordinates(decrypted) == (4, -3, 2)


    

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day20.txt')
    decrypted = decrypt_data_file(data)
    coords = get_coordinates(decrypted)
    print(sum(coords))
    # Gets 11621 - 'your answer is too high'
