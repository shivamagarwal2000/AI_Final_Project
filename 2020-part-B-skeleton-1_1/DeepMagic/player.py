# Assignment 2 COMP30024: Artificial Intelligence Semester 1 2020

# Group Name: DeepMagic
# 
# Student 1 Name: Chan Jie Ho
# Student 1 Number: 961948
#
# Student 2 Name: Shivam Agarwal
# Student 2 Number: 951424

# ============================================================================ #

from referee.game import _NEXT_SQUARES, _NEAR_SQUARES

_BLACKS_ = [(7, 0), (7, 1), (7, 3), (7, 4), (7, 6), (7, 7),
            (6, 0), (6, 1), (6, 3), (6, 4), (6, 6), (6, 7)]
_WHITES_ = [(1, 0), (1, 1), (1, 3), (1, 4), (1, 6), (1, 7),
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
            self.state = set_board(_WHITES_, _BLACKS_)
        else:
            self.state = set_board(_BLACKS_, _WHITES_)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
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
            self.move(n, origin, destination)
        else:
            coordinates = action[1]
            self.boom(coordinates)

    # ("MOVE", n, (xa, ya), (xb, yb))

    def move(self, pieces, origin, destination):
        xa, ya = origin
        xb, yb = destination
        self.state[xb][yb].n += pieces
        self.state[xb][yb].type = self.state[xa][ya].type
        self.state[xa][ya].n -= pieces

        if self.state[xa][ya].n == 0:
            self.state[xa][ya].type = None

    # ("BOOM", (x, y))
    def boom(self, coordinate):
        x, y = coordinate
        self.state[x][y] = CellObject(0, None, (x, y))

        for (near_x, near_y) in _NEAR_SQUARES((x, y)):
            if self.state[near_x][near_y].n != 0:
                self.boom((near_x, near_y))


# ---------------------------------------------------------------------------- #

class CellObject():

    def __init__(self, n, min_or_max, coordinate):
        self.n = n
        self.type = min_or_max
        self.coordinate = coordinate


def set_board(player_pieces, enemy_pieces):
    board = [[0 for x in range(8)] for y in range(8)]

    for x in range(8):
        for y in range(8):
            board[x][y] = CellObject(0, None, (x, y))

    for square in player_pieces:
        x, y = square
        board[x][y] = CellObject(1, "max", (x, y))
    for square in enemy_pieces:
        x, y = square
        board[x][y] = CellObject(1, "min", (x, y))

    return board