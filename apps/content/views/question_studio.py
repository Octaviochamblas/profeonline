import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

from apps.content.views.permissions import is_admin
from apps.content.models import Area, Question, Resource, ResourceQuizConfig
from apps.content.services.ai_generation_service import generate_questions_for_resource

# Tamaño máximo de preguntas generadas por petición HTTP. Mantenerlo chico evita
# chocar con el timeout de gunicorn (~30s en prod): ~5 preguntas ≈ 15s con Gemini.
GENERATION_BATCH_SIZE = 5


def _sum_pool(counts_data):
    """Suma todos los pools (nivel×modo) de un recurso según la matriz de counts."""
    total = 0
    for lvl in ["1", "2", "3"]:
        for m in ["practice", "eval"]:
            try:
                total += int(counts_data.get(lvl, {}).get(m, {}).get("pool", 0))
            except (ValueError, TypeError):
                pass
    return total


def _next_cell(level, mode):
    """Siguiente celda (nivel, modo) dentro de un recurso. (None, None) si terminó.

    Orden: (1,practice)→(1,eval)→(2,practice)→(2,eval)→(3,practice)→(3,eval).
    """
    if mode == "practice":
        return level, "eval"
    if level < 3:
        return level + 1, "practice"
    return None, None


@user_passes_test(is_admin)
def question_studio(request):
    """GET renderiza el selector de recursos para generar preguntas.
    POST inicializa el proceso por lotes (tandas) y renderiza el contenedor de progreso.
    """
    if request.method == "POST":
        # Obtener los IDs de recursos seleccionados
        resource_ids = request.POST.getlist('resources')
        if not resource_ids:
            return HttpResponse(
                '<div class="alert alert--danger">Debe seleccionar al menos un recurso.</div>',
                status=400
            )

        # Mapeamos la matriz de counts desde los inputs
        counts_data = {}
        for lvl in ["1", "2", "3"]:
            practice_pool = int(request.POST.get(f'practice_pool_{lvl}', 15))
            practice_shown = int(request.POST.get(f'practice_shown_{lvl}', 5))
            eval_pool = int(request.POST.get(f'eval_pool_{lvl}', 10))
            eval_shown = int(request.POST.get(f'eval_shown_{lvl}', 3))

            counts_data[lvl] = {
                "practice": {"pool": practice_pool, "shown": practice_shown},
                "eval": {"pool": eval_pool, "shown": eval_shown}
            }

        max_attempts = int(request.POST.get('max_attempts', 3))
        # Tolerante a coma decimal (locale es-*) además de punto.
        pass_threshold = float(str(request.POST.get('pass_threshold', '100')).replace(',', '.')) / 100.0
        recovery_rule = request.POST.get('recovery_rule', 'practice_5_5')
        allow_retake_passed = request.POST.get('allow_retake_passed') in ['true', 'on', 'checked']
        autopublish = request.POST.get('autopublish') in ['true', 'on', 'checked']
        education_level_override = request.POST.get('education_level_override', 'media')
        # Modo de generación: "video" (transcript) o "document" (copia formato de guías).
        gen_source = request.POST.get('gen_source', 'video')
        if gen_source not in ('video', 'document'):
            gen_source = 'video'

        # Instrucciones personalizadas por nivel/modo (ej. {"1_practice": "...", "2_eval": "..."})
        custom_instructions = {}
        for lvl in ["1", "2", "3"]:
            for m in ["practice", "eval"]:
                val = request.POST.get(f'gen_instructions_{lvl}_{m}', '').strip()
                if val:
                    custom_instructions[f"{lvl}_{m}"] = val

        # Estructura del plan inicial
        vals = {
            "resource_ids": [int(rid) for rid in resource_ids],
            "current_index": 0,
            "level": 1,
            "mode": "practice",
            "batch_offset": 0,
            "generated_total": 0,
            "autopublish": autopublish,
            "max_attempts": max_attempts,
            "pass_threshold": pass_threshold,
            "recovery_rule": recovery_rule,
            "allow_retake_passed": allow_retake_passed,
            "counts_data": json.dumps(counts_data),
            "education_level_override": education_level_override,
            "custom_instructions_json": json.dumps(custom_instructions),
            "gen_source": gen_source,
        }

        # Total a generar, en preguntas (el progreso se mide por preguntas creadas).
        total_questions = _sum_pool(counts_data) * len(resource_ids)

        return render(request, 'partials/generation_progress_container.html', {
            'vals': vals,
            'total_questions': total_questions,
            'resource_count': len(resource_ids)
        })

    # GET — árbol jerárquico Área → Asignatura → Tema (+ "Sin tema") → Recursos.
    # Se arma en la vista (no en el template) para agrupar los recursos sin tema y
    # omitir ramas vacías. Prefetch para evitar N+1.
    areas = Area.objects.filter(is_active=True).prefetch_related(
        'subjects__topics__resources', 'subjects__resources'
    ).order_by('order')

    tree = []
    for area in areas:
        subjects_data = []
        for subject in area.subjects.all():
            topics_data = []
            for topic in subject.topics.all():
                topic_resources = list(topic.resources.all())
                if topic_resources:
                    topics_data.append({'topic': topic, 'resources': topic_resources})
            sin_tema = [r for r in subject.resources.all() if r.topic_id is None]
            if topics_data or sin_tema:
                subjects_data.append({
                    'subject': subject,
                    'topics': topics_data,
                    'sin_tema': sin_tema,
                })
        if subjects_data:
            tree.append({'area': area, 'subjects': subjects_data})

    from apps.content.models.resource_quiz_config import default_quiz_counts
    context = {
        'tree': tree,
        'default_counts': default_quiz_counts(),
        'RECOVERY_CHOICES': ResourceQuizConfig.RECOVERY_CHOICES,
        'LEVEL_CHOICES': Question.LEVEL_CHOICES,
    }
    return render(request, 'pages/question_studio.html', context)


