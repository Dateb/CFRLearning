from abc import ABC, abstractmethod
from typing import List

from games.base.state import GameState


class Game(ABC):

    @abstractmethod
    def sample_start_state(self) -> GameState:
        pass

    @abstractmethod
    def get_start_states(self) -> List[GameState]:
        pass

    @abstractmethod
    def set_utility(self, game_state: GameState):
        pass

    @abstractmethod
    def apply_action(self, game_state: GameState, action: int) -> GameState:
        pass
