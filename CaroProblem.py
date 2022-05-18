
from collections import namedtuple

import numpy as np
import random
import tkinter as tk


class CaroProblem():
    def __init__(self, h=10, v=10, k=4):
        self.h = h
        self.v = v
        self.k = k

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def actions(self, state):
        """Các động thái hợp lợi là bất kỳ hình vuông nào chưa được thực hiện."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Di chuyển bất hợp lệ không có hiệu lực
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(
                             board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Trả lại giá trị cho người chơi: 1 là thắng, -1 là thua, 0 nếu trường hợp khác."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """Một state là cuối cùng nếu nó thắng hoặc không có ô trống nào."""
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """Nếu 'X' thắng với nước đi này, trả về 1; nếu 'O' thắng trả về -1; khác trả về 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Trả về True nếu có một dòng di chuyển trên bảng cho người chơi."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n là số lần di chuyển trong hàng
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Bởi vì chúng ta đã đếm chính nó di chuyển hai lần
        return n >= self.k

    def play_game_with_ai(self, state, player_ai):
        """Chơi trò chơi di chuyển xen kẽ n người."""
        move = player_ai(self, state)
        state = self.result(state, move)
        return move


def random_player(game, state):
    """Một người chơi chọn một nước đi phù hợp một cách ngẫu nhiên."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def ai_player(game, state):
    return alpha_beta_search(state, game)

def alpha_beta_search(state, game, d=2, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


GameState = namedtuple('GameState', 'to_move, utility, board, moves')
