import copy
from dlgo.gotypes import Player

class Move():
    def __init__(self, point = None, is_pass = False, is_resign = False):
        #typically you would not create a Move directly,
        # but rather construct an instance by calling the 3 class methods: play, pass_turn, or resign
        assert (point is not None) ^ is_pass ^ is_resign # this is asserting that only 1 or all 3 has to be true
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        # first input of class method is cls to differentiate them from instance methods
        return Move(point = point)
    
    @classmethod 
    def pass_turn(cls):
        return Move(is_pass = True)
    
    @classmethod
    def resign(cls):
        return(Move(is_resign = True))
    
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones) # this uses the data type and removes duplicates
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point) # self.liberties is a set

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones # union the two sets
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )
    
    @property
    def num_liberties(self):
        return(len(self.liberties)) # it's a set, so calling len on it is polymorphism
    
    def __eq__ (self, other):
        return isinstance(other, GoString) and \
        self.color ==other.color and \
        self.stones == other.stones and \
        self.liberties == other.liberties 
    
