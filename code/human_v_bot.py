from dlgo.agent import naive
from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
# from six.moves import input


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots ={
        gotypes.Player.white: naive.RandomBot(),
    }

    while not game.is_over():
        print_board(game.board)

        # you could add a check here to check the current player
        print("Please select a point on the board, or 'resign' or 'pass'")
        human_move_input = input()
        if human_move_input == 'resign':
            human_move = goboard.Move.resign()
        elif human_move_input == 'pass':
            human_move = goboard.Move.pass_turn()
        else:
            human_move_coord = point_from_coords(human_move_input)
            if not game.board.is_on_grid(human_move_coord):
                print(f"That move is off the board. The board size is {board_size}")
                continue
            human_move = goboard.Move.play(human_move_coord)
            if not game.is_valid_move(human_move):
                print(f"That is an invalid move. Please select an empty square that does not self-capture or violoate ko.")
                continue
        
        print(chr(27) + "[2J") # clear screen
        print_move(game.next_player, human_move)
        game = game.apply_move(human_move)

        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()
    # cProfile.run("main()")