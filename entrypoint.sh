#!/bin/sh
set -e

echo "⏳ Waiting for database..."
while ! uv run python - <<EOF
import os
import psycopg2

try:
    psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        sslmode="require",
    )
except psycopg2.OperationalError:
    raise SystemExit(1)
EOF
do
  echo "Database not ready, retrying in 3 seconds..."
  sleep 3
done

echo "✅ Database is ready"

# Run migrations
echo "🗄️ Running migrations..."
uv run python manage.py migrate_schemas --noinput

# Bootstrap public tenant + domain
echo "🏗️ Bootstrapping public tenant..."
uv run python manage.py bootstrap_tenant || echo "ℹ️ Tenant already exists"

# Collect static files
echo "🧹 Collecting static files..."
uv run python manage.py collectstatic --noinput

# Start Gunicorn
echo "🔥 Starting Gunicorn..."
exec "$@"


