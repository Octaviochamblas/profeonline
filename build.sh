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

# Sync the Sites framework domain with CANONICAL_BASE_URL (email links)
python manage.py ensure_site

# NOTA (C1): el seed NO se ejecuta en el deploy para no pisar contenido curado.
# Para sembrar/refrescar contenido, correr a demanda:
#   python manage.py seed_math_resources [--refrescar-seo]
