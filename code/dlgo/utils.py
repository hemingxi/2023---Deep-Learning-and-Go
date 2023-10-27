from dlgo import gotypes
from dlgo.goboard import Move, Board
import numpy as np

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '.',
    gotypes.Player.black: 'x',
    gotypes.Player.white: 'o',
}

def print_move(player, move: Move) -> None:
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{player} {move_str}')

def print_board(board: Board) -> None:
    for row in range(board.num_rows, 0, -1):  # lower left corner is A1
        bump = " " if row <= 9 else ""
        line = []
        for col in range (1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row, col))
            line.append(STONE_TO_CHAR[stone])
            
        print(f"{bump}{row}{''.join(line)}")
    
    print(f"    {''.join(COLS[:board.num_cols])}")
                  
class MoveAge():
    def __init__(self, board):
        self.move_ages = - np.ones((board.num_rows, board.num_cols))

    def get(self, row, col):
        return self.move_ages[row, col]

    def reset_age(self, point):
        self.move_ages[point.row - 1, point.col - 1] = -1

    def add(self, point):
        self.move_ages[point.row - 1, point.col - 1] = 0

    def increment_all(self):
        self.move_ages[self.move_ages > -1] += 1