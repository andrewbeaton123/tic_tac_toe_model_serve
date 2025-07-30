
![Coverage](/coverage.svg)
# Tic Tac Toe Model Serve

A FastAPI-based REST API for serving a trained reinforcement learning agent that predicts the next move in Tic Tac Toe. The agent uses Q-values learned via Monte Carlo methods and can be integrated into web apps, bots, or other services.

## Features

- **REST API**: Predict the next move for a given Tic Tac Toe board state.
- **Reinforcement Learning**: Uses a pre-trained Monte Carlo agent.
- **Easy Integration**: Simple HTTP endpoint for predictions.
- **Structured Logging**: Uses Loguru for structured, JSON-formatted request and application logging.
- **Configurable Validation**: Game rules and allowed players are loaded from `config.yml`.
- **Two-Layer Authentication**: 
  - Azure API Management authentication for client access
  - Internal API key validation for secure service-to-service communication

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

1.  **Q-values File (`saved_q_values.pkl`)**  
    This file contains the trained Q-values for the agent. By default, `saved_q_values.pkl` is used.

    -   **At Build Time**: You can specify a different Q-values file using the `Q_VALUES_FILE` build argument:
        ```bash
        docker build --build-arg Q_VALUES_FILE=path/to/your_q_values.pkl -t my_app .
        ```
    -   **At Runtime (using Docker Volume)**: To change the Q-values without rebuilding the image, mount a volume:
        ```bash
        docker run -v /path/to/your/q_values.pkl:/app/saved_q_values.pkl my_app
        ```

2.  **Configure `config.yml`**
    Ensure `config.yml` is present in the root directory with the necessary game configurations. An example is provided in the project structure.

3.  **Authentication Setup**
    
    The application uses a two-layer authentication system:

    a. **Azure API Management Authentication**
    - Your API is protected by Azure API Management
    - Clients need an Azure subscription key to access the API
    - Configure this in Azure Portal under API Management Services

    b. **Internal API Key**
    - Set the internal API key as an environment variable:
      ```bash
      # Linux/macOS
      export API_KEY="your_secret_api_key"
      
      # Windows PowerShell
      $env:API_KEY="your_secret_api_key"
      ```
    - This key is used for service-to-service authentication
    - Azure API Management will automatically include this key in requests to your API

4.  **Start the API server**

    a. **Start the Local Server**
    ```sh
    uvicorn app:app --reload
    ```

    b. **Create Public Endpoint with NGROK**
    ```sh
    ngrok http 8000
    ```
    - Copy the NGROK URL (e.g., `https://1234-your-ngrok-url.ngrok.io`)
    - Update your Azure API Management service with this URL as the backend
    - NGROK URL needs to be updated in Azure whenever it changes
    4.1 **Start  NGROK**

    ```sh 
    ngrok http 8000 
    ```
    Take the new NGROK link and place it into the current managed api in azure

5.  **Send a prediction request**

    Send a `POST` request to your Azure API Management endpoint with:

    ```json
    {
      "current_player": 1,
      "game_state": [0, 1, 0, 2, 1, 0, 0, 2, 0]
    }
    ```

    **Required Headers:**
    ```
    Ocp-Apim-Subscription-Key: your-azure-subscription-key
    Content-Type: application/json
    ```

    The Azure API Management service will:
    1. Validate your subscription key
    2. Forward the request to your API with the internal API key
    3. Return the response from your API

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
