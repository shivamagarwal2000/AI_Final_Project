# the minimax algorithm that decides which action to play next
class MinimaxAgent:

    def __init__(self, max_depth, player_color):

        self.max_depth = max_depth



    def minimax_decision(self, player):


    def minimax_val(self, player, depth, maximising_player):
        if depth == 0 or terminal(player) == True:
            return evaluate(player)

        # apply all actions to the state and return the list of all the possible states
        all_states = get_all_states(player, player.state, maximising_player)

        if maximising_player:
            value = -1000000
            for child in all_states:
                value = max(value, minimax_val(child, depth - 1, False))
            return value
        else:
            value = 1000000
            for child in all_states:
                value = min(value, minimax_val(child, depth - 1, True))
            return value