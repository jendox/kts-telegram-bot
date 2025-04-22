#!/bin/sh
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting app..."
exec python -m data_service.main
