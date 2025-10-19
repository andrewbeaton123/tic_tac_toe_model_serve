
import sys
sys.path.append('./')

from fastapi.testclient import TestClient
from app import app
from src.auth import get_api_key

# Define a dummy API key for testing
TEST_API_KEY = "test_key"

# Define an override function for the get_api_key dependency
def get_test_api_key():
    return TEST_API_KEY

client = TestClient(app)

def test_no_next_move_detection():
    with client.dependency_overrides({
        get_api_key: get_test_api_key
    }):
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={
                "current_player": 1,
                "game_state": [1, 1, 2, 2, 1, 1, 2, 2, 2]
            }
        )
    assert response.status_code == 422
    assert response.json() == {"detail": "No valid moves available."}

def test_next_move_success():
    with client.dependency_overrides({
        get_api_key: get_test_api_key
    }):
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={
                "current_player": 1,
                "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
            }
        )
    assert response.status_code == 200
    assert "move" in response.json()

def test_invalid_api_key():
    # For this test, we do NOT override get_api_key, so the original logic runs.
    response = client.post(
        "/next_move",
        headers={"tic-tac-key": "invalid_key"},
        json={
            "current_player": 1,
            "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
        }
    )
    assert response.status_code == 403

def test_invalid_player():
    with client.dependency_overrides({
        get_api_key: get_test_api_key
    }):
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={
                "current_player": 3,
                "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
            }
        )
    assert response.status_code == 422

def test_invalid_game_state():
    with client.dependency_overrides({
        get_api_key: get_test_api_key
    }):
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={
                "current_player": 1,
                "game_state": [0, 1, 0, 2, 1, 0, 0, 2]
            }
        )
    assert response.status_code == 422
