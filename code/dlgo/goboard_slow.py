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
    
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {} # underscore is convention that this variable is protected and should not be accessed/modified outside the class
        # I'm assuming grid is a dictionary mapping points to their GoStrings. When you call _grid.get(point) you get the string-of-stones that that point is attached to

    def place_stone(self, player, point):
        """
        This is a docstring for my_method.

        Args:
            param1: Description of the first parameter.
            param2: Description of the second parameter.

        Returns:
            Description of the return value (if any).
        """
        assert self.is_on_grid(point) # point exists on grid
        assert self._grid.get(point) is None # check that there's not already a stone there. _grid.get() returns the string of the stone that's there, or None if it's empty
        
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties =[]

        for neighbor in point.neighbors(): # we defined this in our gotypes.py, point.neighbors returns the 4 points surrounding the input point
            if not self.is_on_grid(neighbor):
                continue # if the neighboring point you are checking is off the grid, then continue the loop no need to do anything else
            
            neighbor_string = self._grid.get(neighbor) # grid is a dict mapping points to their GoStrings, neighbor is Point type
            if neighbor_string is None: # this is the GoString type we defined earlier
                # if neighbor_string is None, that means it's not already part of a GoString, meaning it is empty
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

            new_string = GoString(player, [point], liberties)
            for same_color_string in adjacent_same_color: # [?] finish this part of the code given what you know
                # merge the strings 
            for new_string_point in new_string.stones:
                # merge the strings
            for other_color_string in adjacent_opposite_color:
                # reduce liberties
            for other_color_string in adjacent_opposite_color:
                # capture if their liberties are now at 0


    def is_on_grid(self, point):
        # the grid will go from 1 to num_rows (not 0 delimited)
        return 1 <= point.row <= self.num_rows and \
        1 <= point.col <= self.num_cols
    
    def get(self, point): # [?] I don't think this function is used above? it's using the dictionary get method
        """
        If a stone's been placed on that point, gets you the color of that stone

        Args:
            point: a point of class Point

        Returns:
            Returns the content of a point: a Player (color) if a stone is on the that point, otherwise None
        """
        string = self._grid.get(point)
        if string is None: # this part is redundant but helps with clarity and complies with convention
            return None
        return string.color
    
    def get_go_string(self, point): # [?] this funciton isn't used yet
        """
        If a stone's been placed on that point, gets you string that stone is attached to

        Args:
            point: a point of class Point

        Returns:
            Returns the string that stone is a part of
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
