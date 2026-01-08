#!/bin/sh
set -e

echo "Starting Django entrypoint..."


echo "🗄️ Running migrations..."
uv run python manage.py migrate_schemas --noinput

echo "🧹 Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "🔥 Starting server..."
exec "$@"
