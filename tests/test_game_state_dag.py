import unittest

from games.game import GameState, KuhnPoker
from util.game_state_explorer import DAGExplorer


class TestGameStateDAG(unittest.TestCase):

    def test_add_edge(self):
        kuhn_poker = KuhnPoker()
        start_state = kuhn_poker.sample_start_state()
        next_state = kuhn_poker.apply_action(start_state, 0)

        game_state_dag = DAGExplorer(num_actions=2)
        game_state_dag.add_game_state_edge(start_state, next_state)

        print(game_state_dag.graph.edges)

    def test_successor_game_states(self):
        kuhn_poker = KuhnPoker()
        start_state = kuhn_poker.sample_start_state()
        next_state = kuhn_poker.apply_action(start_state, 0)

        game_state_dag = DAGExplorer(num_actions=2)
        game_state_dag.add_game_state_edge(start_state, next_state)

        for game_state in game_state_dag.get_successor_game_states(start_state):
            print(game_state)