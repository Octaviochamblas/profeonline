#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Ensure the admin superuser exists (idempotent; reads DJANGO_ADMIN_* env vars)
python manage.py ensure_admin

# Seed/refresh math resources
python manage.py seed_math_resources
