from itertools import permutations

from games.base.game import GameState, Game
from games.kuhn_poker.state import KuhnPokerState


class KuhnPoker(Game):

    def __init__(self):
        self.possible_deals = list(permutations([1, 2, 3], 2))

    def get_start_state(self) -> GameState:
        return KuhnPokerState(0, -1, -1, [])

    def apply_action(self, game_state: KuhnPokerState, action: int) -> GameState:
        if game_state.is_stochastic:
            c0, c1 = self.possible_deals[action]
            successor_game_state = KuhnPokerState(0, c0, c1, [])
        else:
            successor_game_state = KuhnPokerState(
                1 - game_state.active_player,
                game_state.c0,
                game_state.c1,
                game_state.plays + [action]
            )
        return successor_game_state
