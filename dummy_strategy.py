from verdecia_melikh import get_playable_columns, board_score
from interfaces import *
import copy
import random


def find_best_move(board, token):
    possible_moves = get_playable_columns(board)
    best_score = 0
    best_move = random.choice(possible_moves)
    for move in possible_moves:
        board_copy = copy.deepcopy(board)
        board_copy.play(move, token)
        score = board_score(board_copy, token)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


class DummyStrategy(Strategy):
    def authors(self) -> str:
        return "Boris Verdecia Echarte"

    def play(self, current_board: Board, your_token: Token) -> int:
        return find_best_move(current_board, your_token)
