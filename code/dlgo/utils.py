from dlgo import gotypes
from dlgo.goboard_slow import Move, Board

COLS = 'ABCDEFGJKLMNOPQRST'
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
                  
