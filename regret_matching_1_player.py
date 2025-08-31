# Regret matching for RPS
from typing import List

import numpy as np

ROCK, PAPER, SCISSOR = 0, 1, 2
NUM_ACTIONS = 3

strategy_sum = [0.0] * NUM_ACTIONS
opponent_strategy = [0.4, 0.3, 0.3]

def get_strategy(regret_sum: List[float]):
    strategy = [0.0] * NUM_ACTIONS
    normalizing_sum = 0
    for i in range(NUM_ACTIONS):
        strategy[i] = np.clip(regret_sum[i], 0, np.inf)
        normalizing_sum += strategy[i]

    if normalizing_sum > 0:
        for i in range(NUM_ACTIONS):
            strategy[i] /= normalizing_sum
    else:
        strategy = [1 / NUM_ACTIONS] * NUM_ACTIONS

    return strategy

def train(n_iter: int):
    regret_sum = [0.0] * NUM_ACTIONS
    for i in range(n_iter):
        # Get regret-matched mixed-strategy actions
        my_action = int(np.random.choice(NUM_ACTIONS, 1, p=get_strategy(regret_sum)))
        other_action = int(np.random.choice(NUM_ACTIONS, 1, p=opponent_strategy))

        # Compute action utilities
        action_utility = [0.0] * NUM_ACTIONS
        action_utility[other_action] = 0
        action_utility[0 if other_action == NUM_ACTIONS - 1 else other_action + 1] = 1
        action_utility[NUM_ACTIONS - 1 if other_action == 0 else other_action - 1] = -1

        # Accumulate action regrets
        for i in range(NUM_ACTIONS):
            regret_sum[i] += action_utility[i] - action_utility[my_action]

        print(f"Total regret: {sum(regret_sum)}")

    print(regret_sum)
    print(get_strategy(regret_sum))

train(n_iter=1000)