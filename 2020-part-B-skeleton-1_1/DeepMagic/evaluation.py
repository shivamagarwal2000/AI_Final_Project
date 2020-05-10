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


def get_no_pieces(game_state, type):
    ans = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if game_state.x == i and game_state.y == j:
                if game_state.piece_type == type:
                    ans += game_state.no_of_pieces

    return ans


def eval(game_state):
    frnd_pieces = get_no_pieces(game_state, frnd)
    enem_pieces = get_no_pieces(game_state, enem)
    weight = 10

    return weight * (frnd_pieces - enem_pieces)


def utility(game_state):
    enem_pieces = get_no_pieces(game_state, enem)
    frnd_pieces = get_no_pieces(game_state, frnd)
    if enem_pieces == 0:
        return 1000
    elif frnd_pieces == 0:
        return -1000
    else:
        return 0