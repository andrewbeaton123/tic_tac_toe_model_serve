from typing import List
from pydantic import BaseModel, Field, validator
from src.config_loader import ALLOWED_PLAYERS

class predict_request(BaseModel):
    current_player: int = Field(..., description="The current player.")
    game_state: List[int] = Field(..., min_items=9, max_items=9, description="A flat list of 9 integers representing the board (0=empty, 1=player 1, 2=player 2).")

    @validator('current_player')
    def validate_current_player(cls, v):
        vi = int(v)
        if vi not in ALLOWED_PLAYERS:
            raise ValueError(f"current_player must be one of {ALLOWED_PLAYERS}")
        return vi

    @validator('game_state')
    def validate_game_state_values(cls, v):
        if not all(item in [0, 1, 2] for item in v):
            raise ValueError('Each item in game_state must be 0, 1, or 2.')
        return v

class next_move(BaseModel):
     move: int
