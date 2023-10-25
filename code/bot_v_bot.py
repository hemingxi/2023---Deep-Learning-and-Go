from dlgo.agent import naive, base, helpers
from dlgo import goboard_slow  # change this to goboard once you implement hashing -> doesn't seem like it's much faster??
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time

def main():
    board_size = 19
    game = goboard_slow.GameState.new_game(board_size)
    bots ={
        gotypes.Player.black: naive.RandomBot(),
        gotypes.Player.white: naive.RandomBot(),
    }

    n=0
    while not game.is_over():
        start_time = time.time()
        time.sleep(0)

        # print(chr(27) + "[2J") # clear screen
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

        end_time = time.time()
        print(f"Move: {n} Elapsted time {end_time - start_time}s")  # takes 1.6s per turn by around turn 70
        n += 1


if __name__ == '__main__':
    main()
