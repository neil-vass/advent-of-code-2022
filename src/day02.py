
translate = { 
    'A': 'Rock', 'B': 'Paper', 'C': 'Scissors',
    'X': 'Lose', 'Y': 'Draw', 'Z': 'Win'
}

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield [translate[c] for c in ln.split()]


points_for = { 'Rock': 1, 'Paper': 2, 'Scissors': 3 }

loses_to = { 'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper' }
wins_against = {v: k for k, v in loses_to.items()}


def score_for_round(their_play, i_should):
    if i_should == 'Lose':
        my_play = loses_to[their_play]
        score = 0
    elif i_should == 'Draw':
        my_play = their_play
        score = 3
    else:
        my_play = wins_against[their_play]
        score = 6

    return score + points_for[my_play]
    
def score_for_strategy(data):
    return sum(score_for_round(*r) for r in data)



#--------------------- tests -------------------------#

def test_score_for_round():
    assert score_for_round(translate['A'], translate['Y']) == 4
    assert score_for_round(translate['B'], translate['X']) == 1
    assert score_for_round(translate['C'], translate['Z']) == 7

def test_score_for_strategy():
    data = fetch_data('sample_data/day02.txt')
    assert score_for_strategy(data) == 12

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day02.txt')
    print(score_for_strategy(data))
