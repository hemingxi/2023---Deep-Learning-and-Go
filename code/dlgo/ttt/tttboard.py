import copy

from dlgo.ttt.ttttypes import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveException(Exception):
    pass


BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
# Top left to lower right diagonal
DIAG_1 = (Point(1, 1), Point(2, 2), Point(3, 3))
# Top right to lower left diagonal
DIAG_2 = (Point(1, 3), Point(2, 2), Point(3, 1))


class Move:
    def __init__(self, point: Point = None, is_pass: bool = False, is_resign: bool = False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point: Point) -> 'Move':
        # First input of class method should be cls.
        return Move(point=point)

    @classmethod
    def pass_turn(cls) -> 'Move':
        # Passing isn't really part of tic-tac-toe
        return Move(is_pass=True)

    @classmethod
    def resign(cls) -> 'Move':
        return Move(is_resign=True)


class Board:
    def __init__(self):
        # Tic-tac-toe only has 3x3 board, so no need for these other parameters
        # self.num_rows = num_rows
        # self.num_cols = num_cols
        self._grid = {}

    def place(self, player: Player, point: Point) -> None:
        """
        Places down your x or o
        """
        assert self._grid.get(point) is None
        assert self.is_on_grid(point)
        self._grid[point] = player

    @staticmethod
    def is_on_grid(self, point: Point) -> bool:
        # Static methods are often used when a method is related to a class but doesn't need access to the instance-specific 
        # attributes or methods of the class.
        return 1 <= point.row <= BOARD_SIZE \
            and 1<= point.col <- BOARD_SIZE

    def get(self, point: Point) -> Player:
        return self._grid.get(point)


class GameState:
    def __init__(self, board: Board, next_player: Player, previous: 'GameState', last_move: Move):
        self.board = board
        self.next_player = next_player
        self.previous = previous
        self.last_move = last_move

    @classmethod
    def new_game(cls) -> 'GameState':
        return GameState(
            board=Board(),
            next_player=Player.x,  # Player x goes first
            previous=None,
            last_move=None
        )

    def apply_move(self, move: Move) -> 'GameState':
        # You don't need Player as input because you know who is playing.
        assert self.is_valid_move(move)
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(
            board=next_board,
            next_player=self.next_player.other,
            previous=self,
            last_move=move
        )

    def is_valid_move(self, move: Move) -> bool:
        if move.is_pass or move.is_resign:
            return True
        is_point_empty = self.board.get(move.point)
        return Board.is_on_grid(move.point) \
            and is_point_empty

    def legal_moves(self) -> list:
        """
        Returns a all the legal moves in a list containing Moves
        """
        moves = []
        for r in ROWS:
            for c in COLS:
                point = Point(r,c)
                if self.board.get(point) is None:
                    moves.append()

    def _has_3_in_a_row(self, player: Player) -> bool:
        # check rows, cols, and diagonals
        pass

    def is_over(self) -> bool:
        # if either player has 3 in a row, 
        # or all the points are filled (and no one has won)
        pass

    def winner(self) -> Player:
        """
        Returns the winner of the current game state if the game is over
        """
        pass

