import os
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.content.models import KnowledgeNode, NodeAssessmentQuestion
from apps.content.services.ai_generation_service import generate_assessment_questions_for_node

LEVELS = (1, 2, 3)
TARGET_POOL = 7
DEFAULT_BATCH_SIZE = 7
DEFAULT_REQUEST_INTERVAL_SECONDS = 6.0


class Command(BaseCommand):
    help = (
        "Genera de forma autónoma e idempotente preguntas de evaluación formal "
        "para un KnowledgeNode o para todos los nodos publicados."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--node",
            default=None,
            help="semantic_id de un nodo puntual (ej. MAT.NUM.ENTEROS_CONJUNTO.NATURALES).",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Procesar todos los nodos de tipo 'recurso' publicados.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=DEFAULT_BATCH_SIZE,
            help=f"Preguntas por lote al llamar a la IA (def. {DEFAULT_BATCH_SIZE}).",
        )
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Guardar directamente como 'publicada' en lugar de 'borrador'.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo mostrar el plan (déficit) sin llamar a la IA.",
        )

    def _has_api_key(self):
        return bool(
            getattr(settings, "GEMINI_API_KEY", None)
            or os.environ.get("GEMINI_API_KEY")
            or getattr(settings, "OPENAI_API_KEY", None)
            or os.environ.get("OPENAI_API_KEY")
        )

    def _configure_windows_utf8(self):
        if not sys.platform.startswith("win"):
            return
        for stream in (sys.stdout, sys.stderr):
            reconfigure = getattr(stream, "reconfigure", None)
            if reconfigure is None:
                continue
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                continue

    def _wait_for_request_slot(self, last_request_at, interval):
        if last_request_at is None or interval <= 0:
            return
        remaining = interval - (time.monotonic() - last_request_at)
        if remaining > 0:
            time.sleep(remaining)

    def handle(self, *args, **options):
        self._configure_windows_utf8()
        dry_run = options["dry_run"]
        batch_size = max(1, options["batch_size"])
        status = "publicada" if options["publish"] else "borrador"

        # Pre-flight de la API key
        is_testing = "test" in sys.argv or "test" in getattr(settings, "SETTINGS_MODULE", "")
        if not dry_run and not self._has_api_key():
            if settings.DEBUG or is_testing:
                self.stdout.write(self.style.WARNING(
                    "Sin GEMINI_API_KEY/OPENAI_API_KEY: se usará el generador SIMULADO (mock)."
                ))
            else:
                raise CommandError(
                    "No hay GEMINI_API_KEY ni OPENAI_API_KEY configuradas."
                )

        # Selección de nodos
        qs = KnowledgeNode.objects.filter(node_type=KnowledgeNode.NODE_RECURSO, is_published=True)
        if options["node"]:
            qs = qs.filter(semantic_id=options["node"])
            if not qs.exists():
                raise CommandError(f"No existe un nodo de recurso publicado con semantic_id '{options['node']}'.")
        elif not options["all"]:
            raise CommandError("Debes especificar un nodo puntual con --node o usar --all para procesar todos.")

        request_interval = DEFAULT_REQUEST_INTERVAL_SECONDS
        last_ai_request_at = None
        total_created = 0

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"{'[DRY-RUN] ' if dry_run else ''}Generación de preguntas de evaluación por nodo"
        ))

        for node in qs.iterator():
            node_has_work = False
            plan = []

            for level in LEVELS:
                existing = NodeAssessmentQuestion.objects.filter(
                    node=node,
                    level=level
                ).exclude(status="archivada").count()

                deficit = max(0, TARGET_POOL - existing)
                if deficit > 0:
                    node_has_work = True
                plan.append((level, existing, deficit))

            if not node_has_work:
                continue

            self.stdout.write(self.style.HTTP_INFO(
                f"\n> '{node.name}' ({node.semantic_id}) - estado='{status}'"
            ))

            for level, existing, deficit in plan:
                if deficit <= 0:
                    continue

                if dry_run:
                    total_created += deficit
                    self.stdout.write(
                        f"    - Nivel {level}: faltan {deficit} (hay {existing}/{TARGET_POOL})"
                    )
                    continue

                remaining = deficit
                while remaining > 0:
                    batch = min(batch_size, remaining)
                    if not is_testing:
                        self._wait_for_request_slot(last_ai_request_at, request_interval)
                        last_ai_request_at = time.monotonic()

                    try:
                        created = generate_assessment_questions_for_node(
                            node=node,
                            level=level,
                            count=batch,
                            status=status,
                            education_level=node.dificultad,
                        )
                        n = len(created)
                    except Exception as exc:
                        self.stdout.write(self.style.ERROR(
                            f"    [x] Nivel {level}: error generando - {exc}"
                        ))
                        break

                    if n == 0:
                        self.stdout.write(self.style.WARNING(
                            f"    [!] Nivel {level}: la IA no devolvió preguntas nuevas (posible duplicación)."
                        ))
                        break

                    total_created += n
                    remaining -= n

                generated = deficit - remaining
                if remaining == 0:
                    self.stdout.write(self.style.SUCCESS(
                        f"    [ok] Nivel {level}: +{generated} (objetivo {TARGET_POOL} cubierto)"
                    ))
                elif generated > 0:
                    self.stdout.write(self.style.WARNING(
                        f"    [~] Nivel {level}: parcial +{generated}/{deficit} (faltan {remaining})"
                    ))

        verbo = "Se generarían" if dry_run else "Generadas"
        self.stdout.write(self.style.SUCCESS(f"\n{verbo} {total_created} preguntas de evaluación."))
