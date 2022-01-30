import math

import agent.base
from MCTSNode import MCTSNode
from agent import naive
from gotypes import Player


class MCTSAgent(agent.base.Agent):
    def __init__(self, num_rounds: int = 100, temperature: int = 1.5):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_pct(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node: MCTSNode):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1
        best_child = None
        for child in node.children:
            score = uct_score(
                total_rollouts,
                child.num_rollouts,
                child.winning_pct(node.game_state.next_player),
                self.temperature)

            if score > best_score:
                best_score = score
                best_child = child
        return best_child


def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


def simulate_random_game(game_state):
    bots = {
        Player.black: naive.RandomBot(),
        Player.white: naive.RandomBot(),
    }
    while not game_state.is_over():
        bot_move = bots[game_state.next_player].select_move(game_state)
        game_state = game_state.apply_move(bot_move)
    return game_state.winner()