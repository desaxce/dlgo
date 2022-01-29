import math

from agent.base import Agent
from agent.helpers import capture_diff
from goboard import GameState
from gotypes import Player

MAX_SCORE = math.inf
MIN_SCORE = -1 * MAX_SCORE


def alpha_beta_best_result(game_state: GameState, max_depth: int, best_black: int, best_white: int, eval_fn) -> int:
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = alpha_beta_best_result(
            next_state, max_depth - 1,
            best_black, best_white,
            eval_fn)
        our_result = -1 * opponent_best_result

        if our_result > best_so_far:
            best_so_far = our_result
        if game_state.next_player == Player.white:
            if best_so_far > best_white:
                best_white = best_so_far
            outcome_for_black = -1 * best_so_far
            if outcome_for_black < best_black:
                return best_so_far
        elif game_state.next_player == Player.black:
            if best_so_far > best_black:
                best_black = best_so_far
            outcome_for_white = -1 * best_so_far
            if outcome_for_white < best_white:
                return best_so_far
    return best_so_far


class MinimaxAgentAlphaBeta(Agent):
    def select_move(self, game_state):
        max_depth = 3

        best_so_far = MIN_SCORE
        best_move = game_state.legal_moves()[0]
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = alpha_beta_best_result(next_state, max_depth - 1, MIN_SCORE, MIN_SCORE, capture_diff)

            our_best_outcome = -1 * opponent_best_outcome

            if our_best_outcome > best_so_far:
                best_so_far = our_best_outcome
                best_move = possible_move
        return best_move
