#!/bin/sh
# BLSUNTECH_V2_ENTRYPOINT_V1
set -eu

echo "BlsunTech V2: collecting static assets..."
python manage.py collectstatic --noinput --verbosity 0

echo "BlsunTech V2: starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --threads 2 \
    --timeout 60
