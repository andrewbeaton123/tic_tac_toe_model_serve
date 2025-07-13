# Stage 1: Build the application
FROM python:3.10-alpine AS builder

WORKDIR /app

# Install git (needed for installing tic_tac_toe_game from git URL)
RUN apk add --no-cache git build-base python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Create the final image
FROM python:3.10-alpine AS final

WORKDIR /app



# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy application code and configuration
COPY --from=builder /app/app.py .
COPY --from=builder /app/config.yml .
COPY --from=builder /app/start.sh .
COPY --from=builder /app/src ./src

# ARG for Q-values file: Allows specifying a different Q-values file at build time.
# Example: docker build --build-arg Q_VALUES_FILE=another_q_values.pkl -t my_app .
ARG Q_VALUES_FILE=saved_q_values.pkl
COPY ${Q_VALUES_FILE} .

# To change Q-values at runtime without rebuilding the image, mount a volume:
# Example: docker run -v /path/to/your/q_values.pkl:/app/saved_q_values.pkl my_app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["/app/start.sh"]