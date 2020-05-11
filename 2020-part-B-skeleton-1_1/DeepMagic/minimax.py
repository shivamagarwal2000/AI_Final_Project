# the minimax algorithm that decides which action to play next

from .actions import *

from .evaluation import *
import random


class MinimaxAgent:

    def __init__(self, max_depth):

        self.max_depth = max_depth

    def minimax_decision(self, player):
        list_actions = valid_moves(player.pieces, player.opponent)
        # print(len(list_actions))
        value = [None] * len(list_actions)
        
        for i, action in enumerate(list_actions):
            temp_player = apply_action(action, player)
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
        if depth == 0 or terminal(player) == True:
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
