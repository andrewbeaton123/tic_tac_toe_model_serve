import sys
sys.path.append('./')

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app import app
from tic_tac_toe_model_serve.auth import get_api_key
from tic_tac_toe_model_serve.dependencies import get_model

TEST_API_KEY = "test_key"

VALID_BOARD = [0, 1, 0, 2, 1, 0, 0, 2, 0]
FULL_BOARD = [1, 1, 2, 2, 1, 1, 2, 2, 2]


def get_test_api_key():
    return TEST_API_KEY


def get_mock_model():
    mock = MagicMock()
    mock.predict.return_value = {"action": 4, "q_value": 0.9}
    return mock


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_next_move_success():
    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_mock_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 1, "game_state": VALID_BOARD}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 200
    assert response.json() == {"move": 4}


def test_no_next_move_detection():
    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_mock_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 1, "game_state": FULL_BOARD}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 422
    assert response.json() == {"detail": "No valid moves available."}


def test_untrained_state_returns_422():
    def get_error_model():
        mock = MagicMock()
        mock.predict.side_effect = ValueError("Untrained game state encountered: (0, 1, 0, 2, 1, 0, 0, 2, 0)")
        return mock

    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_error_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 1, "game_state": VALID_BOARD}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 422
    assert "Untrained game state" in response.json()["detail"]


def test_invalid_api_key():
    response = client.post(
        "/next_move",
        headers={"tic-tac-key": "invalid_key"},
        json={"current_player": 1, "game_state": VALID_BOARD}
    )
    assert response.status_code == 403


def test_invalid_player():
    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_mock_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 3, "game_state": VALID_BOARD}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 422


def test_invalid_game_state_length():
    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_mock_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 1, "game_state": [0, 1, 0, 2, 1, 0, 0, 2]}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 422


def test_invalid_game_state_values():
    app.dependency_overrides[get_api_key] = get_test_api_key
    app.dependency_overrides[get_model] = get_mock_model
    try:
        response = client.post(
            "/next_move",
            headers={"tic-tac-key": TEST_API_KEY},
            json={"current_player": 1, "game_state": [0, 1, 0, 2, 5, 0, 0, 2, 0]}
        )
    finally:
        del app.dependency_overrides[get_api_key]
        del app.dependency_overrides[get_model]

    assert response.status_code == 422
