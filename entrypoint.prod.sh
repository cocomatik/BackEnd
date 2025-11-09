#!/usr/bin/env bash
set -e

# Optional: wait for DB if using containerized postgres
if [ -n "${POSTGRES_USER}" ]; then
  echo "Waiting for database..."
  until python - <<'PY'
import os, sys, time
import psycopg2
from urllib.parse import urlparse

url = os.getenv("DATABASE_URL")
if not url:
    # Build from POSTGRES_* envs (compose local db)
    user = os.getenv("POSTGRES_USER")
    pwd = os.getenv("POSTGRES_PASSWORD")
    host = "db"
    db = os.getenv("POSTGRES_DB")
    url = f"postgresql://{user}:{pwd}@{host}:5432/{db}"

for _ in range(30):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        sys.exit(0)
    except Exception:
        time.sleep(1)
sys.exit(1)
PY
  do
    echo "DB not ready yet..."
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# bind to 0.0.0.0:8000 behind nginx
exec gunicorn BackendR.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60
