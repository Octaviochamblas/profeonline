"""Progreso académico calculado desde los intentos reales (QuizAttempt).

El progreso ya **no** depende de la acción manual "Comprendido"
(`ResourceCompletion`, que se conserva solo como historial). Se calcula así:

- promedio por modo = media de los porcentajes de los **últimos 3 intentos**
  (con 1–2 intentos se usan solo los disponibles).
- progreso de nivel = práctica × 30% + evaluación × 70%
  (un modo sin intentos aporta 0).
- progreso de recurso = promedio de los niveles que tengan algún intento.

Estados históricos (separados del promedio reciente):
- `practice_ready` ("Preparado"): la práctica reciente alcanzó el umbral.
- `passed` ("Aprobado"): algún intento de evaluación aprobó alguna vez; persiste
  aunque el promedio reciente baje.
"""

from apps.content.selectors.evaluation_selectors import (
    get_available_levels_map,
    get_recent_attempts_by_resource,
)

RECENT_ATTEMPTS = 3
PRACTICE_WEIGHT = 0.30
EVALUATION_WEIGHT = 0.70
PRACTICE_READY_THRESHOLD = 80  # % de práctica reciente para quedar "Preparado"

LEVEL_LABELS = {1: "Conceptos", 2: "Ejercicios", 3: "Problemas"}
LEVEL_LABELS_LONG = {
    1: "Conceptos",
    2: "Ejercicios simples",
    3: "Problemas de aplicación",
}

_EMPTY_SLOT = {"recent": [], "passed": False, "count": 0}


def _average(values):
    """Media redondeada de una lista de porcentajes, o None si está vacía."""
    return round(sum(values) / len(values)) if values else None


def build_resource_progress(grouped, available_levels):
    """Construye el contrato de progreso de un recurso.

    Args:
        grouped: dict {(level, mode): {"recent": [pct...], "passed": bool, "count": int}}
                 (salida de `get_recent_attempts_by_resource` para ese recurso).
        available_levels: lista ordenada de niveles con preguntas publicadas.

    Returns:
        dict con `available_levels`, `worked_levels`, `weighted_progress`,
        `levels` (por nivel: averages, recientes, weighted, practice_ready, passed)
        e `initial_level`.
    """
    grouped = grouped or {}
    levels = {}
    worked_levels = []
    worked_level_progress = []

    for level in available_levels:
        prep = grouped.get((level, "preparacion"), _EMPTY_SLOT)
        ev = grouped.get((level, "evaluacion"), _EMPTY_SLOT)

        practice_average = _average(prep["recent"])
        evaluation_average = _average(ev["recent"])
        worked = bool(prep["count"] or ev["count"])

        # Un modo sin intentos aporta 0 al ponderado del nivel.
        weighted = round(
            (practice_average or 0) * PRACTICE_WEIGHT
            + (evaluation_average or 0) * EVALUATION_WEIGHT
        )

        if worked:
            worked_levels.append(level)
            worked_level_progress.append(weighted)

        levels[level] = {
            "level": level,
            "label": LEVEL_LABELS.get(level, f"Nivel {level}"),
            "label_long": LEVEL_LABELS_LONG.get(level, f"Nivel {level}"),
            "available": True,
            "worked": worked,
            "practice_average": practice_average,
            "evaluation_average": evaluation_average,
            "practice_recent": list(prep["recent"]),
            "evaluation_recent": list(ev["recent"]),
            "weighted_progress": weighted,
            "practice_ready": practice_average is not None
            and practice_average >= PRACTICE_READY_THRESHOLD,
            "passed": ev["passed"],
        }

    weighted_progress = (
        round(sum(worked_level_progress) / len(worked_level_progress))
        if worked_level_progress
        else 0
    )

    progress = {
        "available_levels": list(available_levels),
        "worked_levels": worked_levels,
        "weighted_progress": weighted_progress,
        "levels": levels,
        "has_questions": bool(available_levels),
    }
    progress["initial_level"] = select_initial_level(progress)
    return progress


def select_initial_level(progress):
    """Primer nivel disponible no aprobado; si todos aprobados, el más alto."""
    available = progress["available_levels"]
    if not available:
        return None
    for level in available:
        if not progress["levels"][level]["passed"]:
            return level
    return available[-1]


def get_resources_progress(user, resource_ids):
    """Progreso por recurso para varios recursos (sin N+1).

    Returns: dict {resource_id: contrato de progreso}.
    """
    resource_ids = list(resource_ids)
    if not resource_ids:
        return {}
    available_map = get_available_levels_map(resource_ids)
    grouped = get_recent_attempts_by_resource(user, resource_ids, limit=RECENT_ATTEMPTS)
    return {
        rid: build_resource_progress(grouped.get(rid, {}), available_map.get(rid, []))
        for rid in resource_ids
    }


def get_resource_progress(user, resource):
    """Progreso del contrato para un único recurso."""
    rid = resource.id if hasattr(resource, "id") else resource
    return get_resources_progress(user, [rid])[rid]
