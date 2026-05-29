#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Promote 'qimico' to superuser
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); updated = User.objects.filter(username__iexact='qimico').update(is_superuser=True, is_staff=True); print(f'--- PROMOTED {updated} USER(S) MATCHING qimico TO SUPERUSER ---')"
