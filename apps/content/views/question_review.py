from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction

from apps.content.views.permissions import is_admin
from apps.content.models import Resource, Question, Choice, ResourceQuizConfig
from apps.content.models.topic import Topic
from apps.content.services.evaluation_service import get_quiz_config

# Modos que se muestran como secciones plegables dentro de cada nivel.
# "ambas" (legacy) solo aparece si tiene preguntas.
MODE_GROUPS = [
    ("preparacion", "Práctica"),
    ("evaluacion", "Evaluación"),
    ("ambas", "Ambas"),
]


def _edit_choices_ctx(question):
    return {"LEVEL_CHOICES": Question.LEVEL_CHOICES,
            "MODE_CHOICES": Question.MODE_CHOICES,
            "STATUS_CHOICES": Question.STATUS_CHOICES}


def _build_levels_data(resource):
    """Agrupa las preguntas del recurso en Nivel → Modo → preguntas (con choices)."""
    all_questions = list(
        Question.objects.filter(resource=resource)
        .prefetch_related("choices")
        .order_by("level", "order", "id")
    )
    levels_data = []
    for lvl, lvl_name in Question.LEVEL_CHOICES:
        lvl_questions = [q for q in all_questions if q.level == lvl]
        modes = []
        for mkey, mlabel in MODE_GROUPS:
            mqs = [q for q in lvl_questions if q.mode == mkey]
            if mkey == "ambas" and not mqs:
                continue
            modes.append({"key": mkey, "label": mlabel, "questions": mqs, "count": len(mqs)})
        levels_data.append(
            {"num": lvl, "name": lvl_name, "count": len(lvl_questions), "modes": modes}
        )
    return levels_data


@user_passes_test(is_admin)
def question_review(request, slug):
    """Vista principal: acordeón Nivel → Modo → preguntas → alternativas."""
    resource = get_object_or_404(Resource, slug=slug)
    config = get_quiz_config(resource)
    config_db = getattr(resource, "quiz_config", None)

    topic_edu_level = getattr(resource.topic, "education_level", "") or ""
    context = {
        "resource": resource,
        "config": config,
        "config_db": config_db,
        "levels_data": _build_levels_data(resource),
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "RECOVERY_CHOICES": ResourceQuizConfig.RECOVERY_CHOICES,
        "EDUCATION_LEVEL_CHOICES": Topic.EDUCATION_LEVEL_CHOICES,
        "topic_edu_level": topic_edu_level,
        "topic_edu_label": dict(Topic.EDUCATION_LEVEL_CHOICES).get(topic_edu_level, ""),
    }
    return render(request, "pages/question_review.html", context)


@user_passes_test(is_admin)
@require_POST
def save_resource_quiz_config(request, resource_id):
    """Guarda la configuración de quiz de un recurso."""
    resource = get_object_or_404(Resource, id=resource_id)
    config, created = ResourceQuizConfig.objects.get_or_create(resource=resource)

    try:
        counts = {}
        for lvl in ["1", "2", "3"]:
            counts[lvl] = {
                "practice": {
                    "pool": int(request.POST.get(f"practice_pool_{lvl}", 15)),
                    "shown": int(request.POST.get(f"practice_shown_{lvl}", 5)),
                },
                "eval": {
                    "pool": int(request.POST.get(f"eval_pool_{lvl}", 10)),
                    "shown": int(request.POST.get(f"eval_shown_{lvl}", 3)),
                },
            }

        config.counts = counts
        config.max_attempts = int(request.POST.get("max_attempts", 3))
        # El umbral se ingresa de 0 a 100; tolerante a coma decimal.
        threshold_pct = float(str(request.POST.get("pass_threshold", "100")).replace(",", "."))
        config.pass_threshold = threshold_pct / 100.0
        config.recovery_rule = request.POST.get("recovery_rule", "practice_5_5")
        config.allow_retake_passed = request.POST.get("allow_retake_passed") in ["true", "on", "checked"]
        config.autopublish = request.POST.get("autopublish") in ["true", "on", "checked"]

        config.clean()
        config.save()

        if request.headers.get("HX-Request"):
            response = HttpResponse(
                '<div class="alert alert--success" role="alert" id="config-alert">'
                "Configuración guardada correctamente."
                '<button type="button" class="alert-close" aria-label="Cerrar">&times;</button>'
                "</div>"
            )
            response["HX-Trigger"] = "configUpdated"
            return response

        return redirect("content:question_review", slug=resource.slug)

    except Exception as e:
        error_msg = str(e)
        if request.headers.get("HX-Request"):
            return HttpResponse(
                f'<div class="alert alert--danger" role="alert" id="config-alert">'
                f"Error al guardar la configuración: {error_msg}"
                '<button type="button" class="alert-close" aria-label="Cerrar">&times;</button>'
                "</div>",
                status=400,
            )
        return HttpResponse(f"Error: {error_msg}", status=400)


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_question_inline(request, question_id):
    """GET: formulario de edición (o lectura si cancel). POST: guarda y devuelve el ítem."""
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.text = request.POST.get("text", "").strip()
        question.explanation = request.POST.get("explanation", "").strip()
        try:
            question.level = int(request.POST.get("level", 1))
            question.order = int(request.POST.get("order", 0))
        except ValueError:
            pass
        question.mode = request.POST.get("mode", "ambas")
        question.status = request.POST.get("status", "borrador")
        question.save()

        if request.headers.get("HX-Request"):
            # Devuelve el <details> completo (abierto) para refrescar resumen + cuerpo.
            return render(request, "partials/question_item.html", {"question": question, "open": True})
        return redirect("content:question_review", slug=question.resource.slug)

    # GET
    if request.GET.get("cancel"):
        return render(request, "partials/question_detail.html", {"question": question})
    return render(request, "partials/question_edit_form.html", {"question": question, **_edit_choices_ctx(question)})


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_choice_inline(request, choice_id):
    """GET: form de edición (o lectura si cancel). POST: guarda y devuelve la alternativa."""
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question

    if request.method == "POST":
        choice.text = request.POST.get("text", "").strip()
        is_correct = request.POST.get("is_correct") in ["true", "on", "checked"]

        with transaction.atomic():
            if is_correct:
                question.choices.all().update(is_correct=False)
            choice.is_correct = is_correct
            choice.save()

        correct_count = question.choices.filter(is_correct=True).count()
        warning = None
        if correct_count == 0:
            warning = "Sin alternativa correcta."
        elif correct_count > 1:
            warning = f"{correct_count} alternativas marcadas como correctas."

        if request.headers.get("HX-Request"):
            return render(request, "partials/choice_item.html", {"choice": choice, "warning": warning})
        return redirect("content:question_review", slug=question.resource.slug)

    # GET
    if request.GET.get("cancel"):
        return render(request, "partials/choice_item.html", {"choice": choice})
    return render(request, "partials/choice_edit_form.html", {"choice": choice})


