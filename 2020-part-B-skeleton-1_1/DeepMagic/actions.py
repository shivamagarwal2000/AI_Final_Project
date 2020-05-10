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
import copy

class Action:
    def __init__(self, name):
        self.name = name


class Boom(Action):
    def __init__(self, coord):
        super().__init__('BOOM')
        self.x = coord[0]
        self.y = coord[1]

    def get_tuple_form(self):
        my_tuple = (self.name, (self.x, self.y))
        return my_tuple


class Move(Action):
    def __init__(self, no, s_coord, d_coord):
        super().__init__('MOVE')
        self.no_of_pieces = no
        self.src_x = s_coord[0]
        self.src_y = s_coord[1]
        self.dst_x = d_coord[0]
        self.dst_y = d_coord[1]

    def get_tuple_form(self):
        my_tuple = (self.name, self.no_of_pieces, (self.src_x, self.src_y), (self.dst_x, self.dst_y))
        return my_tuple

def valid_moves(player_pieces, enemy_pieces):
    valid = []
    direction = ['N', 'S', 'E', 'W']

    for piece in player_pieces.keys():

        # Can boom
        x, y = piece
        n = player_pieces[piece]
        valid.append(Boom((x,y)))

        # List moves
        for hello in range(1, n+1):
            for steps in range(1, n+1):
                for cardinal in direction:

                    dest_x = x
                    dest_y = y
                    if cardinal == 'N':
                        dest_y += steps

                    elif cardinal == 'S':
                        dest_y -= steps

                    elif cardinal == 'E':
                        dest_x += steps

                    else:
                        dest_x -= steps

                    if dest_x in range(8) and dest_y in range(8):
                        if (dest_x, dest_y) in player_pieces or not ((dest_x, dest_y) in enemy_pieces):
                            valid.append(Move(n, (x,y), (dest_x, dest_y)))

    return valid

# ("MOVE", n, (xa, ya), (xb, yb))
def move(player, pieces, origin, destination, colour):
    xa, ya = origin
    xb, yb = destination
    player.state[xb][yb].n += pieces

    if player.colour == colour:
        player.pieces[(xb,yb)] = player.state[xb][yb].n
    else:
        player.opponent[(xb,yb)] = player.state[xb][yb].n

    player.state[xb][yb].type = player.state[xa][ya].type
    player.state[xa][ya].n -= pieces
    
    if player.state[xa][ya].n == 0:
        player.state[xa][ya].type = None

        if player.colour == colour:
            del player.pieces[(xa,ya)]
        else:
            del player.opponent[(xa,ya)]
            
    else:
        if player.colour == colour:
            player.pieces[(xa,ya)] = player.state[xa][ya].n
        else:
            player.opponent[(xa,ya)] = player.state[xa][ya].n


# ("BOOM", (x, y))
def boom(player, coordinate, colour):
    x, y = coordinate
    player.state[x][y].n = 0
    player.state[x][y].type = None

    if player.colour == colour:
        del player.pieces[(x,y)]
    else:
        del player.opponent[(x,y)]

    for (near_x, near_y) in _NEAR_SQUARES((x,y)):
        if player.state[near_x][near_y].n != 0:
            boom(player, (near_x, near_y), colour)

# game_state will be in the form of (self.pieces, self.opponent)
# returns a list of all states possible after applying all the possible actions
def get_all_states(player, game_state, maximising_player):

    all_states = {}
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
        
        all_states[(action)] = (new_player_pieces, new_enemy_pieces)
    
    return all_states



# the minimax algorithm that decides which move to play next
def minimax(player, game_state, depth, maximising_player):
    if depth == 0 or terminal(game_state) == True:
        return eval(game_state)

    # apply all actions to the state and return the list of all the possible states
    all_states = get_all_states(player, game_state, maximising_player)

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