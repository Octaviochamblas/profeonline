"""Generación autónoma y recurrente de preguntas para recursos.

Esta es la capa de orquestación *headless* del banco de preguntas: recorre los
recursos publicados, calcula —por nivel y modo— cuántas preguntas faltan respecto
del *pool* configurado (``ResourceQuizConfig``), baja la transcripción real del
video de YouTube y genera SOLO el déficit con la IA (Gemini gratis).

Es **idempotente**: si se vuelve a correr, solo rellena lo que falte. Por eso es
seguro encadenarlo a un schedule o al ``Custom Start Command`` de Railway para que
los recursos que sube Codex se vayan poblando de preguntas sin intervención.

Ejemplos:
    # Ver el plan sin gastar nada (no llama a la IA):
    python manage.py generate_pending_questions --dry-run

    # Generar el déficit de los primeros 5 recursos con video que lo necesiten:
    python manage.py generate_pending_questions --only-videos --limit 5

    # Un recurso puntual, publicando directo:
    python manage.py generate_pending_questions --resource mi-slug --publish
"""

import os
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.content.models import Question, Resource, ResourceQuizConfig
from apps.content.models.resource_quiz_config import default_quiz_counts
from apps.content.services.ai_generation_service import generate_questions_for_resource
from apps.content.services.guide_service import build_reference_block
from apps.content.services.transcript_service import fetch_transcript

# Celdas de la matriz, en el mismo orden que usa el Estudio:
# (nivel, modo_config, modo_modelo, etiqueta)
LEVELS = (1, 2, 3)
MODES = (("practice", "preparacion", "práctica"), ("eval", "evaluacion", "evaluación"))

# Igual que el Estudio: lotes chicos para no pedir demasiadas preguntas de golpe.
DEFAULT_BATCH_SIZE = 5
# Tope de caracteres de transcript que se le pasan a la IA.
TRANSCRIPT_MAX_CHARS = 8000
# Intervalo conservador entre inicios de solicitudes para no agotar cuotas bajas.
DEFAULT_REQUEST_INTERVAL_SECONDS = 6.0


