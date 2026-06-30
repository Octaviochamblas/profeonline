"""Genera resúmenes pedagógicos para NodeContent usando Gemini.

Uso:
    python manage.py generate_node_summaries           # todos sin resumen
    python manage.py generate_node_summaries --all     # fuerza regeneración
    python manage.py generate_node_summaries --id MAT.NUM.ENTEROS_CONJUNTO.DEFINICION
"""

import logging
import os
import re
import time

import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.content.models import NodeContent

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """\
Eres un profesor experto en {asignatura}. Tu tarea es escribir un resumen didáctico
para una tarjeta de repaso que el alumno verá ANTES de practicar ejercicios.

El resumen debe:
- Tener 2-3 oraciones máximo.
- Explicar en qué consiste el concepto Y cómo se aplica (el qué y el cómo).
- Usar lenguaje claro y directo, apropiado para un alumno secundario.
- NO repetir el título del recurso textualmente.
- NO comenzar con "En este recurso..." ni "Este recurso...".
- Si usas énfasis, usa Markdown real y con intención (ej. `**concepto clave**`).
- Si aparece notación matemática, delimítala con `$...$`. Nunca escribas fórmulas
  crudas como `x^2`, `a/b` o `a+b` fuera de delimitadores matemáticos.
- NO uses comillas envolventes, placeholders como `""`, énfasis vacío como `** **`
  o `** ""`, listas, títulos, ni bloques de código.

Información del recurso:
Tema: {nombre}
Objetivo: {objetivo}
Procedimiento (pasos clave):
{procedimiento}

Responde SOLO con el texto final del resumen. Puedes usar Markdown ligero si aporta
claridad, pero sin comillas exteriores ni formato sobrante.
"""

_SURROUNDING_QUOTES = (
    ('"', '"'),
    ("'", "'"),
    ("“", "”"),
    ("‘", "’"),
)


def _normalize_summary_output(text: str) -> str:
    summary = str(text or "").strip()
    if summary.startswith("```") and summary.endswith("```"):
        summary = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", summary)
        summary = re.sub(r"\s*```$", "", summary).strip()

    changed = True
    while changed and len(summary) >= 2:
        changed = False
        for opener, closer in _SURROUNDING_QUOTES:
            if summary.startswith(opener) and summary.endswith(closer):
                summary = summary[len(opener):-len(closer)].strip()
                changed = True
                break

    summary = re.sub(r"\*\*\s*\*\*", "", summary)
    summary = re.sub(r"\*\*\s*[\"“”'‘’]{0,2}\s*\*\*", "", summary)
    summary = re.sub(r"\s{2,}", " ", summary).strip()
    return summary


def _call_gemini(prompt: str, key: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": key}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 429:
                time.sleep(30 * (attempt + 1))
                continue
            resp.raise_for_status()
            data = resp.json()
            # Gemini 2.5 puede devolver varios parts (thinking + texto).
            # Solo concatenamos los parts sin thought:true.
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
            if not text.strip():
                raise RuntimeError("Gemini devolvió texto vacío")
            return text.strip()
        except Exception as e:
            if attempt == 2:
                raise RuntimeError(f"Gemini falló tras 3 intentos: {e}") from e
            time.sleep(3)
    raise RuntimeError("Gemini no respondió tras 3 intentos (rate limit)")


class Command(BaseCommand):
    help = "Genera resúmenes pedagógicos con Gemini para NodeContent."

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Regenerar incluso los que ya tienen resumen.",
        )
        parser.add_argument(
            "--id",
            dest="semantic_id",
            default=None,
            help="Procesar solo este semantic_id.",
        )

    def handle(self, *args, **options):
        key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            self.stderr.write(self.style.ERROR("GEMINI_API_KEY no configurada."))
            return

        qs = NodeContent.objects.select_related("node")
        if options["semantic_id"]:
            qs = qs.filter(node__semantic_id=options["semantic_id"])
        elif not options["all"]:
            qs = qs.filter(resumen="")

        total = qs.count()
        if total == 0:
            self.stdout.write("No hay NodeContent que procesar.")
            return

        self.stdout.write(f"Generando resúmenes para {total} recursos…")
        ok = errors = 0

        for nc in qs:
            pasos = nc.procedimiento or []
            pasos_str = "\n".join(
                f"- {p}" for p in pasos[:5]
            ) or "(sin procedimiento definido)"

            prompt = _PROMPT_TEMPLATE.format(
                asignatura=nc.node.subject_abbr,
                nombre=nc.node.name,
                objetivo=nc.objetivo or "(sin objetivo)",
                procedimiento=pasos_str,
            )

            try:
                resumen = _normalize_summary_output(_call_gemini(prompt, key))
                nc.resumen = resumen
                nc.save(update_fields=["resumen"])
                self.stdout.write(f"  OK  {nc.node.semantic_id}")
                ok += 1
                time.sleep(6)  # cortesía con la API gratuita (límite: 10 RPM)
            except Exception as e:
                self.stderr.write(f"  ERR {nc.node.semantic_id}: {e}")
                errors += 1

        self.stdout.write(
            self.style.SUCCESS(f"\nOK: {ok}  Errores: {errors}")
        )
