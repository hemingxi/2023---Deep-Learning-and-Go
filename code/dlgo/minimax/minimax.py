import enum
import agent

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3

class MinimaxAgent(agent.Agent):
    def select_move(self, game_state):
        pass