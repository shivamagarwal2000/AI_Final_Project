# Assignment 2 COMP30024: Artificial Intelligence Semester 1 2020

# Group Name: DeepMagic
# 
# Student 1 Name: Chan Jie Ho
# Student 1 Number: 961948
#
# Student 2 Name: Shivam Agarwal
# Student 2 Number: 951424

# Player module holds all the classes and functions required to define the 
# player that will be playing the Expendibots game 

from DeepMagic.actions import * 
from DeepMagic.evaluation import *
                        
# ============================================================================ #
# EXAMPLEPLAYER CLASS #
# ------------------- #
#
# ExamplePlayer class that will play the Expendibots game, keeping track of its 
# own pieces and the opponents pieces, then choosing the best possible action 
# from the all the possible movements using a minimax algorithm, updating after 
# each player's turn.

class ExamplePlayer:

    # __INIT__ FUNCTION #
    # ----------------- #

    # Player constructor that sets up an 8x8 matrix of the board as well as two 
    # dictionaries that will allow the player to keep track of the pieces that 
    # the player controls and the pieces that the opponent controls.

    # It takes the colour of the player (either "black" or "white") as input.
    
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
        
        # Initial coordinates of the pieces
        _BLACK_ = [(7,0), (7,1), (7,3), (7,4), (7,6), (7,7), 
                   (6,0), (6,1), (6,3), (6,4), (6,6), (6,7)]
        _WHITE_ = [(1,0), (1,1), (1,3), (1,4), (1,6), (1,7), 
                   (0,0), (0,1), (0,3), (0,4), (0,6), (0,7)]

        self.colour = colour
        
        if colour == "white":
            self.state, self.pieces, self.opponent = set_board(_WHITE_, _BLACK_)
    
        else:
            self.state, self.pieces, self.opponent = set_board(_BLACK_, _WHITE_)

    # ------------------------------------------------------------------------ #
    # ACTION FUNCTION #
    # --------------- #

    # Action function that decides what action the player should take

    # It returns the best possible action, decided by the minimax algorithm

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

    # ------------------------------------------------------------------------ #
    # UPDATE FUNCTION #
    # --------------- #

    # Update function that updates the internal representation of the board and 
    # the pieces remaining on the board that the player and the opponent 
    # controls after each player's turn.

    # It takes in the colour of the player that last performed the action and 
    # the action performed.

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

        # Determine if the action was a move or boom action and perform it
        if action[0] == "MOVE":
            n, origin, destination = action[1:]
            move(self, n, origin, destination, colour)

        else:
            coordinates = action[1]
            boom(self, coordinates, colour)

# ============================================================================ #
# CELLOBJECT CLASS #
# ---------------- #
#
# CellObject class that makes up each individual tile in the 8x8 matrix.

class CellObject:

    # __INIT__ FUNCTION #
    # ----------------- #

    # CellObject constructor that sets what each tile holds.

    # It takes in the number of pieces on that tile and the type of the pieces (whether the algorithm will be finding the max of it – the player – or the min – the opponent) and the coordinates.

    def __init__(self, n, min_or_max, coordinate):
        self.n = n
        self.type = min_or_max
        self.coordinate = coordinate

# ---------------------------------------------------------------------------- #
# SET_BOARD FUNCTION #
# ------------------ #
#
# Helper function that creates the initial 8x8 matrix of CellObjects and places 
# all the initial pieces on the corresponding tiles.
# 
# It takes the coordinates of the player's pieces and those of the opponenet's 
# pieces input and returns 8x8 board, and the dictionaries of the coordinates 
# of the player's and enemy's pieces and how many pieces are on each coordinate.

def set_board(player_pieces, enemy_pieces):

        board = [[0 for x in range(8)] for y in range(8)]

        # Fill the 8x8 matrix with empty tiles first
        for x in range(8):
            for y in range(8):
                board[x][y] = CellObject(0, None, (x, y))

        # Iterate through the given coordinates and fill the 8x8 matrix with 
        # the pieces and add it to a dictionary to keep track of the pieces
        # using the same representation as Assignment 1
        player = {}
        enemy = {}

        for square in player_pieces:
            x, y = square
            board[x][y] = CellObject(1, "max", (x,y))
            player[(x,y)] = 1

        for square in enemy_pieces:
            x, y = square
            board[x][y] = CellObject(1, "min", (x,y))
            enemy[(x,y)] = 1

        return board, player, enemy

# ============================================================================ #

# :)