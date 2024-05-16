from interfaces import *
import random
import copy

BIG_INT = 999999999999999


def has_won(board: Board, token: Token) -> bool:
    # Check rows
    for line_index in range(board.height):
        count = 0
        for column_index in range(board.width):
            if board.box(line_index, column_index) == token:
                count += 1
                if count == board.to_win:
                    return True
            else:
                count = 0
    # Check columns
    for column_index in range(board.width):
        count = 0
        for line_index in range(board.height):
            if board.box(line_index, column_index) == token:
                count += 1
                if count == board.to_win:
                    return True
            else:
                count = 0

    # Check diagonals using the function below
    for diagonal in board.diagonals():
        count = 0
        if len(diagonal) >= board.to_win:
            for curr_token in diagonal:
                if curr_token == token:
                    count += 1
                    if count == board.to_win:
                        return True
                else:
                    count = 0
    return False


def game_over(board):
    return has_won(board, Token.RED) or has_won(board, Token.YELLOW) or is_draw(board)


def is_draw(board: Board) -> bool:
    for line_index in range(board.height):
        for column_index in range(board.width):
            if board.box(line_index, column_index) == Token.EMPTY:
                return False
    return True


def get_playable_columns(board):
    return [index for index in range(board.width) if
            Token.EMPTY in board.column(index)]


def calculate_score(board, token_list, token, other_token):
    score = 0
    for j in range(len(token_list) - (board.to_win - 1)):
        window = token_list[j:j + board.to_win]
        if count_token(window, token) == board.to_win:
            score += 10000
        elif count_token(window, token) == board.to_win - 1 and count_token(window, Token.EMPTY) == 1:
            score += 1000
        elif count_token(window, token) == board.to_win - 2 and count_token(window, Token.EMPTY) == 2:
            score += 500
        elif count_token(window, other_token) == board.to_win - 1 and count_token(window, Token.EMPTY) == 1:
            score -= 8500
    return score


def board_score(board, token):
    other_token = Token.YELLOW
    if token == Token.YELLOW:
        other_token = Token.RED
    score = 0
    # take the center
    center_col = board.column(board.width // 2)
    center_tokens = count_token(center_col, token)
    score += 50 * center_tokens
    # horizontal score
    for i in range(board.height):
        row = board.line(i)
        score += calculate_score(board, row, token, other_token)
    # vertical score
    for i in range(board.width):
        column = board.column(i)
        score += calculate_score(board, column, token, other_token)
    # diagonal scores
    for diagonal in board.diagonals():
        if len(diagonal) >= board.to_win:
            score += calculate_score(board, diagonal, token, other_token)
    return score


def count_token(window, token):
    count = 0
    for w_token in window:
        if w_token == token:
            count += 1
    return count


def minimax(board, token, other_token, alpha, beta, depth, maximizing_player):
    moves = get_playable_columns(board)
    if depth == 0 or game_over(board):
        if has_won(board, token):
            return 0, BIG_INT
        elif has_won(board, other_token):
            return 0, -BIG_INT
        elif is_draw(board):
            return 0, 0
        return 0, board_score(board, token)
    if maximizing_player:
        best_score = float("-inf")
        best_move = random.choice(moves)
        for move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.play(move, token)
            score = minimax(board_copy, token, other_token, alpha, beta, depth - 1, False)[1]
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_move, best_score
    else:
        min_score = float("inf")
        best_move = random.choice(moves)
        for move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.play(move, other_token)
            score = minimax(board_copy, token, other_token, alpha, beta, depth - 1, True)[1]
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_move, min_score


class StrawHatStrategy(Strategy):
    DEPTH = 4

    def authors(self) -> str:
        return "Boris Verdecia - Othman Melikh"

    def play(self, current_board: Board, your_token: Token) -> int:
        maximizing = True
        other_token = Token.YELLOW
        if your_token == Token.YELLOW:
            other_token = Token.RED
            maximizing = False
        return minimax(current_board, your_token, other_token, float("-inf"), float("inf"), self.DEPTH, maximizing)[0]
