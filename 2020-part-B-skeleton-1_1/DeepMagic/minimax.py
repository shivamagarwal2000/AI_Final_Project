# the minimax algorithm that decides which action to play next

from .actions import *

from .evaluation import *
import random


class MinimaxAgent:

    def __init__(self, max_depth, move_no):

        self.max_depth = max_depth
        self.move_no = move_no

    def minimax_decision(self, player):
        list_actions = valid_moves(player.pieces, player.opponent)

        # print(len(list_actions))
        if self.move_no < 5:
            remove_booms(list_actions)

        length = len(list_actions)

        # print(len(list_actions))
        value = [None] * length

        if length < 20:
            self.max_depth = 2

        elif length < 10:
            self.max_depth = 3

        for i, action in enumerate(list_actions):
            temp_player = apply_action(action, player)
            if self.max_depth < 2:
                value[i] = evaluate(temp_player)
            else:
                value[i] = self.minimax_val(temp_player, self.max_depth, False)
            # print(value[i])

        maximum = -10000

        for i, val in enumerate(value):
            if val > maximum:
                maximum = val
                index = i
        # return random.choice(list_actions).get_tuple_form()
        return list_actions[index].get_tuple_form()

    def minimax_val(self, player, depth, maximising_player):
        # if depth == 0 or terminal(player) == True:
        #     return evaluate(player)

        if depth == 0:
            return evaluate(player)

        # apply all actions to the state and return the list of all the possible states
        # list of tuples of player pieces and opponent pieces
        all_states = get_all_states(player, maximising_player)

        if maximising_player:
            value = -1000000
            for child in all_states:
                value = max(value, self.minimax_val(child, depth - 1, False))
            return value
        else:
            value = 1000000
            for child in all_states:
                value = min(value, self.minimax_val(child, depth - 1, True))
            return value
