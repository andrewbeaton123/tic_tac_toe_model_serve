
import numpy as np
from tic_tac_toe_game import TicTacToe

class PredictionAgent:
    def __init__(self, q_values):
        self.q_values = q_values

    def _get_state(self, env: TicTacToe) -> tuple:
        """
        Gets the current state of the environment as a hashable tuple.
        """
        return tuple(int(x) for x in env.board.reshape(-1))

    def get_action(self, game_state: TicTacToe) -> int:
        
        

        state_key = self._get_state(game_state)

        if state_key in self.q_values:
            actions_q_values = self.q_values[state_key]
            # Find the action with the maximum Q-value
            best_action = max(actions_q_values, key=actions_q_values.get)
            return best_action
        else:
            # This case should ideally not happen if all states are covered in q_values.
            # For now, let's return a random valid move if the state is not found.
            # In a real scenario, you might want to log this or handle it more robustly.
            valid_moves = game_state.get_valid_moves()
            if len(valid_moves) > 0:
                return np.random.choice(np.array(valid_moves))
            else:
                return -1 # No valid moves, game might be over
