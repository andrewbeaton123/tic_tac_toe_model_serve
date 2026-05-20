import numpy as np
import logging

from pythonjsonlogger import jsonlogger
from typing import List
from fastapi import FastAPI, Depends
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from tic_tac_toe_game import TicTacToe
from tic_tac_toe_model_serve.prediction_agent import PredictionAgent


from tic_tac_toe_model_serve.auth import get_api_key
from tic_tac_toe_model_serve.schemas import predict_request, next_move
from tic_tac_toe_model_serve.middleware import log_request_performance
from tic_tac_toe_model_serve.valid_state_check import check_game_state_valid

from tic_tac_toe_model_serve.errors.error_class import NoValidMovesAvailable
from tic_tac_toe_model_serve.errors.error_handlers import no_valid_moves_available_handler

from tic_tac_toe_model_serve.dependencies import get_prediction_agent

#initialize the logger for training data capture 
logger = logging.getLogger("mlops_training_data")
handler = logging.StreamHandler()## using this enables azure to scrape the results from the standard out 
formatter = jsonlogger.JsonFormatter('%(asctime)s %(user_id)s %(board_state)s %(move)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# initialize the telemetry 
configure_azure_monitor()
app = FastAPI()

#show the dog the rabbit 
FastAPIInstrumentor.instrument_app(app)

app.add_exception_handler(NoValidMovesAvailable, no_valid_moves_available_handler)

# Add middleware
app.middleware("http")(log_request_performance)



def capture_training_data(user_id: str, board: List, move: int):
    # This JSON record lands in Log Analytics and is queryable via KQL
    logger.info("move_event", extra={'user_id': user_id, 'board_state': board, 'move': move})


@app.post("/next_move", response_model=next_move)
async def predict_next_move(request_data: predict_request,
                             api_key: str = Depends(get_api_key),
                             agent: PredictionAgent = Depends(get_prediction_agent)):

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("tic_tac_toe_q_learning_inference"):
        check_game_state_valid(np.reshape(request_data.game_state, (3, 3)))

        current_game = TicTacToe(request_data.current_player,
                                np.reshape(request_data.game_state, (3, 3)))


        move_next = agent.get_action(current_game)
        capture_training_data("User_id_not_set",request_data.game_state, move_next)
        pass
    return {"move": move_next}
