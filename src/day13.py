
import ast

class PacketPair:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def in_right_order(self):
        return packets_are_in_right_order(self.left, self.right) 


def packets_are_in_right_order(l: list, r: list):
    for i in range(max(len(l), len(r))):
        if i < min(len(l), len(r)):
            left_val = l[i]
            right_val = r[i]
            if isinstance(left_val, int) and isinstance(right_val, int):
                if left_val < right_val:
                    return True
                if left_val > right_val:
                    return False
            else:
                if isinstance(left_val, int):
                    left_val = [left_val]
                if isinstance(right_val, int):
                    right_val = [right_val] 
                sublist_result = packets_are_in_right_order(left_val, right_val)
                if sublist_result is not None:
                    return sublist_result                     
        if i == len(l):
            return True
        if i == len(r):
            return False 


def fetch_data(path):
    with open(path, 'r') as f:
        while True:
            try:
                left = ast.literal_eval(next(f))
                right = ast.literal_eval(next(f))
                yield PacketPair(left, right)
                next(f)
            except StopIteration:
                return

def sum_indices_of_pairs_in_right_order(data):
    total = idx = 0
    for pair in data:
        idx += 1
        if pair.in_right_order():
            total += idx
    return total


def fetch_packets(path):
    with open(path, 'r') as f:
        for ln in f:
            if ln.rstrip():
                yield ast.literal_eval(ln)

def add_dividers_and_sort_all_packets(packets):
    result = [ [[2]], [[6]] ]
    for p in packets:
        inserted = False
        for i in range(len(result)):
            if packets_are_in_right_order(p, result[i]):
                result.insert(i, p)
                inserted = True
                break
        if not inserted:
            result.append(p)
    return result

def find_decoder_key(sorted_packets):
    return (sorted_packets.index([[2]])+1) * (sorted_packets.index([[6]])+1) 
    

#--------------------- tests -------------------------#

def test_fetch_data():
    data = list(fetch_data('sample_data/day13.txt'))
    assert len(data) == 8
    assert data[0].left == [1,1,3,1,1]
    assert data[0].right == [1,1,5,1,1]

def test_in_right_order():
    data = fetch_data('sample_data/day13.txt')
    assert next(data).in_right_order(), "Pair 1: [1,1,3,1,1] vs [1,1,5,1,1]"
    assert next(data).in_right_order(), "Pair 2: [[1],[2,3,4]] vs [[1],4]"
    assert not next(data).in_right_order(), "Pair 3: [9] vs [[8,7,6]]"
    assert next(data).in_right_order(), "Pair 4: [[4,4],4,4] vs [[4,4],4,4,4]" 
    assert not next(data).in_right_order(), "Pair 5: [7,7,7,7] vs [7,7,7]"
    assert next(data).in_right_order(), "Pair 6: [] vs [3]"
    assert not next(data).in_right_order(), "Pair 7: [[[]]] vs [[]]"
    assert not next(data).in_right_order(), "Pair 8: [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]"

def test_sum_indices_of_pairs_in_right_order():
    data = fetch_data('sample_data/day13.txt')
    assert sum_indices_of_pairs_in_right_order(data) == 13

def test_add_dividers_and_sort_all_packets():
    packets = fetch_packets('sample_data/day13.txt')
    sorted_packets = add_dividers_and_sort_all_packets(packets)
    assert len(sorted_packets) == 18
    assert sorted_packets[0] == []
    assert sorted_packets[9] == [[2]]

def test_find_decoder_key():
    packets = fetch_packets('sample_data/day13.txt')
    sorted_packets = add_dividers_and_sort_all_packets(packets)
    assert find_decoder_key(sorted_packets) == 140

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day13.txt')
    print(f"Part 1: {sum_indices_of_pairs_in_right_order(data)}")

    packets = fetch_packets('data/day13.txt')
    sorted_packets = add_dividers_and_sort_all_packets(packets)
    print(f"Part 2: {find_decoder_key(sorted_packets)}")

