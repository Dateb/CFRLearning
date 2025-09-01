import random
from itertools import permutations
from typing import List

from games.base.game import GameState, Game
from games.kuhn_poker.state import KuhnPokerState


class KuhnPoker(Game):

    def __init__(self):
        self.possible_deals = list(permutations([1, 2, 3], 2))

    def sample_start_state(self) -> GameState:
        c0, c1 = random.choice(self.possible_deals)
        return self._create_start_state(c0, c1)

    def get_start_states(self) -> List[GameState]:
        return [self._create_start_state(deal[0], deal[1]) for deal in self.possible_deals]

    def _create_start_state(self, c0: int, c1: int) -> GameState:
        return KuhnPokerState(0, c0, c1, [])

    def set_utility(self, game_state: KuhnPokerState):
        player_card = game_state.c0 if game_state.active_player == 0 else game_state.c1
        opponent_card = game_state.c1 if game_state.active_player == 0 else game_state.c0
        is_player_card_higher = player_card > opponent_card

        if game_state.is_terminal_pass:
            if game_state.is_double_pass:
                game_state.utility = 1 if is_player_card_higher else -1
            else:
                game_state.utility = 1
        if game_state.is_double_bet:
            game_state.utility = 2 if is_player_card_higher else -2

    def apply_action(self, game_state: KuhnPokerState, action: int) -> GameState:
        successor_game_state = KuhnPokerState(
            1 - game_state.active_player,
            game_state.c0,
            game_state.c1,
            game_state.plays + [action]
        )

        self.set_utility(successor_game_state)
        return successor_game_state
