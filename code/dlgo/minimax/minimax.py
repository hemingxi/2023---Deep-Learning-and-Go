import enum
import agent
from ttt import *  # GameState, Move
import random


class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


class MinimaxAgent(agent.Agent):

    def select_move(self, game_state: GameState) -> Move:
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state)
            our_best_outcome = reverse_game_outcome(opponent_best_outcome)
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:  # if winning_moves is not None
            return random.choice(winning_moves)
        elif draw_moves:
            return random.choice(draw_moves)
        else:
            return random.choice(losing_moves)


def best_result(game_state: GameState) -> GameResult:
    if game_state.is_over():
        # this code generalizes to other games. 
        # in tic-tac-toe if the game_state.is_over() and you played and won on the previous move, 
        # then game_state.next_player will be always be the other player
        # so only the last condition will ever activate
        # in other games, if opponent resigns, then it will be your move and you are the winner
        if game_state.winner() == game_state.next_player:
            return GameResult.win 
        elif game_state.winner() == None:
            return GameResult.draw
        else:
            return GameResult.loss


def reverse_game_outcome(game_result: GameResult) -> GameResult:
    assert game_result is not None
    if game_result == GameResult.win:
        return GameResult.loss
    if game_result == GameResult.loss:
        return GameResult.win
    return GameResult.draw