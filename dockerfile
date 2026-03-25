# Stage 1: Build the application
FROM python:3.10-alpine AS builder

WORKDIR /app

# Install git (needed for installing tic_tac_toe_game from git URL)
RUN apk add --no-cache git build-base python3-dev

# Copy pyproject.toml, README.md, and the new package folder
COPY  . /app/
RUN pip install --no-cache-dir .

# Stage 2: Create the final image
FROM python:3.10-alpine AS final

WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy application code
COPY . .

# Copy the Q-values file (assuming it's part of the build for now)
# This can be overridden by mounting a volume at runtime if needed
COPY saved_q_values.pkl .

# Set environment variable for the Q-values path, defaulting to the copied file
ENV Q_VALUES_PATH="/app/saved_q_values.pkl"

# Set the PATH to include the site-packages where dependencies are installed
ENV PATH="/usr/local/bin:$PATH"


# old method that starts ngrok and the api in the one location
#CMD ["/app/start.sh"]

EXPOSE 9100
# new method that just starts the api using uvicorn
#TODO: move the port address andd other options out to a environment variable

ENTRYPOINT ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9100"]
