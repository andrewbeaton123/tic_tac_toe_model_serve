

from src.errors.error_class import NoValidMovesAvailable
from typing import List

def  check_game_state_valid(game_state: List):

    if 0 not in game_state:
        raise  NoValidMovesAvailable(game_state)
    