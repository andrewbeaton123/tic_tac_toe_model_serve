
![Coverage](/coverage.svg)
# Tic Tac Toe Model Serve

A FastAPI-based REST API for serving a trained reinforcement learning agent that predicts the next move in Tic Tac Toe. The agent uses Q-values learned via Monte Carlo methods and is loaded at runtime from an MLflow model registry or local path.

## Features

- **REST API**: Predict the next move for a given Tic Tac Toe board state.
- **MLflow Model Serving**: Loads a `mlflow.pyfunc.PythonModel` at startup via a configurable URI — supports local paths, `runs:/` URIs, and `models:/` registry URIs.
- **Reinforcement Learning**: Serves a pre-trained Monte Carlo Q-learning agent.
- **Structured Logging**: Uses Loguru for structured, JSON-formatted request and application logging.
- **Two-Layer Authentication**:
  - Azure API Management authentication for client access
  - Internal API key validation for secure service-to-service communication

## Project Structure

```
.
├── app.py                              # Main FastAPI application
├── pyproject.toml                      # Project metadata and dependencies
├── tic_tac_toe_model_serve/
│   ├── __init__.py
│   ├── auth.py                         # API key authentication logic
│   ├── config_loader.py                # Re-exports key settings values
│   ├── dependencies.py                 # FastAPI dependency: loads MLflow model
│   ├── logging_config.py               # Loguru configuration
│   ├── logging_intercept.py            # Standard library log intercept
│   ├── middleware.py                   # Request performance logging middleware
│   ├── schemas.py                      # Pydantic request/response models
│   ├── settings.py                     # Pydantic BaseSettings (env / .env file)
│   ├── valid_state_check.py            # Board state validation
│   └── errors/
│       ├── error_class.py              # Custom HTTP exception classes
│       └── error_handlers.py           # FastAPI exception handlers
├── tests/
│   └── test_api.py                     # Pytest test suite
├── logs/                               # Log output directory
├── dockerfile                          # Docker container definition
└── LICENSE
```

## Requirements

- Python 3.10+
- Dependencies are managed via `pyproject.toml`.

Key runtime dependencies:
- `fastapi` / `uvicorn`: Web framework and ASGI server
- `mlflow`: Model loading from MLflow tracking server or local path
- `loguru`: Structured logging
- `tic_tac_toe_game`: Custom game logic library (loaded from GitHub)

Install all dependencies including test extras:

```sh
pip install -e .[test]
```

## Configuration

All configuration is managed through environment variables or a `.env` file using Pydantic `BaseSettings`.

| Variable | Required | Description |
|---|---|---|
| `API_KEY` | Yes | Internal API key for request authentication |
| `MLFLOW_MODEL_URI` | Yes | MLflow URI of the trained model to serve |
| `ALLOWED_PLAYERS` | No | Allowed player IDs (default: `[1, 2]`) |

**Example `.env` file:**

```bash
export API_KEY="your_secret_api_key"
export MLFLOW_MODEL_URI="models:/tictactoe-agent/1"
```

The `MLFLOW_MODEL_URI` accepts any valid MLflow model URI:

| Format | Example | Use case |
|---|---|---|
| Local path | `./mlflow_model` | Development / offline |
| Runs URI | `runs:/<run_id>/model` | Specific training run |
| Registry URI | `models:/tictactoe-agent/1` | Production (Model Registry) |

## Usage

1. **Set environment variables** in `.env` (see Configuration above).

2. **Start the API server:**

    ```sh
    uvicorn app:app --reload
    ```

3. **Send a prediction request** — `POST /next_move`:

    ```json
    {
      "current_player": 1,
      "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
    }
    ```

    - `current_player`: `1` or `2`
    - `game_state`: flat list of 9 integers — `0` = empty, `1` = player 1, `2` = player 2

    **Required Headers:**
    ```
    tic-tac-key: your_api_key
    Content-Type: application/json
    ```

    **Example Response:**
    ```json
    {
      "move": 6
    }
    ```

    - `move`: Board index (0–8) of the agent's recommended next move.

4. **Health check** — `GET /health`:

    ```json
    { "status": "ok" }
    ```

## Error Responses

| Condition | Status | Detail |
|---|---|---|
| Invalid API key | 403 | Forbidden |
| Board is full (no valid moves) | 422 | `"No valid moves available."` |
| Untrained game state encountered | 422 | `"Untrained game state encountered: ..."` |
| Invalid `current_player` value | 422 | Pydantic validation error |
| `game_state` wrong length or values | 422 | Pydantic validation error |

## Running with Ngrok for Development

When testing locally against Azure API Management, expose your local server with ngrok:

```sh
uvicorn app:app --reload --port 8000
ngrok http 8000
```

Update the backend URL in Azure API Management to the ngrok-provided URL. Note: the free tier assigns a new URL on each restart.

## Logging

The application uses [Loguru](https://loguru.readthedocs.io/en/stable/) for logging.
- Logs are written to the `logs/` directory.
- A new log file is created when the current one reaches 10 MB.
- Logs are in JSON format for easy parsing and analysis.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

**Author:** Andrew Beaton
