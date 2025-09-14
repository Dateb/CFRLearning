import random
from itertools import combinations_with_replacement
from typing import List

from games.base.game import GameState, Game


class OneDieDudo(Game):

    def __init__(self):
        self.possible_rolls = list(combinations_with_replacement([1, 2, 3, 4, 5, 6], 2))

    def sample_start_state(self) -> GameState:
        return self.create_start_state(random.randint(1, 6), random.randint(1, 6))

    def get_start_state(self) -> List[GameState]:
        return [self.create_start_state(roll[0], roll[1]) for roll in self.possible_rolls]

    def create_start_state(self, roll0: int, roll1: int) -> GameState:
        return GameState(
            public_state=f"{roll0}",
            private_state=f"{roll1}",
            active_player=0,
            num_actions=2,
        )

    def set_utility(self, game_state: GameState):
        pass

    def apply_action(self, game_state: GameState, action: int) -> GameState:
        pass

    def _get_num_claims(self, n: int, r: int) -> int:
        return (2 - n) * 6 + (6 - r) * n

game = OneDieDudo()
print(game.get_start_state())
