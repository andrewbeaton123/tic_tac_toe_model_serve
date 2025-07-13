# Tic Tac Toe Model Serve

A FastAPI-based REST API for serving a trained reinforcement learning agent that predicts the next move in Tic Tac Toe. The agent uses Q-values learned via Monte Carlo methods and can be integrated into web apps, bots, or other services.

## Features

- **REST API**: Predict the next move for a given Tic Tac Toe board state.
- **Reinforcement Learning**: Uses a pre-trained Monte Carlo agent.
- **Easy Integration**: Simple HTTP endpoint for predictions.
- **Structured Logging**: Uses Loguru for structured, JSON-formatted request and application logging.
- **Configurable Validation**: Game rules and allowed players are loaded from `config.yml`.
- **API Key Authentication**: Secure access to the prediction endpoint.

## Project Structure

```
.
├── app.py                  # Main FastAPI application
├── requirements.txt        # Python dependencies
├── saved_q_values.pkl      # Trained Q-values (required)
├── config.yml              # Application configuration (e.g., game rules)
├── src/
│   ├── __init__.py
│   ├── auth.py             # API key authentication logic
│   ├── config_loader.py    # Loads configuration from config.yml
│   ├── load_q_values.py    # Helper to load Q-values
│   ├── logging_config.py   # Loguru configuration
│   ├── middleware.py       # Custom FastAPI middleware (e.g., request logging)
│   ├── prediction_agent.py # The prediction agent logic
│   └── schemas.py          # Pydantic models for request/response validation
├── logs/                   # Directory for log files
├── dockerfile              # Docker container definition
├── .gitignore              # Git ignore file
└── LICENSE                 # Project License
```

## Requirements

- Python 3.10+
- All dependencies are listed in `requirements.txt`.

Key dependencies include:
- `fastapi`: The web framework.
- `uvicorn`: The ASGI server.
- `loguru`: For logging.
- `tic_tac_toe_game`: Custom game logic library.
- `tic_tac_learn`: Custom reinforcement learning library.
- `PyYAML`: For loading configuration.

Install all dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1.  **Ensure `saved_q_values.pkl` is present**  
    This file contains the trained Q-values for the agent and must be in the root directory.

2.  **Configure `config.yml`**
    Ensure `config.yml` is present in the root directory with the necessary game configurations. An example is provided in the project structure.

3.  **Set up API Key**
    The application uses an API key for authentication. Set the `API_KEY` environment variable before starting the application.

    Example (Linux/macOS):
    ```bash
    export API_KEY="your_secret_api_key"
    ```
    Example (Windows PowerShell):
    ```powershell
    $env:API_KEY="your_secret_api_key"
    ```

4.  **Start the API server**

    ```sh
    uvicorn app:app --reload
    ```

5.  **Send a prediction request**

    Send a `POST` request to the `/next_move` endpoint with a JSON body and the API key in the header:

    ```json
    {
      "current_player": 1,
      "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
    }
    ```

    **Headers:**
    `tic-tac-key: your_secret_api_key`

    -   `current_player`: `1` or `2` (as defined in `config.yml`).
    -   `game_state`: A flat list of 9 integers representing the board (0=empty, 1=player 1, 2=player 2).

    **Example Response:**

    ```json
    {
      "move": 6
    }
    ```

    -   `move`: The board index (0-8) of the agent's recommended move.

## Logging

The application uses [Loguru](https://loguru.readthedocs.io/en/stable/) for logging.
- Logs are automatically written to the `logs/` directory.
- A new log file is created when the current one reaches 10 MB.
- Logs are in JSON format for easy parsing and analysis.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

**Author:** Andrew Beaton
