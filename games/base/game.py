from abc import ABC, abstractmethod

from games.base.state import GameState


class Game(ABC):

    @abstractmethod
    def get_start_state(self) -> GameState:
        pass

    @abstractmethod
    def apply_action(self, game_state: GameState, action: int) -> GameState:
        pass
