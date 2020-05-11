# Assignment 2 COMP30024: Artificial Intelligence Semester 1 2020

# Group Name: DeepMagic
# 
# Student 1 Name: Chan Jie Ho
# Student 1 Number: 961948
#
# Student 2 Name: Shivam Agarwal
# Student 2 Number: 951424

# ============================================================================ #

# the module will be used to estimate the evaluation function of the form
# Eval(s) = w1f1(s) + w2f2(s) + . . . + wnfn(s)


def get_no_pieces(player_pieces):
    ans = 0
    for piece in player_pieces.keys():
        n = player_pieces[piece]
        ans += n

    return ans


# find the chaining score of a state - the difference between the max chain size of player and the opponent
# def chaining_score()


def evaluate(player):
    frnd_pieces = get_no_pieces(player.pieces)
    enem_pieces = get_no_pieces(player.opponent)
    weight = 10

    if frnd_pieces == 0 and enem_pieces != 0:
        return -10000
    elif enem_pieces == 0 and frnd_pieces != 0:
        return 10000

    return weight * (frnd_pieces - enem_pieces)


def terminal(player):
    frnd_pieces = get_no_pieces(player.pieces)
    enem_pieces = get_no_pieces(player.opponent)
    if enem_pieces == 0 or frnd_pieces == 0:
        return True
    else:
        return False