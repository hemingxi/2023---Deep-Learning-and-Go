import copy
from dlgo.gotypes import Player, Point
from typing import Union, Tuple
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to run")
        return result
    return wrapper


class Move():
    def __init__(self, point = None, is_pass = False, is_resign = False):
        #typically you would not create a Move directly,
        # but rather construct an instance by calling the 3 class methods: play, pass_turn, or resign
        assert (point is not None) ^ is_pass ^ is_resign # this is asserting that only 1 or all 3 has to be true
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod # these do not operate on the instance, but rather the class method directly
    def play(cls, point: Point) -> Point:
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
        self.stones = set(stones) # this uses the set data type and removes duplicates. Each stone is a Point
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point) # self.liberties is a set

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones # union the two sets
        return GoString(
            self.color, # color
            combined_stones, # stones
            (self.liberties | go_string.liberties) - combined_stones # liberties
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
        # I'm assuming grid is a dictionary mapping points to their GoStrings. 
        # When you call _grid.get(point) you get the string-of-stones that that point is attached to

    def place_stone(self, player, point):
        """
        This method places a stone down

        Args:
            player: Type Player (black or white) that is placing the stone
            point: where on the grid the player is placing the stone

        Returns:
            Doesn't return anything, modifies _grid directly
        """
        assert self.is_on_grid(point) # point exists on grid
        assert self._grid.get(point) is None # check that there's not already a stone there. 
        # _grid.get() returns the string of the stone that's there, or None if it's empty
        
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties =[]

        for neighbor in point.neighbors(): # we defined this in our gotypes.py, point.neighbors returns the 4 points surrounding the input point
            if not self.is_on_grid(neighbor):
                continue # if the neighboring point you are checking is off the grid, then continue the loop no need to do anything else
            
            # get the liberties and neighboring strings of this point
            neighbor_string = self._grid.get(neighbor) # grid is a dict mapping points to their GoStrings, neighbor is Point type
            if neighbor_string is None: # this is the GoString type we defined earlier
                # if neighbor_string is None, that means it's not already part of a GoString, meaning it is empty
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            elif neighbor_string.color == player.other: # you ahvet to add this condition otherwise you'll try to remove liberties of an empty board
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

        # this block needs to be outside the loop, 
        # because only after looping through all the neighbors do you have a proper list of liberties
        new_string = GoString(player, [point], liberties) # make a new GoString with only the one point
        for same_color_string in adjacent_same_color: # add it to all existing strings that it's next to
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones: # update all the points in this combined string 
            self._grid[new_string_point] = new_string 
        for other_color_string in adjacent_opposite_color: # remove liberties from opposing strings
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color: # capture any strings with no liberties left
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point):
        # the grid will go from 1 to num_rows (not 0 delimited)
        return 1 <= point.row <= self.num_rows and \
        1 <= point.col <= self.num_cols
    
    def get(self, point: Point) -> Player: # [?] I don't think this function is used above? it's using the dictionary get method
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
    
    def get_go_string(self, point) -> GoString: # [?] this funciton isn't used yet
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
    
    def _remove_string(self, string): # underscore indicates private function not to be used outside of this class
        for point in string.stones:
            # stones might gain liberties after capture
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:  # don't want to add liberties to itself that string is getting deleted, 
                # because it no longer exists
                    neighbor_string.add_liberty(point)

            self._grid[point] = None # pop this at the end is the correct order
        

class GameState():
    """
    This knows about:
       the board position, 
       the next player, 
       the previous game state, 
       and the last move

    Args:
        board: the current board state
        next_player: 
        previous_state:
        last_move:
    """
    def __init__(self, board: Board, next_player: Player, previous: 'GameState', move: Move):
        self.board = board # class Board
        self.next_player = next_player # enum Player
        self.previous_state = previous # class GameState, this points to the previous GameState
        self.last_move = move # class Move (play, pass, or resign)

    def apply_move(self, move: Move) -> 'GameState': # move is from the Move class, and could be play, pass or resign
        """
        Args:
            move: Type Move (play, pass, or resign) to be applied
        Returns:
            Returns new game state after applying move
        """
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point) # self.next_player.other gives you the current player
        else:
            next_board = self.board
        return GameState(
            next_board, 
            self.next_player.other, 
            self,
            move
        )

    @classmethod
    def new_game(cls, board_size: Union[int, tuple]) -> 'GameState': # this is a forward reference string, otherwise the linter says type not defined
        """
        Args:
            board_size: could be int or tuple
        Returns:
            Returns new game state with no stones placed
        """
        if isinstance(board_size, int):
            # this gives flexibility to define board size as either 19, or (19,19)
            board_size = (board_size, board_size) # create a tuple
        board = Board(*board_size)
        return GameState(
            board,
            Player.black, # black goes first
            None,
            None
        )
    
    def is_over(self) -> bool:
        if self.last_move is None: # check for edge case of being a new game
            return False
        if self.last_move.is_resign:
            return True
        
        second_last_move = self.previous_state.last_move
        if second_last_move is None: # check for edge case of first move in a new game
            return False
        return self.last_move.is_pass and second_last_move.is_pass
    
    # check 3 rules:
    # point you want to play is empty
    # check move is not self_capture
    # check that move does not violate ko - returns to previous board state

    def is_move_self_capture(self, player: Player, move: Move) -> bool:
        if not move.is_play: # if they pass or resign, it is not a self capture
            return False
        # my attempt:
        # does it work? no, because the apply_move calls play_stone which does not check for self capture
        # so the stones will still be on there
        # new_state = self.apply_move(Move)
        # return new_state.board.get_go_string(move.point) is None
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        return next_board.get_go_string(move.point).num_liberties == 0
    
    @property
    def situation(self) -> Tuple[Player, Board]:
        return(self.next_player, self.board)

    def does_move_violate_ko(self, player: Player, move: Move) -> bool: 
        # my attempt 1:
        # it does not work because you need to check the situation (player and board)
        # next_game_state = copy.deepcopy(self)
        # next_game_state.apply_move(move)
        # game_state_iterate = next_game_state.previous_state
        # while game_state_iterate is not None:
        #     if next_game_state.board == game_state_iterate.board:
        #         return True
        #     game_state_iterate = game_state_iterate.previous_state
        if not move.is_play:
            return False # skip all the checks if they pass or resign
        # my attempt 2:
        # might not be good to deepcopy the GameState object, because it points to other objects. It's too much overhead
        # next_game_state = copy.deepcopy(self)
        # next_game_state.apply_move(move)
        # past_state = next_game_state.previous_state
        # while past_state is not None:
        #     if next_game_state.situation == past_state.situation:
        #         return True
        #     past_state = past_state.previous_state
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        past_state = self.previous_state  # can start with self.previous because after you place the stone it can't possibly be equal the current state
        while past_state is not None:
            if past_state.situation == (player.other, next_board):  # you can define next_situation = (player.other, next_board) for readbility
                return True
            past_state = past_state.previous_state
        return False
    
    # @timing_decorator
    def is_valid_move(self, move: Move) -> bool:
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        is_point_empty = self.board.get(move.point) is None
        return (
            is_point_empty and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))
    