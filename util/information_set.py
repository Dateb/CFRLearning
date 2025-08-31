import numpy as np

class InformationSet:
    def __init__(self, num_actions: int):
        self.num_actions = num_actions
        self.regret_sum = np.zeros(num_actions)
        self.strategy = np.zeros(num_actions)
        self.strategy_sum = np.zeros(num_actions)

    def get_strategy(self, realization_weight: float) -> np.ndarray:
        self.strategy = self.regret_sum.clip(min=0)
        normalizing_sum = sum(self.strategy)

        if normalizing_sum > 0:
            self.strategy /= normalizing_sum
        else:
            self.strategy[:] = 1.0 / self.num_actions

        self.strategy_sum += realization_weight * self.strategy

        return self.strategy

    def get_average_strategy(self) -> np.ndarray:
        average_strategy = np.zeros(self.num_actions)
        normalizing_sum = sum(self.strategy_sum)

        if normalizing_sum > 0:
            average_strategy = self.strategy_sum / normalizing_sum
        else:
            average_strategy[:] = 1.0 / self.num_actions

        return average_strategy

    def __repr__(self):
        return f"{self.key}: {self.get_average_strategy()}"