@user_passes_test(is_admin)
@require_POST
def generate_questions_chunk(request):
    """Genera un lote chico (≤GENERATION_BATCH_SIZE) de una celda (recurso, nivel, modo).

    El front encadena llamadas hasta completar toda la matriz. Cada petición es corta
    para no superar el timeout de gunicorn.
    """
    # Manejar los IDs del recurso
    resource_ids_raw = request.POST.getlist('resource_ids[]')
    if not resource_ids_raw:
        try:
            resource_ids_raw = json.loads(request.POST.get('resource_ids', '[]'))
        except ValueError:
            resource_ids_raw = []

    if not resource_ids_raw:
        resource_ids_raw = [int(x) for x in request.POST.getlist('resource_ids') if x]

    resource_ids = [int(rid) for rid in resource_ids_raw]
    current_index = int(request.POST.get('current_index', 0))
    level = int(request.POST.get('level', 1))
    mode = request.POST.get('mode', 'practice')  # 'practice' o 'eval'
    batch_offset = int(request.POST.get('batch_offset', 0))
    generated_total = int(request.POST.get('generated_total', 0))
    autopublish = request.POST.get('autopublish') in ['true', 'on', 'checked', True]
    max_attempts = int(request.POST.get('max_attempts', 3))
    # Tolerante a coma decimal (locale es-*) además de punto.
    pass_threshold = float(str(request.POST.get('pass_threshold', '1.0')).replace(',', '.'))
    recovery_rule = request.POST.get('recovery_rule', 'practice_5_5')
    allow_retake_passed = request.POST.get('allow_retake_passed') in ['true', 'on', 'checked', True]
    counts_data = json.loads(request.POST.get('counts_data', '{}'))
    education_level_override = request.POST.get('education_level_override', 'media')
    custom_instructions_json = request.POST.get('custom_instructions_json', '{}')
    gen_source = request.POST.get('gen_source', 'video')  # "video" o "document"
    try:
        custom_instructions_map = json.loads(custom_instructions_json)
    except (json.JSONDecodeError, ValueError):
        custom_instructions_map = {}

    total_questions = _sum_pool(counts_data) * len(resource_ids)

    # Si por alguna razón el índice está fuera del rango
    if current_index >= len(resource_ids):
        return render(request, 'partials/generation_completed.html', {
            'total_questions': total_questions,
            'resource_count': len(resource_ids),
        })

    resource_id = resource_ids[current_index]
    resource = get_object_or_404(Resource.objects.select_related("topic"), id=resource_id)

    # Nivel educativo: del tema o la asignatura del recurso; si no, el override del form.
    edu_level = resource.get_education_level() or education_level_override

    # 1. Guardar/actualizar config UNA sola vez por recurso (primera celda, primer lote).
    if level == 1 and mode == "practice" and batch_offset == 0:
        config, _ = ResourceQuizConfig.objects.get_or_create(resource=resource)
        config.counts = counts_data
        config.max_attempts = max_attempts
        config.pass_threshold = pass_threshold
        config.recovery_rule = recovery_rule
        config.allow_retake_passed = allow_retake_passed
        config.autopublish = autopublish
        config.save()

    # 2. Calcular el lote actual de esta celda.
    model_mode = "preparacion" if mode == "practice" else "evaluacion"
    mode_label = "práctica" if mode == "practice" else "evaluación"
    level_str = str(level)
    pool = int(counts_data.get(level_str, {}).get(mode, {}).get('pool', 0))
    remaining = max(0, pool - batch_offset)
    batch = min(GENERATION_BATCH_SIZE, remaining)

    if batch > 0:
        try:
            instr_key = f"{level}_{mode}"  # e.g. "1_practice"
            custom_instr = custom_instructions_map.get(instr_key) or None
            created = generate_questions_for_resource(
                resource=resource,
                level=level,
                mode=model_mode,
                count=batch,
                status="publicada" if autopublish else "borrador",
                education_level=edu_level,
                custom_instructions=custom_instr,
                use_transcript=(gen_source == "video"),
                use_guides=True,
            )
            n_created = len(created)
            generated_total += n_created
            done_in_cell = batch_offset + n_created
            log_msg = (
                f"'{resource.title}' · N{level} {mode_label}: "
                f"+{n_created} ({done_in_cell}/{pool})."
            )
            log_status = "success"
        except Exception as e:
            log_msg = f"Error en '{resource.title}' (N{level} {mode_label}): {str(e)}"
            log_status = "error"
    else:
        log_msg = f"'{resource.title}' · N{level} {mode_label}: sin pool configurado, omitido."
        log_status = "info"

    # 3. Avanzar el estado. Avanzamos por 'batch' (lo intentado) para no quedar en bucle.
    new_offset = batch_offset + max(batch, 0)
    if new_offset >= pool:
        nl, nm = _next_cell(level, mode)
        if nl is None:
            next_index = current_index + 1
            next_level, next_mode, next_offset = 1, "practice", 0
        else:
            next_index, next_level, next_mode, next_offset = current_index, nl, nm, 0
    else:
        next_index, next_level, next_mode, next_offset = current_index, level, mode, new_offset

    finished = next_index >= len(resource_ids)
    percentage = min(100, round((generated_total / total_questions) * 100)) if total_questions > 0 else 100

    next_vals = None
    if not finished:
        next_vals = {
            "resource_ids": resource_ids,
            "current_index": next_index,
            "level": next_level,
            "mode": next_mode,
            "batch_offset": next_offset,
            "generated_total": generated_total,
            "autopublish": autopublish,
            "max_attempts": max_attempts,
            "pass_threshold": pass_threshold,
            "recovery_rule": recovery_rule,
            "allow_retake_passed": allow_retake_passed,
            "counts_data": json.dumps(counts_data),
            "education_level_override": education_level_override,
            "custom_instructions_json": custom_instructions_json,
            "gen_source": gen_source,
        }

    context = {
        'log_msg': log_msg,
        'log_status': log_status,
        'percentage': percentage,
        'finished': finished,
        'generated_total': generated_total,
        'total_questions': total_questions,
        'next_vals': next_vals,
    }
    return render(request, 'partials/generation_step_result.html', context)
