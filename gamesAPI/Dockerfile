# syntax=docker/dockerfile:1
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./

RUN python -m venv /app/.venv \
    && . /app/.venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

# Copy the rest of the application code
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

# Expose FastAPI and FastMCP ports
EXPOSE 8000 8001

# Command to run both FastAPI and FastMCP servers
CMD ["python", "main.py"]
