from abc import ABC, abstractmethod
from typing import Iterable

import networkx as nx

from games.game import GameState, Game


class GameStateExplorer(ABC):

    def __init__(self, game: Game):
        self.game = game

    @abstractmethod
    def get_successor_game_states(self, game_state: GameState) -> Iterable[GameState]:
        pass

class LazyExplorer(GameStateExplorer):

    def __init__(self, game: Game):
        super().__init__(game)

    def get_successor_game_states(self, game_state: GameState) -> Iterable[GameState]:
        return [self.game.apply_action(game_state, i) for i in range(game_state.num_actions)]


class DAGExplorer(GameStateExplorer):

    def __init__(self, game: Game):
        super().__init__(game)
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        for start_state in self.game.get_start_states():
            self.add_children_to_game_state(start_state)

    def add_children_to_game_state(self, game_state: GameState):
        if game_state.is_terminal:
            return

        for i in range(game_state.num_actions):
            successor_game_state = self.game.apply_action(game_state, i)
            self.add_game_state_edge(game_state, successor_game_state)
            self.add_children_to_game_state(successor_game_state)

    def add_game_state_edge(self, parent_game_state: GameState, child_game_state: GameState):
        self.graph.add_edge(parent_game_state, child_game_state)

    def get_successor_game_states(self, game_state: GameState) -> Iterable[GameState]:
        return self.graph.successors(game_state)


