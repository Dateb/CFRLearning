from abc import ABC, abstractmethod


class GameState(ABC):

    def __init__(self, active_player: int, num_actions: int):
        self.active_player = active_player
        self.num_actions = num_actions
        self.utility = 0
        self.id = f"{self.get_public_info()}/{self.get_private_info()}"
        self.is_terminal = self._is_terminal()
        self.is_stochastic = self._is_stochastic()

    def __eq__(self, other):
        return isinstance(other, GameState) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.id

    @abstractmethod
    def get_num_actions(self) -> int:
        pass

    @abstractmethod
    def get_public_info(self) -> str:
        pass

    @abstractmethod
    def get_private_info(self) -> str:
        pass

    @abstractmethod
    def _is_terminal(self) -> bool:
        pass

    @abstractmethod
    def _is_stochastic(self) -> bool:
        pass
