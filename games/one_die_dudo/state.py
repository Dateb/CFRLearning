from typing import List

from games.base.state import GameState

class Claim:

    def __init__(self, number: int, rank: int, is_doubting: bool):
        self.number = number
        self.rank = rank
        self.is_doubting = is_doubting
        self.n_better_claims = (2 - number) * 6 + (6 - rank)

class OneDieDudoState(GameState):

    def __init__(self, active_player: int, r0: int, r1: int, claim_history: List[Claim]):
        self.r0 = r0
        self.r1 = r1
        self.claim_history = claim_history

        num_actions = self.get_num_actions()
        super().__init__(active_player, num_actions)

    def get_num_actions(self) -> int:
        if self._is_terminal():
            return 0

        if self._is_stochastic():
            return 6 * 6

        if not self.claim_history:
            return 2 * 6

        best_claim = self.claim_history[-1]
        return best_claim.n_better_claims + 1

    def get_public_info(self) -> str:
        player_roll_value = str(self.r0) if self.active_player == 0 else str(self.r1)
        return f"{player_roll_value}{self.claim_history}"

    def get_private_info(self) -> str:
        return str(self.r1) if self.active_player == 0 else str(self.r0)

    def _is_terminal(self) -> bool:
        return self.claim_history[-1].is_doubting if self.claim_history else False

    def _is_stochastic(self) -> bool:
        return self.r0 == -1
