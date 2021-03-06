import random

from goboard import GameState
from gotypes import Player


class MCTSNode(object):
    def __init__(self, game_state: GameState, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        self.children: [MCTSNode] = []
        self.unvisited_moves = game_state.legal_moves()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        next_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(next_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner: Player):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_pct(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)
