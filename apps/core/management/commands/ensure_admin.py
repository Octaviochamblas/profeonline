import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Garantiza que exista un superusuario administrador. "
        "Es idempotente y lee las credenciales desde variables de entorno "
        "(DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_EMAIL, DJANGO_ADMIN_PASSWORD). "
        "Nunca reescribe la contraseña de un usuario que ya existe."
    )

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME", "admin")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        user = User.objects.filter(username=username).first()

        if user is None:
            if not password:
                self.stdout.write(
                    self.style.WARNING(
                        f"El superusuario '{username}' no existe y DJANGO_ADMIN_PASSWORD "
                        "no está definido; no se creó ninguna cuenta."
                    )
                )
                return

            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f"Superusuario '{username}' creado correctamente.")
            )
            return

        # El usuario ya existe: aseguramos privilegios pero NUNCA reescribimos
        # la contraseña automáticamente (eso permitía resetearla en cada arranque).
        update_fields = []
        if not user.is_superuser:
            user.is_superuser = True
            update_fields.append("is_superuser")
        if not user.is_staff:
            user.is_staff = True
            update_fields.append("is_staff")

        if update_fields:
            user.save(update_fields=update_fields)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuario '{username}' actualizado (privilegios restaurados)."
                )
            )
        else:
            self.stdout.write(f"Superusuario '{username}' ya estaba configurado.")
