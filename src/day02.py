def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.split()

# dictionary of {my_play: (scores, beats)}
rules = {
    'Rock': (1, 'Scissors'),
    'Paper': (2, 'Rock'),
    'Scissors': (3, 'Paper')
}

def translate(c):
    if c in 'AX': return 'Rock'
    elif c in 'BY': return 'Paper'
    elif c in 'CZ': return 'Scissors'

def score_for_round(their_play, my_play):
    their_play, my_play = translate(their_play), translate(my_play)
    score, my_play_beats = rules[my_play]

    if my_play_beats == their_play:
        score += 6
    elif my_play == their_play:
        score += 3
    return score
    
def score_for_strategy(data):
    return sum(score_for_round(*r) for r in data)



#--------------------- tests -------------------------#

def test_score_for_round():
    assert score_for_round('A', 'Y') == 8
    assert score_for_round('B', 'X') == 1
    assert score_for_round('C', 'Z') == 6

def test_score_for_strategy():
    data = fetch_data('sample_data/day02.txt')
    assert score_for_strategy(data) == 15

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day02.txt')
    print(score_for_strategy(data))
