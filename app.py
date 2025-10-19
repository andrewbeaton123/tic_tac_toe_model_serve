import numpy as np

from fastapi import FastAPI, Depends
from tic_tac_toe_game import TicTacToe
from src.prediction_agent import PredictionAgent
from src.load_q_values import load_q_values

from pathlib import Path

from src.auth import get_api_key
from src.schemas import predict_request, next_move
from src.middleware import log_request_performance
from src.logging_config import logger
from src.valid_state_check import check_game_state_valid
from src.config_loader import Q_VALUES_PATH


from src.config_loader import Q_VALUES_PATH

from src.errors.error_class import NoValidMovesAvailable
from src.errors.error_handlers import no_valid_moves_available_handler

app = FastAPI()

app.add_exception_handler(NoValidMovesAvailable, no_valid_moves_available_handler)

# Add middleware
app.middleware("http")(log_request_performance)



from src.dependencies import get_prediction_agent

@app.post("/next_move", response_model=next_move)
async def predict_next_move(request_data: predict_request,
                             api_key: str = Depends(get_api_key),
                             agent: PredictionAgent = Depends(get_prediction_agent)):
    
    check_game_state_valid(np.reshape(request_data.game_state, (3, 3)))

    current_game = TicTacToe(request_data.current_player,
                            np.reshape(request_data.game_state, (3, 3)))
    
    
    move_next = agent.get_action(current_game)
    return {"move": move_next}
