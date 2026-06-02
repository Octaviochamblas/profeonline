import os
import shutil
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Restaura un backup de la base de datos (SQLite o PostgreSQL) con guardas de seguridad para evitar tocar producción."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            "-f",
            type=str,
            required=True,
            help="Ruta del archivo backup a restaurar (obligatorio).",
        )
        parser.add_argument(
            "--confirmar",
            action="store_true",
            help="Confirma la restauración en bases de datos de producción o remotas.",
        )
        parser.add_argument(
            "--destino",
            type=str,
            help="Nombre de la base de datos destino para verificar el objetivo de la restauración.",
        )
        parser.add_argument(
            "--permitir-remoto",
            action="store_true",
            help=(
                "Permite restaurar contra una base remota/producción. Usar solo en emergencias "
                "después de apuntar DATABASE_URL al destino correcto."
            ),
        )

    def handle(self, *args, **options):
        db_config = settings.DATABASES["default"]
        engine = db_config["ENGINE"]
        db_name = db_config["NAME"]

        # Obtener y validar el archivo backup
        backup_file = options.get("file")
        if not os.path.exists(backup_file):
            raise CommandError(f"El archivo backup no existe: {backup_file}")

        # Guardas de seguridad anti-producción
        db_host = db_config.get("HOST", "")
        db_password = db_config.get("PASSWORD", "")

        is_postgresql = engine == "django.db.backends.postgresql"
        is_remote = is_postgresql and db_host not in ["", "localhost", "127.0.0.1", "db"]
        is_prod_settings = is_postgresql and not settings.DEBUG

        if is_remote or is_prod_settings:
            self.stdout.write(self.style.WARNING(
                "¡PELIGRO!: Se detectó que el destino de la base de datos es REMOTO o de PRODUCCIÓN."
            ))

            confirmar = options.get("confirmar")
            destino = options.get("destino")
            permitir_remoto = options.get("permitir_remoto")

            if not confirmar or destino != db_name or not permitir_remoto:
                raise CommandError(
                    "Operación abortada por seguridad. Para restaurar sobre una base de datos remota o de producción, "
                    "debe proveer obligatoriamente los flags:\n"
                    "  --confirmar\n"
                    f"  --destino {db_name}\n"
                    "  --permitir-remoto\n"
                    "Por favor verifique que está apuntando al destino correcto."
                )

        if engine == "django.db.backends.sqlite3":
            try:
                self.stdout.write("Iniciando restauración de SQLite...")
                from django.db import connection, connections
                import sqlite3

                if db_name and db_name != ":memory:":
                    connections.close_all()
                    shutil.copy2(backup_file, db_name)
                else:
                    connection.ensure_connection()
                    con = connection.connection
                    if con is None:
                        raise CommandError("No hay conexión activa a la base de datos SQLite.")

                    src = sqlite3.connect(backup_file)
                    with src:
                        src.backup(con)
                    src.close()

                self.stdout.write(self.style.SUCCESS(f"Restauración SQLite exitosa desde: {backup_file}"))
            except Exception as e:
                raise CommandError(f"Error al restaurar SQLite: {str(e)}")

        elif engine == "django.db.backends.postgresql":
            db_user = db_config.get("USER", "")
            db_port = db_config.get("PORT", "")

            self.stdout.write(f"Iniciando restauración de PostgreSQL sobre la DB: {db_name}...")

            env = os.environ.copy()
            if db_password:
                env["PGPASSWORD"] = db_password

            # Construir comando pg_restore
            # Usamos formato Custom (-F c), no-owner (-O), no-privileges (-x), clean (-c) para limpiar antes
            cmd = ["pg_restore", "-d", db_name, "-O", "-x", "-c", "-v"]
            if db_user:
                cmd.extend(["-U", db_user])
            if db_host:
                cmd.extend(["-h", db_host])
            if db_port:
                cmd.extend(["-p", str(db_port)])
            cmd.append(backup_file)

            try:
                subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f"Restauración PostgreSQL exitosa desde: {backup_file}"))
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr or e.stdout or ""
                if db_password:
                    error_msg = error_msg.replace(db_password, "********")
                raise CommandError(f"Error al ejecutar pg_restore: {error_msg}")
            except Exception as e:
                raise CommandError(f"Error inesperado al restaurar PostgreSQL: {str(e)}")

        else:
            raise CommandError(f"Engine de base de datos no soportado para restauración: {engine}")
