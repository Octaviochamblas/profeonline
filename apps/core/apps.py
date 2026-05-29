from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        # Run superuser setup on startup
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@profeonline.cl', 'ProfeOnline2026!')
                print("--- Startup: 'admin' superuser created successfully ---")
            else:
                u = User.objects.get(username='admin')
                u.set_password('ProfeOnline2026!')
                u.is_superuser = True
                u.is_staff = True
                u.save()
                print("--- Startup: 'admin' superuser verified/reset ---")

            # Also promote qimico user case-insensitively
            updated = User.objects.filter(username__iexact='qimico').update(is_superuser=True, is_staff=True)
            if updated:
                print(f"--- Startup: Promoted {updated} user(s) matching 'qimico' ---")
        except Exception as e:
            # Silent fallback during migrations or database creation
            print(f"--- Startup: Skipping superuser setup because: {e} ---")
