import unittest

from games.kuhn_poker.game import KuhnPoker
from learners.cfr_chance_sampling import CFRSolver
from util.game_state_explorer import DAGExplorer


class TestCFRChanceSampling(unittest.TestCase):

    def test_kuhn_poker_nash_value(self):
        # Nash value in poker for the starting player is -1/18: https://en.wikipedia.org/wiki/Kuhn_poker
        KUHN_POKER_FIRST_PLAYER_NASH_VALUE = -1/18

        n_iterations = 420000
        game = KuhnPoker()
        game_state_explorer = DAGExplorer(game)
        cfr = CFRSolver(game_state_explorer, n_iterations, 0.5)
        nash_value_estimate = cfr.run()

        self.assertAlmostEqual(nash_value_estimate, KUHN_POKER_FIRST_PLAYER_NASH_VALUE, places=5)