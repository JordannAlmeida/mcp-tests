# syntax=docker/dockerfile:1
# Build stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN python -m venv /app/.venv \
    && . /app/.venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the rest of the application code
COPY . .

# Set environment variables for venv
ENV PATH="/app/.venv/bin:$PATH"

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables (optional, for Streamlit)
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
