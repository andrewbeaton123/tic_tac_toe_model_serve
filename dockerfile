# Stage 1: Builder - Install dependencies
FROM python:3.10-alpine as builder

WORKDIR /app

# Install system dependencies required for certain Python packages, including git
RUN apk add --no-cache build-base curl unzip git

# Install Ngrok
RUN curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o ngrok.zip && \
    unzip ngrok.zip && \
    rm ngrok.zip && \
    mv ngrok /usr/local/bin

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image - Create the production image
FROM python:3.10-alpine

WORKDIR /app

# Install system dependencies for Ngrok in the final image
RUN apk add --no-cache curl unzip

# Copy Ngrok from the builder stage
COPY --from=builder /usr/local/bin/ngrok /usr/local/bin/ngrok

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the path to the venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code and the startup script
COPY . .
COPY start.sh .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using the startup script
CMD ["./start.sh"]

