def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

char_to_digit = {'0':0, '1':1, '2':2, '-':-1, '=':-2}
digit_to_char = {v:k for k,v in char_to_digit.items()}

def think(target, so_far, idx):
    if target == 0:
        return so_far
    # what can I remove from target so it becomes a multiple of the next idx?
    for digit in (-2, -1, 0, 1, 2):
        value = digit * (5**idx)
        if ((target-value) % (5**(idx+1))) == 0:
            return think(target-value, digit_to_char[digit] + so_far, idx+1)


def to_snafu(n):
    return think(n, '', 0)
        

def to_decimal(snafu):
    snafu = reversed(snafu)
    return sum(char_to_digit[n]*(5**idx) for idx, n in enumerate(snafu))

#--------------------- tests -------------------------#

def test_to_snafu():
    assert to_snafu(1) == '1'
    assert to_snafu(2) == '2'
    assert to_snafu(3) == '1='
    assert to_snafu(4) == '1-'
    assert to_snafu(5) == '10'
    assert to_snafu(6) == '11'
    assert to_snafu(7) == '12'
    assert to_snafu(8) == '2='
    assert to_snafu(9) == '2-'
    assert to_snafu(10) == '20'
    assert to_snafu(15) == '1=0'
    assert to_snafu(314159265) == '1121-1110-1=0'


def test_to_decimal():
    assert to_decimal('12') == 7
    assert to_decimal('112') == 32
    assert to_decimal('12111') == 906
    assert to_decimal('1=-1=') == 353
    assert to_decimal('1=-0-2') == 1747


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day25.txt')
    print('Hello, World!')
