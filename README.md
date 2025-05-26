# Tic Tac Toe Model Serve

A FastAPI-based REST API for serving a trained reinforcement learning agent that predicts the next move in Tic Tac Toe. The agent uses Q-values learned via Monte Carlo methods and can be integrated into web apps, bots, or other services.

## Features

- **REST API**: Predict the next move for a given Tic Tac Toe board state.
- **Reinforcement Learning**: Uses a pre-trained Monte Carlo agent.
- **Easy Integration**: Simple HTTP endpoint for predictions.
- **Logging**: Uses Loguru for informative logging.

## Requirements

- Python 3.10+
- See `requirements.txt` for all dependencies.

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1. **Ensure [`saved_q_values.pkl`](saved_q_values.pkl) is present**  
   The file should contain the trained Q-values for the agent.

2. **Start the API server**

```sh
uvicorn app:app --reload
```

3. **Send a prediction request**

POST to `/next_move` with JSON body:

```json
{
  "current_player": 1,
  "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
}
```

- `current_player`: `1` or `2`
- `game_state`: Flat list of 9 integers (0=empty, 1=player 1, 2=player 2)

**Response:**

```json
{
  "move": 6
}
```

- `move`: Index (0-8) of the recommended move.

## File Structure

```
app.py                  # Main FastAPI app
requirements.txt        # Python dependencies
saved_q_values.pkl      # Trained Q-values (required)
mlflow_artifacts/       # (Optional) MLflow artifacts
```

## License

MIT License. See [`LICENSE`](LICENSE).

---

**Author:** Andrew Beaton

---

*Note: This repo requires the `tic_tac_toe_game` and `tic_tac_learn` modules, which should be available in your Python environment.*