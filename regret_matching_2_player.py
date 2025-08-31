# Regret matching for RPS
from typing import List

import numpy as np

NUM_ACTIONS = 3

class RegretMatchingPlayer:

    regrets: List[float] = [0.0] * NUM_ACTIONS
    strategy_sum: List[float] = [0.0] * NUM_ACTIONS

    def get_strategy(self):
        strategy = [0.0] * NUM_ACTIONS
        normalizing_sum = 0
        for i in range(NUM_ACTIONS):
            strategy[i] = np.clip(self.regrets[i], 0, np.inf)
            normalizing_sum += strategy[i]

        for i in range(NUM_ACTIONS):
            if normalizing_sum > 0:
                strategy[i] /= normalizing_sum
            else:
                strategy[i] = 1 / NUM_ACTIONS

            self.strategy_sum[i] += strategy[i]

        return strategy

    def get_average_strategy(self):
        return [s / sum(self.strategy_sum) for s in self.strategy_sum]

    def add_regret(self, action: int, opponent_action: int):
        # Compute action utilities
        action_utility = [0.0] * NUM_ACTIONS
        action_utility[opponent_action] = 0
        action_utility[0 if opponent_action == NUM_ACTIONS - 1 else opponent_action + 1] = 1
        action_utility[NUM_ACTIONS - 1 if opponent_action == 0 else opponent_action - 1] = -1

        # Accumulate action regrets
        for i in range(NUM_ACTIONS):
            self.regrets[i] += action_utility[i] - action_utility[action]

def train(n_iter: int):
    p1 = RegretMatchingPlayer()
    p2 = RegretMatchingPlayer()
    for i in range(n_iter):
        # Get regret-matched mixed-strategy actions
        action_p1 = int(np.random.choice(NUM_ACTIONS, 1, p=p1.get_strategy()))
        action_p2 = int(np.random.choice(NUM_ACTIONS, 1, p=p2.get_strategy()))

        p1.add_regret(action_p1, action_p2)
        p2.add_regret(action_p2, action_p1)

        # print(f"Total regret p1/p2: {sum(regret_sum_p1)}/{sum(regret_sum_p2)}")

    print(p1.regrets)
    print(p1.get_average_strategy())

train(n_iter=8000)