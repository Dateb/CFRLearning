import numpy as np

from games.game import GameState
from util.game_state_explorer import GameStateExplorer
from util.information_set import InformationSet


class CFRSolver:

    def __init__(self, game_state_explorer: GameStateExplorer):
        self.info_sets = {}
        self.game_state_explorer = game_state_explorer

    def run(self, game_state: GameState, p0: float, p1: float) -> float:
        if game_state.is_terminal:
            return game_state.utility

        info_set = self.get_info_set(game_state)

        active_player_p = p0 if game_state.active_player == 0 else p1
        strategy = info_set.get_strategy(active_player_p)

        action_util = self.get_action_util(game_state, strategy, p0, p1)
        node_util = sum([strategy[i] * action_util[i] for i in range(game_state.num_actions)])

        # For each action, compute and accumulate counterfactual regret
        for i in range(game_state.num_actions):
            regret = action_util[i] - node_util
            info_set.regret_sum[i] += (p1 if game_state.active_player == 0 else p0) * regret

        return node_util

    def get_action_util(self, game_state: GameState, strategy: np.ndarray, p0: float, p1: float) -> np.ndarray:
        action_util = np.zeros(game_state.num_actions)
        i = 0
        for successor_game_state in self.game_state_explorer.get_successor_game_states(game_state):
            if game_state.active_player == 0:
                action_util[i] = -self.run(successor_game_state, p0 * strategy[i], p1)
            else:
                action_util[i] = -self.run(successor_game_state, p0, p1 * strategy[i])

            i += 1

        return action_util

    def get_info_set(self, game_state: GameState) -> InformationSet:
        if game_state.is_terminal:
            game_state_key = f"{game_state.public_state}{game_state.private_state}"
        else:
            game_state_key = game_state.public_state

        if game_state_key not in self.info_sets:
            self.info_sets[game_state_key] = InformationSet(game_state.num_actions)

        return self.info_sets[game_state_key]