@user_passes_test(is_admin)
@require_POST
def add_question_inline(request, resource_id):
    """Crea una pregunta en el nivel/modo indicados y devuelve el ítem (abierto)."""
    resource = get_object_or_404(Resource, id=resource_id)
    try:
        level = int(request.POST.get("level", 1))
    except (ValueError, TypeError):
        level = 1
    mode = request.POST.get("mode", "ambas")
    if mode not in dict(Question.MODE_CHOICES):
        mode = "ambas"

    last_order = Question.objects.filter(resource=resource, level=level).count()
    question = Question.objects.create(
        resource=resource,
        level=level,
        mode=mode,
        text="Nueva pregunta (editar aquí)",
        explanation="",
        status="borrador",
        order=last_order + 1,
    )
    Choice.objects.create(question=question, text="Alternativa A (correcta)", is_correct=True, order=1)
    Choice.objects.create(question=question, text="Alternativa B", is_correct=False, order=2)
    Choice.objects.create(question=question, text="Alternativa C", is_correct=False, order=3)
    Choice.objects.create(question=question, text="Alternativa D", is_correct=False, order=4)

    if request.headers.get("HX-Request"):
        return render(request, "partials/question_item.html", {"question": question, "open": True})
    return redirect("content:question_review", slug=resource.slug)


@user_passes_test(is_admin)
@require_POST
def add_choice_inline(request, question_id):
    """Crea una alternativa y devuelve su formulario de edición (para completarla)."""
    question = get_object_or_404(Question, id=question_id)
    last_order = question.choices.count()
    choice = Choice.objects.create(
        question=question, text="Nueva alternativa", is_correct=False, order=last_order + 1
    )
    if request.headers.get("HX-Request"):
        return render(request, "partials/choice_edit_form.html", {"choice": choice})
    return redirect("content:question_review", slug=question.resource.slug)


@user_passes_test(is_admin)
@require_POST
def delete_question(request, question_id):
    """Elimina la pregunta. Retorna vacío para que HTMX remueva el ítem."""
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def delete_choice(request, choice_id):
    """Elimina la alternativa. Retorna vacío para que HTMX la remueva."""
    choice = get_object_or_404(Choice, id=choice_id)
    choice.delete()
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def bulk_action_questions(request, resource_id):
    """Acción en lote sobre preguntas seleccionadas. Devuelve HTML HTMX o redirige."""
    resource = get_object_or_404(Resource, id=resource_id)
    action = request.POST.get("action")
    question_ids = request.POST.getlist("selected_questions")
    level = request.POST.get("level")
    mode_key = request.POST.get("mode")

    if question_ids:
        qs_target = Question.objects.filter(resource=resource, id__in=question_ids)
        if action == "publicar":
            qs_target.update(status="publicada")
        elif action == "borrador":
            qs_target.update(status="borrador")
        elif action == "archivar":
            qs_target.update(status="archivada")
        elif action == "eliminar":
            qs_target.delete()

    if request.headers.get("HX-Request") and level and mode_key:
        qs = (
            Question.objects.filter(resource=resource, level=level, mode=mode_key)
            .prefetch_related("choices")
            .order_by("order", "id")
        )
        parts = [
            render_to_string("partials/question_item.html", {"question": q}, request=request)
            for q in qs
        ]
        if not parts:
            parts = ['<p class="acc-empty">Sin preguntas en esta sección todavía.</p>']
        return HttpResponse("".join(parts))

    return redirect("content:question_review", slug=resource.slug)
