#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Promote all existing users to superuser
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); updated = 0;
for u in User.objects.all():
    u.is_superuser = True
    u.is_staff = True
    u.save()
    updated += 1
print(f'--- PROMOTED {updated} TOTAL USER(S) TO SUPERUSER ---')"
