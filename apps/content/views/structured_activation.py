"""Admin-only activation of the structured bank pilot, governed by the gate.

The flag ``Topic.structured_bank_enabled`` is never flipped by hand: activation runs the
read-only gate and only turns it on when every check passes. Rollback is a single click
(turn the flag off, keep the topic in staging).
"""

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from apps.content.models.topic import Topic
from apps.content.services.activation_gate_service import evaluate_topic_gate
from apps.content.views.permissions import is_admin


def _render_panel(request, topic, *, message="", message_kind="", status=200):
    gate = evaluate_topic_gate(topic, user=request.user)
    return render(
        request,
        "partials/_activation_gate.html",
        {
            "topic": topic,
            "gate": gate,
            "message": message,
            "message_kind": message_kind,
        },
        status=status,
    )


@user_passes_test(is_admin)
@require_GET
def activation_panel(request):
    """Render the gate checklist for a topic (HTMX).

    Usa un parámetro propio (``activation_topic_id``) para no acoplarse al selector de
    ítems del panel: la activación debe poder elegir cualquier tema activo (incluido un
    legacy) para marcarlo en preparación.
    """
    topic_id = request.GET.get("activation_topic_id") or request.GET.get("topic_id")
    if not topic_id:
        return render(request, "partials/_activation_gate.html", {"topic": None})
    topic = get_object_or_404(Topic, id=topic_id, is_active=True)
    return _render_panel(request, topic)


@user_passes_test(is_admin)
@require_POST
def set_staging(request):
    """Mark/unmark a topic as 'in preparation' (enables admin panels, not student views)."""
    topic = get_object_or_404(
        Topic, id=request.POST.get("topic_id"), is_active=True
    )
    enable = request.POST.get("staging") == "1"
    # No tocar staging si el banco ya está activo: ahí la edición ya está habilitada.
    if not topic.structured_bank_enabled:
        topic.structured_bank_staging = enable
        topic.save(update_fields=["structured_bank_staging"])
    message = (
        "Tema en preparación: ya puedes clasificar y configurar su banco."
        if topic.structured_bank_staging
        else "Preparación desactivada."
    )
    return _render_panel(request, topic, message=message, message_kind="info")


@user_passes_test(is_admin)
@require_POST
def activate_structured_bank(request):
    """Run the gate and only then turn the pilot on for ONE topic."""
    topic = get_object_or_404(
        Topic, id=request.POST.get("topic_id"), is_active=True
    )
    if topic.structured_bank_enabled:
        return _render_panel(
            request,
            topic,
            message="El banco ya está activo en este tema.",
            message_kind="info",
        )
    gate = evaluate_topic_gate(topic, user=request.user)
    if not gate["ok"]:
        return render(
            request,
            "partials/_activation_gate.html",
            {
                "topic": topic,
                "gate": gate,
                "message": "No se puede activar: faltan requisitos del gate.",
                "message_kind": "danger",
            },
            status=400,
        )
    topic.structured_bank_enabled = True
    topic.structured_bank_staging = False
    topic.save(update_fields=["structured_bank_enabled", "structured_bank_staging"])
    return _render_panel(
        request,
        topic,
        message="¡Banco activado! El tema ya muestra guía, banco y evaluaciones a los alumnos.",
        message_kind="success",
    )


@user_passes_test(is_admin)
@require_POST
def deactivate_structured_bank(request):
    """Rollback: turn the pilot off (the topic reverts to the legacy experience)."""
    topic = get_object_or_404(
        Topic, id=request.POST.get("topic_id"), is_active=True
    )
    topic.structured_bank_enabled = False
    topic.structured_bank_staging = True
    topic.save(update_fields=["structured_bank_enabled", "structured_bank_staging"])
    return _render_panel(
        request,
        topic,
        message="Banco desactivado (rollback). El tema volvió al sistema actual.",
        message_kind="info",
    )
