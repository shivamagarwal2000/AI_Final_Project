
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
