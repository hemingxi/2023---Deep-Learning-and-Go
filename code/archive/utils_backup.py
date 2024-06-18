from dlgo import gotypes
from dlgo.goboard_fast import Move, Board
import numpy as np

# this backup utils worked with goboard and goboard_slow

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
 
def point_from_coords(coords):
    # Both index and find will work here. 
    # You need to add 1 because of python's 0 indexing and convering it back to 1 based indexing that we use in the Board class
    col = COLS.index(coords[0]) + 1 
    row = int(coords[1:])  # it could be something like A17, so you need to take the 1th position to the end
    return gotypes.Point(row=row, col=col)