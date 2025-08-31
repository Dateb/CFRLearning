import random
from abc import ABC, abstractmethod
from itertools import permutations
from typing import List


class GameState:

    def __init__(self, public_state: str, private_state: str, active_player: int, num_actions: int):
        self.public_state = public_state
        self.private_state = private_state
        self.id = f"{self.public_state}/{self.private_state}"

        self.active_player = active_player
        self.num_actions = num_actions
        self.is_terminal = True if num_actions == 0 else False
        self.utility = 0

    def __eq__(self, other):
        return isinstance(other, GameState) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.id

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


class KuhnPoker(Game):

    def __init__(self):
        self.possible_deals = list(permutations([1, 2, 3], 2))

    def sample_start_state(self) -> GameState:
        c0, c1 = random.choice(self.possible_deals)
        return self.create_start_state(c0, c1)

    def get_start_states(self) -> List[GameState]:
        return [self.create_start_state(deal[0], deal[1]) for deal in self.possible_deals]

    def create_start_state(self, c0: int, c1: int) -> GameState:
        return GameState(
            public_state=f"{c0}",
            private_state=f"{c1}",
            active_player=0,
            num_actions=2,
        )

    def set_utility(self, game_state: GameState):
        player_card = int(game_state.public_state[0])
        opponent_card = int(game_state.private_state[0])
        history = game_state.public_state[1:]
        is_player_card_higher = player_card > opponent_card
        is_terminal_pass = history[-1] == 'p'
        is_double_bet = history[-2:] == "bb"
        if is_terminal_pass:
            if history == "pp":
                game_state.utility = 1 if is_player_card_higher else -1
            else:
                game_state.utility = 1
        elif is_double_bet:
            game_state.utility = 2 if is_player_card_higher else -2

    def apply_action(self, game_state: GameState, action: int) -> GameState:
        next_public_state = f"{game_state.private_state}{game_state.public_state[1:]}{'p' if action == 0 else 'b'}"
        is_terminal = self.is_terminal_public_state(next_public_state)
        successor_game_state = GameState(
            public_state=next_public_state,
            private_state=game_state.public_state[0],
            active_player=1-game_state.active_player,
            num_actions=0 if is_terminal else 2
        )
        self.set_utility(successor_game_state)
        return successor_game_state

    def is_terminal_public_state(self, public_state: str) -> bool:
        n_plays = len(public_state) - 1
        if n_plays > 1:
            is_terminal_pass = public_state[-1] == 'p'
            is_double_bet = public_state[-2:] == "bb"
            return is_terminal_pass or is_double_bet
        else:
            return False
