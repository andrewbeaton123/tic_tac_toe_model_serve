
import numpy as np
from tic_tac_toe_game import TicTacToe

class PredictionAgent:
    def __init__(self, q_values):
        self.q_values = q_values

    def get_action(self, game_state: TicTacToe) -> int:
        # Assuming q_values is a dictionary where keys are game states (or their string representation)
        # and values are dictionaries of actions to Q-values.
        # The TicTacToe game state needs to be hashable to be used as a key.
        # If the q_values are stored with string representations of states, convert the current state.
        
        # For simplicity, let's assume the q_values keys are directly comparable to game_state objects
        # or a hashable representation of them.
        
        # If the game_state object itself is not hashable, you might need to convert it
        # to a hashable representation (e.g., a tuple of the board, or a string).
        # Based on how TicTacToe is used in app.py, it seems like it might be directly used as a key
        # or has a __hash__ method.
        
        state_key = game_state # Use the game_state object directly as the key

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
            if valid_moves:
                return np.random.choice(valid_moves)
            else:
                return -1 # No valid moves, game might be over