class Command(BaseCommand):
    help = (
        "Genera de forma autónoma e idempotente las preguntas que falten en cada "
        "recurso, basándose en la transcripción real del video y en el pool "
        "configurado por recurso (ResourceQuizConfig)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--resource",
            default=None,
            help="Slug de un recurso puntual. Por defecto procesa todos los publicados.",
        )
        parser.add_argument(
            "--subject",
            default=None,
            help="Slug de una asignatura a procesar (ej. matematica-escolar).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Máximo de recursos a procesar en esta corrida (0 = sin límite). "
                 "Solo cuentan los que tenían trabajo pendiente.",
        )
        parser.add_argument(
            "--only-videos",
            action="store_true",
            help="Procesar únicamente recursos que tengan video_url.",
        )
        parser.add_argument(
            "--allow-without-transcript",
            action="store_true",
            help="Generar igual aunque el video no tenga transcripción disponible "
                 "(por defecto se omite el recurso y se reintenta en la próxima corrida).",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=DEFAULT_BATCH_SIZE,
            help=f"Preguntas por lote al llamar a la IA (def. {DEFAULT_BATCH_SIZE}).",
        )
        parser.add_argument(
            "--education-level",
            default="media",
            help="Nivel educativo de respaldo si el tema no define uno (def. 'media').",
        )
        publish_group = parser.add_mutually_exclusive_group()
        publish_group.add_argument(
            "--publish",
            action="store_true",
            help="Guardar como 'publicada' (es el comportamiento por defecto).",
        )
        publish_group.add_argument(
            "--draft",
            action="store_true",
            help="Forzar 'borrador' (por defecto las preguntas se publican de inmediato).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo mostrar el plan (déficit y transcript) sin llamar a la IA.",
        )

    # ---------------------------------------------------------------- helpers

    def _plan_for(self, resource, counts):
        """Devuelve [(level, cfg_mode, model_mode, label, target, existing, deficit)]."""
        plan = []
        for level in LEVELS:
            for cfg_mode, model_mode, label in MODES:
                target = 0
                try:
                    target = int(counts.get(str(level), {}).get(cfg_mode, {}).get("pool", 0))
                except (ValueError, TypeError, AttributeError):
                    target = 0
                existing = (
                    Question.objects.filter(resource=resource, level=level, mode=model_mode)
                    .exclude(status="archivada")
                    .count()
                )
                deficit = max(0, target - existing)
                plan.append((level, cfg_mode, model_mode, label, target, existing, deficit))
        return plan

    def _resource_config(self, resource):
        return ResourceQuizConfig.objects.filter(resource=resource).first()

    def _resolve_status(self, config, force_publish, force_draft):
        # Preferencia del 🧑 (2026-06-17): publicar de inmediato por defecto.
        # Solo queda en borrador si se pide explícito con --draft.
        if force_draft:
            return "borrador"
        return "publicada"

    def _has_api_key(self):
        return bool(
            getattr(settings, "GEMINI_API_KEY", None)
            or os.environ.get("GEMINI_API_KEY")
            or getattr(settings, "OPENAI_API_KEY", None)
            or os.environ.get("OPENAI_API_KEY")
        )

    def _configure_windows_utf8(self):
        """Configura la consola real sin alterar streams durante el import."""
        if not sys.platform.startswith("win"):
            return
        for stream in (sys.stdout, sys.stderr):
            reconfigure = getattr(stream, "reconfigure", None)
            if reconfigure is None:
                continue
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                # Streams capturados, cerrados o no reconfigurables.
                continue

    def _wait_for_request_slot(self, last_request_at, interval):
        """Mantiene un intervalo mínimo entre inicios de solicitudes."""
        if last_request_at is None or interval <= 0:
            return
        remaining = interval - (time.monotonic() - last_request_at)
        if remaining > 0:
            time.sleep(remaining)

    # ------------------------------------------------------------------- main

    def handle(self, *args, **options):
        self._configure_windows_utf8()
        dry_run = options["dry_run"]
        limit = options["limit"]
        only_videos = options["only_videos"]
        allow_without_transcript = options["allow_without_transcript"]
        batch_size = max(1, options["batch_size"])
        education_fallback = options["education_level"]
        force_publish = options["publish"]
        force_draft = options["draft"]
        try:
            request_interval = max(
                0.0,
                float(os.environ.get(
                    "AI_REQUEST_INTERVAL_SECONDS",
                    DEFAULT_REQUEST_INTERVAL_SECONDS,
                )),
            )
        except ValueError as exc:
            raise CommandError(
                "AI_REQUEST_INTERVAL_SECONDS debe ser un número de segundos."
            ) from exc

        # Pre-flight de la API key (en dry-run no importa; en DEBUG/tests se usa mock).
        is_testing = "test" in sys.argv or "test" in getattr(settings, "SETTINGS_MODULE", "")
        if not dry_run and not self._has_api_key():
            if settings.DEBUG or is_testing:
                self.stdout.write(self.style.WARNING(
                    "Sin GEMINI_API_KEY/OPENAI_API_KEY: se usará el generador SIMULADO (mock)."
                ))
            else:
                raise CommandError(
                    "No hay GEMINI_API_KEY ni OPENAI_API_KEY configuradas. "
                    "Configura una (Gemini es gratis: https://aistudio.google.com/apikey) "
                    "o usa --dry-run para ver el plan sin generar."
                )

        # Selección de recursos.
        qs = Resource.objects.filter(is_published=True).select_related("topic")
        if options["resource"]:
            qs = qs.filter(slug=options["resource"])
            if not qs.exists():
                raise CommandError(f"No existe un recurso publicado con slug '{options['resource']}'.")
        if options["subject"]:
            qs = qs.filter(subject__slug=options["subject"])
        if only_videos:
            qs = qs.exclude(video_url__isnull=True).exclude(video_url="")
        qs = qs.order_by("id")

        # Contadores de resumen.
        n_processed = 0          # recursos con trabajo en los que efectivamente se actuó
        n_no_deficit = 0         # recursos ya completos
        n_no_transcript = 0      # recursos saltados por falta de transcript
        total_created = 0
        total_planned = 0        # déficit total detectado (útil en dry-run)
        last_ai_request_at = None

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"{'[DRY-RUN] ' if dry_run else ''}Generación de preguntas pendientes"
        ))

        for resource in qs.iterator():
            config = self._resource_config(resource)
            counts = config.counts if config else default_quiz_counts()
            plan = self._plan_for(resource, counts)
            resource_deficit = sum(row[6] for row in plan)

            if resource_deficit == 0:
                n_no_deficit += 1
                continue

            # Respetar el límite: solo cuenta recursos que requerían trabajo.
            if limit and n_processed >= limit:
                break

            total_planned += resource_deficit

            # Transcript: se PREFIERE el guardado en el recurso (bajado aparte desde
            # una IP residencial). Solo si no hay guardado se intenta en vivo (que en
            # la nube suele estar bloqueado por YouTube). Se reutiliza en las celdas.
            transcript = (resource.transcript or "").strip() or None
            if not transcript and resource.video_url:
                transcript = fetch_transcript(resource.video_url, max_chars=TRANSCRIPT_MAX_CHARS)
            if not transcript and not allow_without_transcript:
                n_no_transcript += 1
                self.stdout.write(
                    f"  [skip] '{resource.title}': sin transcript guardado ni disponible "
                    f"(deficit {resource_deficit}). Se reintentara cuando se cargue."
                )
                continue

            # Guías de referencia del recurso (estilo + contenido). Se arman una vez.
            reference_guides = build_reference_block(resource)

            status = self._resolve_status(config, force_publish, force_draft)
            edu_level = (getattr(resource.topic, "education_level", "") or "") or education_fallback
            t_flag = "con transcript" if transcript else "SIN transcript"
            g_flag = "con guia" if reference_guides else "sin guia"

            self.stdout.write(self.style.HTTP_INFO(
                f"\n> '{resource.title}' - deficit {resource_deficit} - {t_flag} - {g_flag} - estado='{status}'"
            ))

            n_processed += 1
            created_here = 0

            for level, cfg_mode, model_mode, label, target, existing, deficit in plan:
                if deficit <= 0:
                    continue

                if dry_run:
                    total_created += deficit  # en dry-run reportamos lo que se generaría
                    created_here += deficit
                    self.stdout.write(
                        f"    - N{level} {label}: faltan {deficit} (hay {existing}/{target})"
                    )
                    continue

                remaining = deficit
                while remaining > 0:
                    batch = min(batch_size, remaining)
                    if not is_testing:
                        self._wait_for_request_slot(last_ai_request_at, request_interval)
                        last_ai_request_at = time.monotonic()
                    try:
                        created = generate_questions_for_resource(
                            resource=resource,
                            level=level,
                            mode=model_mode,
                            count=batch,
                            status=status,
                            education_level=edu_level,
                            transcript=transcript,
                            use_transcript=False,  # ya lo bajamos arriba; no re-fetch
                            reference_guides=reference_guides,
                            use_guides=False,  # ya las armamos arriba; no re-consultar
                        )
                        n = len(created)
                    except Exception as exc:  # noqa: BLE001 - una celda no debe tumbar la corrida
                        self.stdout.write(self.style.ERROR(
                            f"    [x] N{level} {label}: error generando - {exc}"
                        ))
                        break

                    if n == 0:
                        self.stdout.write(self.style.WARNING(
                            f"    [!] N{level} {label}: la IA no devolvio preguntas; se corta esta celda."
                        ))
                        break

                    created_here += n
                    total_created += n
                    remaining -= n

                # Pie de celda fiel a lo ocurrido: el [ok] sale solo si se cubrio el
                # deficit. Si se corto antes (error/0 de la IA) ya se emitio un [x]/[!];
                # aqui solo se reporta lo generado parcial, nunca un falso [ok].
                generated = deficit - remaining
                if remaining == 0:
                    self.stdout.write(self.style.SUCCESS(
                        f"    [ok] N{level} {label}: +{generated} (objetivo {target} cubierto)"
                    ))
                elif generated > 0:
                    self.stdout.write(self.style.WARNING(
                        f"    [~] N{level} {label}: parcial +{generated}/{deficit} "
                        f"(faltan {remaining}, reintenta luego)"
                    ))

            self.stdout.write(
                f"  -> {'plan' if dry_run else 'generadas'} {created_here} en '{resource.title}'."
            )

        # ----------------------------------------------------------- resumen
        self.stdout.write(self.style.MIGRATE_HEADING("\nResumen"))
        verbo = "Se generarían" if dry_run else "Generadas"
        self.stdout.write(f"  Recursos con trabajo:   {n_processed}")
        self.stdout.write(f"  Recursos ya completos:  {n_no_deficit}")
        self.stdout.write(f"  Saltados sin transcript:{n_no_transcript}")
        self.stdout.write(self.style.SUCCESS(f"  {verbo} {total_created} preguntas."))
        if not dry_run and total_created and force_draft:
            self.stdout.write(
                "  Las preguntas en 'borrador' esperan tu revisión en la página de revisión."
            )
