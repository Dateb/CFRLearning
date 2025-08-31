import unittest

from games.game import GameState, KuhnPoker


class TestKuhnPoker(unittest.TestCase):

    def test_is_terminal_state(self):
        kuhn_poker = KuhnPoker()
        start_state = kuhn_poker.sample_start_state()
        single_pass_state = GameState(
            public_state="1p",
            private_state="2",
            active_player=1
        )
        double_pass_state = GameState(
            public_state="1pp",
            private_state="2",
            active_player=0
        )
        self.assertFalse(kuhn_poker.is_terminal_public_state(start_state))
        self.assertFalse(kuhn_poker.is_terminal_public_state(single_pass_state))
        self.assertTrue(kuhn_poker.is_terminal_public_state(double_pass_state))

    def test_get_utility(self):
        kuhn_poker = KuhnPoker()
        losing_double_pass_state = GameState(
            public_state="1pp",
            private_state="2",
            active_player=0,
        )
        winning_double_pass_state = GameState(
            public_state="2pp",
            private_state="1",
            active_player=0,
        )
        bet_pass_state = GameState(
            public_state="2bp",
            private_state="3",
            active_player=0,
        )
        pass_bet_pass_state = GameState(
            public_state="3pbp",
            private_state="2",
            active_player=0,
        )
        losing_pass_bet_bet_state = GameState(
            public_state="1pbb",
            private_state="2",
            active_player=0,
        )
        winning_pass_bet_bet_state = GameState(
            public_state="2pbb",
            private_state="1",
            active_player=1,
        )
        self.assertEqual(kuhn_poker.set_utility(losing_double_pass_state), -1)
        self.assertEqual(kuhn_poker.set_utility(winning_double_pass_state), 1)
        self.assertEqual(kuhn_poker.set_utility(bet_pass_state), 1)
        self.assertEqual(kuhn_poker.set_utility(pass_bet_pass_state), 1)
        self.assertEqual(kuhn_poker.set_utility(losing_pass_bet_bet_state), -2)
        self.assertEqual(kuhn_poker.set_utility(winning_pass_bet_bet_state), 2)
