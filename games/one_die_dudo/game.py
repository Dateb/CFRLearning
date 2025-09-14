import random
from itertools import combinations_with_replacement
from typing import List

from games.base.game import GameState, Game
from games.one_die_dudo.state import OneDieDudoState, Claim


class OneDieDudo(Game):

    def __init__(self):
        self.possible_rolls = list(combinations_with_replacement([1, 2, 3, 4, 5, 6], 2))

    def get_start_state(self) -> GameState:
        return OneDieDudoState(0, -1, -1, [])

    def set_utility(self, game_state: GameState):
        pass

    def apply_action(self, game_state: OneDieDudoState, action: int) -> GameState:
        if game_state.is_stochastic:
            r0, r1 = self.possible_rolls[action]
            successor_game_state = OneDieDudoState(0, r0, r1, [])
        else:
            previous_claim = game_state.claim_history[-1]
            if action == game_state.num_actions - 1:
                next_claim = Claim(-1, -1, is_doubting=True)
            else:
                next_claim = self.action_to_claim(previous_claim, action)
            successor_game_state = OneDieDudoState(
                1 - game_state.active_player,
                game_state.r0,
                game_state.r1,
                game_state.claim_history + [next_claim]
            )

            self.set_utility(successor_game_state)

        return successor_game_state

    def action_to_claim(self, previous_claim: Claim, action: int) -> Claim:
        claim_increase = action + 1
        next_rank = (previous_claim.rank + claim_increase) % 6

        next_number = claim_increase // 6
        if (claim_increase % 6) > (6 - previous_claim.rank):
            next_number += 1

        return Claim(number=next_number, rank=next_rank, is_doubting=False)




game = OneDieDudo()
print(game.get_start_state())
