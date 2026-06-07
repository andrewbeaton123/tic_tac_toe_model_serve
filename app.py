import numpy as np

from fastapi import FastAPI, Depends, HTTPException
from mlflow.pyfunc import PyFuncModel

from tic_tac_toe_model_serve.auth import get_api_key
from tic_tac_toe_model_serve.schemas import predict_request, next_move
from tic_tac_toe_model_serve.middleware import log_request_performance
from tic_tac_toe_model_serve.valid_state_check import check_game_state_valid

from tic_tac_toe_model_serve.errors.error_class import NoValidMovesAvailable
from tic_tac_toe_model_serve.errors.error_handlers import no_valid_moves_available_handler

from tic_tac_toe_model_serve.dependencies import get_model

app = FastAPI()

app.add_exception_handler(NoValidMovesAvailable, no_valid_moves_available_handler)

app.middleware("http")(log_request_performance)


@app.post("/next_move", response_model=next_move)
async def predict_next_move(request_data: predict_request,
                             api_key: str = Depends(get_api_key),
                             model: PyFuncModel = Depends(get_model)):

    check_game_state_valid(np.reshape(request_data.game_state, (3, 3)))

    model_input = [{
        "current_player": request_data.current_player,
        "game_state": request_data.game_state,
    }]
    try:
        result = model.predict(model_input)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"move": result["action"]}


@app.get("/health")
async def health():
    return {"status": "ok"}
