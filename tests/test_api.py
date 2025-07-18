import sys
sys.path.append('./')

import os
from fastapi.testclient import  TestClient
from app import app


client = TestClient(app)
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise Exception("API KEY NOT LOADED")



def test_next_move_success():
    response  = client.post(
        "/next_move",
        headers={"tic-tac-key" : API_KEY}, 
        json  = {
            "current_player": 1,
            "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
        }
    )
    assert  response.status_code == 200 
    assert "move" in response.json()