#!/usr/bin/env bash
set -e

echo "Checking Alembic..."
alembic --version

echo "Running migrations..."
alembic upgrade head

echo "############################# start fastapi #############################"

# Start FastAPI application
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
