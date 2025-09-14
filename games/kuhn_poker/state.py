from typing import List

from games.base.state import GameState


class KuhnPokerState(GameState):

    def __init__(self, active_player: int, c0: int, c1: int, plays: List[int]):
        self.c0 = c0
        self.c1 = c1
        self.plays = plays

        self.is_terminal_pass = len(self.plays) > 1 and self.plays[-1] == 0
        self.is_double_bet = self.plays[-2:] == [1, 1]
        self.is_double_pass = self.plays[-2:] == [0, 0]

        num_actions = self.get_num_actions()
        super().__init__(active_player, num_actions)

    def get_num_actions(self) -> int:
        if self._is_stochastic():
            return 6
        return 0 if self.is_terminal_pass or self.is_double_bet else 2

    def get_public_info(self) -> str:
        player_card_value = str(self.c0) if self.active_player == 0 else str(self.c1)
        return f"{player_card_value}{self.plays}"

    def get_private_info(self) -> str:
        return str(self.c1) if self.active_player == 0 else str(self.c0)

    def _is_terminal(self) -> bool:
        return self.num_actions == 0

    def _is_stochastic(self) -> bool:
        return self.c0 == -1
    
    def _get_terminal_utility(self) -> float:
        utility = 0
        player_card = self.c0 if self.active_player == 0 else self.c1
        opponent_card = self.c1 if self.active_player == 0 else self.c0
        is_player_card_higher = player_card > opponent_card

        if self.is_terminal_pass:
            if self.is_double_pass:
                utility = 1 if is_player_card_higher else -1
            else:
                utility = 1
        if self.is_double_bet:
            utility = 2 if is_player_card_higher else -2

        return utility
