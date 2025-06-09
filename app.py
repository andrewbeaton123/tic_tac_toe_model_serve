from fastapi import FastAPI, HTTPException
from tic_tac_toe_game import TicTacToe
from tic_tac_toe_game.get_all_states import generate_all_states
from  tic_tac_learn.monte_carlo_learning.monte_carlo_tic_tac_2 import MonteCarloAgent
from src.load_q_values import load_q_values
import numpy as np 

from loguru import logger
from typing import List
from pathlib import Path
from pydantic import BaseModel


app = FastAPI()


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
async def predict_next_move(request_data : predict_request) :
    logger.info("starting move predict")
    move_next = agent.get_action( TicTacToe(request_data.current_player, 
                                np.reshape(request_data.game_state, (3, 3))))
    logger.info(f"The move is {move_next}")
    return {"move": move_next}