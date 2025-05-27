# Multi-stage build: backend + frontend
FROM python:3.10-slim

WORKDIR /app

COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Install backend dependencies
RUN pip install --upgrade pip && \
    pip install -r backend/requirements.txt && \
    pip install -r frontend/requirements.txt

# Default to launching the API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
