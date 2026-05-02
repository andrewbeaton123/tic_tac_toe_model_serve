from numpy import ndarray
from tic_tac_toe_model_serve.errors.error_class import NoValidMovesAvailable


def  check_game_state_valid(game_state: ndarray):

    if 0 not in game_state:
        raise  NoValidMovesAvailable(game_state)
