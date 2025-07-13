import time
#

import numpy as np 


from fastapi import FastAPI, HTTPException, Request
from tic_tac_toe_game import TicTacToe
from tic_tac_toe_game.get_all_states import generate_all_states
from  tic_tac_learn.monte_carlo_learning.monte_carlo_tic_tac_2 import MonteCarloAgent
from src.load_q_values import load_q_values


from loguru import logger
from typing import List
from pathlib import Path
from pydantic import BaseModel
from fastapi.responses import JSONResponse


#auth imports
from fastapi.security import APIKeyHeader
from fastapi import Depends, Security
import os


#using local env
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
if not API_KEY :
    raise Exception("API KEY NOT LOADED")
API_KEY_NAME = "tic-tac-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        logger.debug(api_key_header)
        logger.debug(API_KEY)
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

app = FastAPI()
#setup loggins to create a new log file every 10mb
logger.add("logs/app.log", rotation="10 MB", serialize=True)  # JSON logs

class predict_request(BaseModel):
    current_player : int
    game_state : List

class next_move(BaseModel):
     move: int

pkl_file_path = Path("saved_q_values.pkl")

q_values = load_q_values(pkl_file_path)
agent = MonteCarloAgent(0.0, # setting epsilon to 0 makes it predict base don q values every time
                        generate_all_states())



agent.load_q_values(q_values)

@app.post("/next_move", response_model=next_move )
async def predict_next_move(request_data : predict_request,
                            api_key: str = Depends(get_api_key)) :
    
    logger.info("starting move predict")
    move_next = agent.get_action( TicTacToe(request_data.current_player, 
                                np.reshape(request_data.game_state, (3, 3))))
    logger.info(f"The move is {move_next}")
    return {"move": move_next}


@app.middleware("http")
async def log_request_performance(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info({
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "duration_ms": int(duration * 1000)
    })
    return response