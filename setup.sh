#!/bin/bash

Exit on any error

echo "Starting Smart House Backend Setup... 🚀"
set -e

Create and activate virtual environment

echo "Setting up virtual environment... 🏗️"
python3 -m venv venv
source venv/bin/activate

Upgrade pip

echo "Upgrading pip... 📦"
pip install --upgrade pip

Install dependencies

echo "Installing dependencies... ⚙️"
pip install -r requirements.txt

Set up environment variables

echo "Loading environment variables... 🌍"
cp .env.example .env

Run database migrations

echo "Applying database migrations... 🗄️"
alembic upgrade head

Start Redis server (if not running)

echo "Starting Redis server... 🔥"
if ! pgrep -x "redis-server" > /dev/null; then
redis-server --daemonize yes
fi

Start Celery worker

echo "Starting Celery worker... ⏳"
celery -A app.celery_worker worker --loglevel=info &

Start the application

echo "Starting FastAPI server... 🚀"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "Smart House Backend setup completed! 🎉"