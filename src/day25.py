def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

char_to_digit = {'0':0, '1':1, '2':2, '-':-1, '=':-2}
digit_to_char = {v:k for k,v in char_to_digit.items()}

def to_snafu(n):
    return digit_to_char[n]
    

def to_decimal(snafu):
    snafu = reversed(snafu)
    return sum(char_to_digit[n]*(5**idx) for idx, n in enumerate(snafu))

#--------------------- tests -------------------------#

def test_to_snafu():
    assert to_snafu(1) == '1'
    assert to_snafu(2) == '2'
    assert to_snafu(3) == '1='

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
