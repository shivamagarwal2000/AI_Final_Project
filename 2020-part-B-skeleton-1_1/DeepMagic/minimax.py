# the minimax algorithm that decides which action to play next

from .actions import *

from .evaluation import *


class MinimaxAgent:

    def __init__(self, max_depth):

        self.max_depth = max_depth

    def minimax_decision(self, player):
        list_actions = valid_moves(player.pieces, player.opponent)
        value = []

        for i, action in enumerate(list_actions):
            temp_player = apply_action(action, player)
            value[i] = self.minimax_val(temp_player, self.max_depth, False)

        maximum = 0
        for i, val in enumerate(value):
            if val > maximum:
                maximum = value
                index = i

        return list_actions[index]

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
