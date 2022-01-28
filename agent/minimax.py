import enum
import math
import random

import gotypes
from agent.base import Agent


MAX_SCORE = math.inf
MIN_SCORE = -1 * MAX_SCORE


class MinimaxAgentDepthPruning(Agent):
    def select_move(self, game_state):
        max_depth = 2

        best_so_far = MIN_SCORE
        best_move = game_state.legal_moves()[0]
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state, max_depth - 1, capture_diff)

            our_best_outcome = -1 * opponent_best_outcome

            if our_best_outcome > best_so_far:
                best_so_far = our_best_outcome
                best_move = possible_move
        return best_move


def best_result(game_state, max_depth, eval_fn) -> int:
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:
        return eval_fn(game_state)

    best_result_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        our_result = -1 * opponent_best_result
        if our_result > best_result_so_far:
            best_result_so_far = our_result
    return best_result_so_far


def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = gotypes.Point(r, c)
            color = game_state.board.get(p)
            if color == gotypes.Player.black:
                black_stones += 1
            elif color == gotypes.Player.white:
                white_stones += 1
    diff = black_stones - white_stones
    if game_state.next_player == gotypes.Player.black:
        return diff
    return -1 * diff
