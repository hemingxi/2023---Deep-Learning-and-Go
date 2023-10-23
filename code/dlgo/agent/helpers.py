from dlgo.gotypes import Point, Player
from dlgo.goboard_slow import Board

def is_point_an_eye(board: Board, point: Point, color: Player) -> bool:
    # eye has to be empty point:
    if board.get(point) is not None:
        return False
    
    # all adjacent points must be friendly stones
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):  # need to check if board is on grid here
            if board.get(neighbor) != color:
                return False
        
    corners = [
        Point(point.row - 1, point.row + 1),
        Point(point.row - 1, point.row - 1),
        Point(point.row + 1, point.row + 1),
        Point(point.row + 1, point.row - 1),
    ]

    # my attempt:
    # this is unnecessarily verbose, but it skips a few checks
    """
    diagonal_friendly_counter: int
    diagonal_opposite_or_empty_counter: int
    # if point is in middle of board, 3 out of 4 diagonal adjacent points needs to be friendy
    if (point.row not in (1, board.num_rows)) and (point.col not in (1, board.num_cols)):
        for diagonal_neighbor in diagonal_neighbors:
            if board.get(diagonal_neighbor) == color:
                diagonal_friendly_counter += 1
            else:
                diagonal_opposite_or_empty_counter += 1
            if diagonal_opposite_or_empty_counter > 1:
                return False
        return True
    # if point is on the edge
    elif (point.row in (1, board.num_rows)) ^ (point.col in (1, board.num_cols)):
        for diagonal_neighbor in diagonal_neighbors:
            if not board.is_on_grid(diagonal_neighbor):
                continue
            if board.get(diagonal_neighbor) == color:
                diagonal_friendly_counter += 1
            else:
                diagonal_opposite_or_empty_counter += 1
            if diagonal_opposite_or_empty_counter > 0:
                return False
        return True
    # if point is on the corner
    elif (point.row in (1, board.num_rows)) and (point.col in (1, board.num_cols)):
        for diagonal_neighbor in diagonal_neighbors:
            if not board.is_on_grid(diagonal_neighbor):
                continue
            if board.get(diagonal_neighbor) == color:
                diagonal_friendly_counter += 1
            else:
                diagonal_opposite_or_empty_counter += 1
            if diagonal_opposite_or_empty_counter > 0:
                return False
        return True
    """

    friendly_corners: int = 0
    off_grid_corners: int = 0

    for corner in corners:
        if not board.is_on_grid(corner):
            off_grid_corners += 1
        elif board.get(corner) == color:
            friendly_corners += 1
    if off_grid_corners == 0: # point is in middle
        return friendly_corners >= 3
    else: # point is on edge or corner
        return friendly_corners + off_grid_corners == 4