import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Genera un backup de la base de datos por defecto (SQLite o PostgreSQL) en la carpeta backups/."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Ruta del archivo de salida del backup. Si no se provee, se auto-genera con timestamp.",
        )

    def handle(self, *args, **options):
        db_config = settings.DATABASES["default"]
        engine = db_config["ENGINE"]

        # Crear directorio backups/ si no existe
        backups_dir = os.path.join(settings.BASE_DIR, "backups")
        os.makedirs(backups_dir, exist_ok=True)

        # Determinar el archivo de salida
        output_file = options.get("file")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        if engine == "django.db.backends.sqlite3":
            if not output_file:
                output_file = os.path.join(backups_dir, f"db_backup_{timestamp}.sqlite3")

            try:
                self.stdout.write("Iniciando respaldo de SQLite...")
                from django.db import connection
                import sqlite3

                connection.ensure_connection()
                con = connection.connection
                if con is None:
                    raise CommandError("No hay conexión activa a la base de datos SQLite.")

                dest = sqlite3.connect(output_file)
                with dest:
                    con.backup(dest)
                dest.close()

                self.stdout.write(self.style.SUCCESS(f"Respaldo SQLite exitoso: {output_file}"))
            except Exception as e:
                raise CommandError(f"Error al respaldar SQLite: {str(e)}")

        elif engine == "django.db.backends.postgresql":
            if not output_file:
                output_file = os.path.join(backups_dir, f"db_backup_{timestamp}.dump")

            db_name = db_config["NAME"]
            db_user = db_config.get("USER", "")
            db_host = db_config.get("HOST", "")
            db_port = db_config.get("PORT", "")
            db_password = db_config.get("PASSWORD", "")

            self.stdout.write("Iniciando respaldo de PostgreSQL...")

            env = os.environ.copy()
            if db_password:
                env["PGPASSWORD"] = db_password

            # Construir comando pg_dump
            # Usamos formato Custom (-F c), blobs (-b)
            cmd = ["pg_dump", "-F", "c", "-b", "-f", output_file]
            if db_user:
                cmd.extend(["-U", db_user])
            if db_host:
                cmd.extend(["-h", db_host])
            if db_port:
                cmd.extend(["-p", str(db_port)])
            cmd.append(db_name)

            try:
                subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f"Respaldo PostgreSQL exitoso: {output_file}"))
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr or e.stdout or ""
                # Ocultar la contraseña si apareciera en el mensaje
                if db_password:
                    error_msg = error_msg.replace(db_password, "********")
                raise CommandError(f"Error al ejecutar pg_dump: {error_msg}")
            except Exception as e:
                raise CommandError(f"Error inesperado al respaldar PostgreSQL: {str(e)}")

        else:
            raise CommandError(f"Engine de base de datos no soportado para respaldos: {engine}")
