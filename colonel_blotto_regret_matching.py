class Game:
    def __init__(self):
        self.pure_strategies = []
        S = 5
        for i in range(S + 1):
            for j in range(S + 1):
                for k in range(S + 1):
                    if i + j + k == S:
                        self.pure_strategies.append((i, j, k))

        self.n_actions = len(self.pure_strategies)
        print(self.pure_strategies)

    def get_utility(self, player_strategy_id, opponent_strategy_id):
        player_strategy = self.pure_strategies[player_strategy_id]
        opponent_strategy = self.pure_strategies[opponent_strategy_id]

        player_n_battlefields_won = 0
        opponen_n_battlefields_won = 0
        for i in range(len(player_strategy)):
            if player_strategy[i] > opponent_strategy[i]:
                player_n_battlefields_won += 1
            if opponent_strategy[i] > player_strategy[i]:
                opponen_n_battlefields_won += 1

        if player_n_battlefields_won > opponen_n_battlefields_won:
            return 1
        if opponen_n_battlefields_won > player_n_battlefields_won:
            return -1
        return 0


# Regret matching for RPS
from typing import List

import numpy as np

class RegretMatchingPlayer:

    def __init__(self, game: Game):
        self.game = game
        self.n_actions = game.n_actions
        self.regrets = [0.0] * self.n_actions
        self.strategy_sum = [0.0] * self.n_actions

    def get_strategy(self):
        strategy = [0.0] * self.n_actions
        normalizing_sum = 0
        for i in range(self.n_actions):
            strategy[i] = np.clip(self.regrets[i], 0, np.inf)
            normalizing_sum += strategy[i]

        for i in range(self.n_actions):
            if normalizing_sum > 0:
                strategy[i] /= normalizing_sum
            else:
                strategy[i] = 1 / self.n_actions

            self.strategy_sum[i] += strategy[i]

        return strategy

    def get_average_strategy(self):
        return [s / sum(self.strategy_sum) for s in self.strategy_sum]

    def add_regret(self, action: int, opponent_action: int):
        action_utility = [self.game.get_utility(i, opponent_action) for i in range(self.n_actions)]

        # Accumulate action regrets
        for i in range(self.n_actions):
            self.regrets[i] += action_utility[i] - action_utility[action]

def train(n_iter: int):
    game = Game()
    p1 = RegretMatchingPlayer(game)
    p2 = RegretMatchingPlayer(game)
    for i in range(n_iter):
        # Get regret-matched mixed-strategy actions
        action_p1 = int(np.random.choice(game.n_actions, 1, p=p1.get_strategy()))
        action_p2 = int(np.random.choice(game.n_actions, 1, p=p2.get_strategy()))

        p1.add_regret(action_p1, action_p2)
        p2.add_regret(action_p2, action_p1)

        # print(f"Total regret p1/p2: {sum(regret_sum_p1)}/{sum(regret_sum_p2)}")

    print(p1.regrets)
    avg_strategy = p1.get_average_strategy()
    print({game.pure_strategies[i]: avg_strategy[i] for i in range(len(avg_strategy))})

train(n_iter=8000)