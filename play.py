from interfaces import *
from random_strategy import RandomStrategy
from verdecia_melikh import StrawHatStrategy, has_won, is_draw
from dummy_strategy import DummyStrategy
import time


def play_game():
    # Create a new board with numbers for height, width, and win-con
    board = Board(6, 7, 4)

    # instance for our strategy
    # choosing the color for the first move. (rules dictate that RED plays first)
    player_token = Token.RED

    count = 0
    while True:
        # Print the current state of the board
        print(board)
        print("-------")  # Helps with seeing different boards as the game progresses
        if player_token == Token.RED:
            strategy = StrawHatStrategy()
            # strategy = DummyStrategy()
            # chosen_column = int(input("chose a col starting from 0 to 6: "))
            start = time.time()
            chosen_column = strategy.play(board, player_token)
            end = time.time()
            # print("Temps de calcul: ", end - start)
            print(f"Random played col {chosen_column}")
        elif player_token == Token.YELLOW:
            # strategy = DummyStrategy()
            strategy = StrawHatStrategy()
            start = time.time()
            chosen_column = strategy.play(board, player_token)
            end = time.time()
            print("Temps de calcul: ", end - start)
            print(f"AI played col {chosen_column}")

        board.play(chosen_column, player_token)
        # Check for a win-con
        count += 1
        if has_won(board, player_token):
            print(board)  # To print the board showing the win
            print(f"Player {player_token.value} wins after {count} moves!")
            break

        # Check for a draw-con
        if is_draw(board):
            print(board)  # To print the board showing the draw
            print(f"It's a draw! after {count} moves")
            break

        # alternate between token colors for each turn
        if player_token == Token.RED:
            player_token = Token.YELLOW
        else:
            player_token = Token.RED


# Start the game
if __name__ == '__main__':
    play_game()
