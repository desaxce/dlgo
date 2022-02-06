import math

from agent.base import Agent
from MCTSNode import MCTSNode
from agent import naive
from agent.naive_fast import FastRandomBot
from gotypes import Player


class MCTSAgent(Agent):
    def __init__(self, num_rounds: int = 100, temperature: int = 1.5):
        Agent.__init__(self)
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
        # Polite strategy to resign when winning probability < 10%.
        # Commented out to generate games.
        # if best_pct < 0.1:
        #     return Move.resign()
        return best_move

    def select_child(self, node: MCTSNode):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        for child in node.children:
            win_pct = child.winning_pct(node.game_state.next_player)
            exploration = math.sqrt(log_rollouts / child.num_rollouts)
            score = win_pct + self.temperature * exploration

            if score > best_score:
                best_score = score
                best_child = child
        return best_child


# Not used because we rather refactor the log of rollouts outside this function
def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


def simulate_random_game(game_state):
    bots = {
        Player.black: FastRandomBot(),
        Player.white: FastRandomBot(),
    }
    while not game_state.is_over():
        bot_move = bots[game_state.next_player].select_move(game_state)
        game_state = game_state.apply_move(bot_move)
    return game_state.winner()
