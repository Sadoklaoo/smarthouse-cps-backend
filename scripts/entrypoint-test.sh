#!/bin/bash
# entrypoint-test.sh

# Wait for the test database to be ready
echo "Waiting for the test database to be ready..."
/wait-for-it.sh test_db:5432 --timeout=20 --strict -- echo "Test database is ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head


# Run tests
echo "Running tests..."
pytest --disable-warnings

# Keep the container alive (optional for debugging)
tail -f /dev/null