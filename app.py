from fastapi import FastAPI, HTTPException
from tic_tac_toe_game import TicTacToe
from tic_tac_toe_game.get_all_states import generate_all_states
from  tic_tac_learn.monte_carlo_learning.monte_carlo_tic_tac_2 import MonteCarloAgent
import pickle as pkl 
import numpy as np 
import pandas as pd 
from loguru import logger
from typing import List

from pydantic import BaseModel


app = FastAPI()


class predict_request(BaseModel):
    current_player : int
    game_state : List

class next_move(BaseModel):
     move: int

pkl_file_path = "saved_q_values.pkl"
try:
        with open(pkl_file_path, 'rb') as f:
            q_values  = pkl.load(f)
        logger.info("Successfully loaded .pkl file from artifact.")
        # Now you can use 'loaded_pkl' (your reinforcement learning model)
        # next_move = loaded_pkl.predict(current_board_state) # Example
        # print("Next Move:", next_move)

except FileNotFoundError:
    print(f"Error: The .pkl file '{pkl_file_path}' was not found in the artifacts.")
except Exception as e:
    print(f"Error loading .pkl file: {e}")


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