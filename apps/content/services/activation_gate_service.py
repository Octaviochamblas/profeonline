"""Read-only activation gate for the structured bank pilot.

Verifies that a topic's structured content (items, public guide, visible bank and
hidden evaluation pools) is complete and that level/final evaluations are assemblable
*before* allowing ``Topic.structured_bank_enabled`` to be turned on. It never writes.

Coexistence model: the gate does NOT require retiring the legacy bank (``scope=""``);
it only checks that the new structured layer is ready. Activation is fully reversible
by turning the flag back off.
"""

from dataclasses import dataclass

from apps.content.models import (
    ExerciseItem,
    Question,
    ResourceExerciseItem,
)
from apps.content.models.learning_guide import LearningGuide
from apps.content.models.topic_bank_config import TopicBankConfig
from apps.content.services.evaluation_assembly_service import (
    assemble_final_evaluation,
    assemble_level_evaluation,
)


@dataclass(frozen=True)
class GateCheck:
    key: str
    label: str
    ok: bool
    detail: str = ""


def _effective_practice_quota(link):
    return link.practice_quota or link.exercise_item.detected_exercise_count


def _effective_evaluation_quota(link):
    return link.evaluation_quota or link.exercise_item.detected_exercise_count


def _published_count(*, item, resource, scope, level=None):
    filters = {
        "exercise_item": item,
        "resource": resource,
        "scope": scope,
        "status": "publicada",
        "resource__is_published": True,
        "exercise_item__status": "aprobado",
    }
    if scope in {"evaluacion_nivel", "prueba_final"}:
        filters["mode"] = "evaluacion"
        filters["estimated_minutes__gt"] = 0
        filters["points__gt"] = 0
        filters["level"] = item.level
    return Question.objects.filter(**filters).count()


def evaluate_topic_gate(topic, *, user):
    """Return ``{"ok": bool, "checks": [GateCheck, ...]}`` for one topic.

    ``user`` is only used to drive the assembler dry-run (its no-repetition history is
    irrelevant for a not-yet-live topic, so the feasibility check stays deterministic).
    """
    checks = []

    # 1. Configuración del banco presente y válida.
    config = TopicBankConfig.objects.filter(topic=topic).first()
    if config is None:
        checks.append(
            GateCheck(
                "config",
                "Configuración del banco creada",
                False,
                "Falta TopicBankConfig (minutos, intentos y distribución).",
            )
        )
        return {"ok": False, "checks": checks}
    checks.append(GateCheck("config", "Configuración del banco creada", True))

    # 2. Ítems: al menos uno aprobado y ninguno pendiente ("propuesto").
    items = list(
        ExerciseItem.objects.filter(topic=topic)
        .exclude(status="archivado")
        .prefetch_related("resource_links__resource", "resource_links__exercise_item")
    )
    approved = [item for item in items if item.status == "aprobado"]
    pending = [item for item in items if item.status == "propuesto"]
    checks.append(
        GateCheck(
            "items_aprobados",
            "Todos los ítems están aprobados",
            bool(approved) and not pending,
            (
                "No hay ítems aprobados."
                if not approved
                else f"{len(pending)} ítem(s) sin aprobar."
                if pending
                else ""
            ),
        )
    )

    # 3. Guía ProfeOnline pública.
    guide = LearningGuide.objects.filter(
        topic=topic, status="publicada", visibility="publica"
    ).first()
    checks.append(
        GateCheck(
            "guia_publica",
            "Guía ProfeOnline publicada",
            guide is not None,
            "" if guide else "Genera y publica la guía del tema.",
        )
    )

    # 4-5. Cobertura de banco visible y reserva de pools de evaluación, por ítem/recurso.
    visible_gaps = []
    level_gaps = []
    final_gaps = []
    has_eval_quota = False
    for item in approved:
        for link in item.resource_links.all():
            resource = link.resource
            if not resource.is_published:
                continue
            practice_quota = _effective_practice_quota(link)
            eval_quota = _effective_evaluation_quota(link)
            if practice_quota > 0:
                published = _published_count(
                    item=item, resource=resource, scope="banco_visible"
                )
                if published < practice_quota:
                    visible_gaps.append(
                        f"{item.title}/{resource.title}: {published}/{practice_quota}"
                    )
            if eval_quota > 0:
                has_eval_quota = True
                level_reserve = config.level_eval_attempts * eval_quota
                final_reserve = config.final_attempts * eval_quota
                level_published = _published_count(
                    item=item, resource=resource, scope="evaluacion_nivel"
                )
                final_published = _published_count(
                    item=item, resource=resource, scope="prueba_final"
                )
                if level_published < level_reserve:
                    level_gaps.append(
                        f"{item.title}/{resource.title}: "
                        f"{level_published}/{level_reserve}"
                    )
                if final_published < final_reserve:
                    final_gaps.append(
                        f"{item.title}/{resource.title}: "
                        f"{final_published}/{final_reserve}"
                    )

    checks.append(
        GateCheck(
            "banco_visible_completo",
            "Banco visible completo por ítem",
            not visible_gaps,
            "; ".join(visible_gaps[:5]),
        )
    )
    checks.append(
        GateCheck(
            "cuotas_evaluacion",
            "Cuotas de evaluación configuradas",
            has_eval_quota,
            "" if has_eval_quota else "Ningún ítem/recurso tiene cuota de evaluación.",
        )
    )
    checks.append(
        GateCheck(
            "reserva_nivel",
            (
                "Reserva de evaluación por nivel "
                f"(≥ {config.level_eval_attempts} intentos sin repetir)"
            ),
            not level_gaps,
            "; ".join(level_gaps[:5]),
        )
    )
    checks.append(
        GateCheck(
            "reserva_final",
            (
                "Reserva de prueba final "
                f"(≥ {config.final_attempts} intentos sin repetir)"
            ),
            not final_gaps,
            "; ".join(final_gaps[:5]),
        )
    )

    # 6. Factibilidad real: dry-run de los ensambladores (distribución/duración/pool).
    final_ok, final_detail = _final_feasible(topic=topic, config=config, user=user)
    checks.append(
        GateCheck("prueba_final_armable", "Prueba final armable", final_ok, final_detail)
    )
    level_ok, level_detail = _levels_feasible(topic=topic, approved=approved, user=user)
    checks.append(
        GateCheck(
            "evaluaciones_nivel_armables",
            "Evaluaciones por nivel armables",
            level_ok,
            level_detail,
        )
    )

    return {"ok": all(check.ok for check in checks), "checks": checks}


def _final_feasible(*, topic, config, user):
    try:
        assemble_final_evaluation(user=user, topic=topic, config=config, seed=0)
    except ValueError as exc:
        return False, str(exc)
    return True, ""


def _levels_feasible(*, topic, approved, user):
    # (recurso, nivel) que deberían poder armar una evaluación de nivel.
    pairs = set()
    for item in approved:
        for link in item.resource_links.all():
            if (
                link.resource.is_published
                and _effective_evaluation_quota(link) > 0
            ):
                pairs.add((link.resource, item.level))
    if not pairs:
        return False, "No hay recursos con cuota de evaluación por nivel."
    failures = []
    for resource, level in sorted(pairs, key=lambda pair: (pair[0].id, pair[1])):
        try:
            assemble_level_evaluation(
                user=user, topic=topic, resource=resource, level=level, seed=0
            )
        except ValueError as exc:
            failures.append(f"{resource.title} · Nivel {level}: {exc}")
    return not failures, "; ".join(failures[:5])
