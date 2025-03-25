#!/bin/bash
# entrypoint.sh

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI application
echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000