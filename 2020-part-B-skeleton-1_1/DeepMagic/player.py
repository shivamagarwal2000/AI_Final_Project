# Assignment 2 COMP30024: Artificial Intelligence Semester 1 2020

# Group Name: DeepMagic
# 
# Student 1 Name: Chan Jie Ho
# Student 1 Number: 961948
#
# Student 2 Name: Shivam Agarwal
# Student 2 Number: 951424

# ============================================================================ #

from .actions import *  # Boom, Move, valid_moves, move, boom
from .evaluation import *
import copy

_BLACK_ = [(7, 0), (7, 1), (7, 3), (7, 4), (7, 6), (7, 7),
           (6, 0), (6, 1), (6, 3), (6, 4), (6, 6), (6, 7)]
_WHITE_ = [(1, 0), (1, 1), (1, 3), (1, 4), (1, 6), (1, 7),
           (0, 0), (0, 1), (0, 3), (0, 4), (0, 6), (0, 7)]


class ExamplePlayer:

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.

        self.colour = colour
        if colour == "white":
            self.state, self.pieces, self.opponent = set_board(_WHITE_, _BLACK_)
        else:
            self.state, self.pieces, self.opponent = set_board(_BLACK_, _WHITE_)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        get_all_states(self, (self.pieces, self.opponent), True)

        return ("BOOM", (0, 0))

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.

        if action[0] == "MOVE":
            n, origin, destination = action[1:]
            move(self, n, origin, destination, colour)
        else:
            coordinates = action[1]
            boom(self, coordinates, colour)


# game_state will be in the form of (self.pieces, self.opponent)
# returns a list of all states possible after applying all the possible actions
def get_all_states(player, game_state, maximising_player):
    all_states = []
    pieces, opponent = game_state

    if maximising_player:
        moves = valid_moves(pieces, opponent)
        colour = player.colour
    else:
        moves = valid_moves(opponent, pieces)
        if player.colour == "white":
            colour = "black"
        else:
            colour = "white"

    for movement in moves:
        action = movement.get_tuple_form()
        temp = copy.deepcopy(player)
        if action[0] == "MOVE":
            n, origin, destination = action[1:]
            move(temp, n, origin, destination, colour)
        else:
            coordinates = action[1]
            boom(temp, coordinates, colour)

        new_player_pieces = temp.pieces
        new_enemy_pieces = temp.opponent

        all_states.append((new_player_pieces, new_enemy_pieces))

    return all_states


# the minimax algorithm that decides which move to play next
def minimax(player, depth, maximising_player):
    if depth == 0 or terminal(player) == True:
        return evaluate(player)

    # apply all actions to the state and return the list of all the possible states
    all_states = get_all_states(player, player.state, maximising_player)

    if maximising_player:
        value = -1000000
        for child in all_states:
            value = max(value, minimax(child, depth - 1, False))
        return value
    else:
        value = 1000000
        for child in all_states:
            value = min(value, minimax(child, depth - 1, True))
        return value


# ---------------------------------------------------------------------------- #

class CellObject:
    def __init__(self, n, min_or_max, coordinate):
        self.n = n
        self.type = min_or_max
        self.coordinate = coordinate


def set_board(player_pieces, enemy_pieces):
    board = [[0 for x in range(8)] for y in range(8)]

    for x in range(8):
        for y in range(8):
            board[x][y] = CellObject(0, None, (x, y))

    player = {}
    enemy = {}
    for square in player_pieces:
        x, y = square
        board[x][y] = CellObject(1, "max", (x, y))
        player[(x, y)] = 1
    for square in enemy_pieces:
        x, y = square
        board[x][y] = CellObject(1, "min", (x, y))
        enemy[(x, y)] = 1

    return board, player, enemy
