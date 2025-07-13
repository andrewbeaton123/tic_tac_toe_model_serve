#!/bin/sh

# Start Uvicorn in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Ngrok
# Use the NGROK_AUTH_TOKEN environment variable for authentication
# Expose port 8000 (where Uvicorn is running)
ngrok authtoken $NGROK_AUTH_TOKEN
ngrok http 8000 --log stdout > ngrok.log &

# Keep the container running by tailing the ngrok log or waiting for uvicorn
wait $!
