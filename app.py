import numpy as np

from fastapi import FastAPI, Depends
from tic_tac_toe_game import TicTacToe
from tic_tac_toe_model_serve.prediction_agent import PredictionAgent


from tic_tac_toe_model_serve.auth import get_api_key
from tic_tac_toe_model_serve.schemas import predict_request, next_move
from tic_tac_toe_model_serve.middleware import log_request_performance
from tic_tac_toe_model_serve.valid_state_check import check_game_state_valid

from tic_tac_toe_model_serve.errors.error_class import NoValidMovesAvailable
from tic_tac_toe_model_serve.errors.error_handlers import no_valid_moves_available_handler

from tic_tac_toe_model_serve.dependencies import get_prediction_agent
app = FastAPI()

app.add_exception_handler(NoValidMovesAvailable, no_valid_moves_available_handler)

# Add middleware
app.middleware("http")(log_request_performance)




@app.post("/next_move", response_model=next_move)
async def predict_next_move(request_data: predict_request,
                             api_key: str = Depends(get_api_key),
                             agent: PredictionAgent = Depends(get_prediction_agent)):

    check_game_state_valid(np.reshape(request_data.game_state, (3, 3)))

    current_game = TicTacToe(request_data.current_player,
                            np.reshape(request_data.game_state, (3, 3)))


    move_next = agent.get_action(current_game)
    return {"move": move_next}
