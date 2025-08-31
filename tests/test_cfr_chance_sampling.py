import time
import unittest

from games.game import KuhnPoker
from learners.cfr_chance_sampling import CFRSolver
from util.game_state_explorer import DAGExplorer


class TestCFRChanceSampling(unittest.TestCase):

    def test_kuhn_poker_nash_value(self):
        # Nash value in poker for the starting player is -1/18: https://en.wikipedia.org/wiki/Kuhn_poker
        KUHN_POKER_FIRST_PLAYER_NASH_VALUE = -1/18

        n_iterations = 1000000
        util = 0
        game = KuhnPoker()
        game_state_explorer = DAGExplorer(game)
        cfr = CFRSolver(game_state_explorer)
        for i in range(n_iterations):
            util += cfr.run(game.sample_start_state(), 1.0, 1.0)

        cfr_nash_value_estimate = util / n_iterations
        self.assertAlmostEqual(cfr_nash_value_estimate, KUHN_POKER_FIRST_PLAYER_NASH_VALUE, places=3)