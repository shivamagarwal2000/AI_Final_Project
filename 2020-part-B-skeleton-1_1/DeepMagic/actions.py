from referee.game import _NEXT_SQUARES, _NEAR_SQUARES

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
            # self.pieces.remove((xa,ya))
            del player.pieces[(xa,ya)]
        else:
            # self.opponent.remove((xa,ya))
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
        # self.pieces.remove((x,y))
        del player.pieces[(x,y)]
    else:
        # self.opponent.remove((x,y))
        del player.opponent[(x,y)]

    for (near_x, near_y) in _NEAR_SQUARES((x,y)):
        if player.state[near_x][near_y].n != 0:
            boom(player, (near_x, near_y), colour)