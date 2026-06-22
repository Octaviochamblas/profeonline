"""Servicio para la generación asistida de preguntas por IA."""

import json
import hashlib
import logging
import os
import random
import sys
import time
import requests
from django.conf import settings
from apps.content.models import Choice, Question

logger = logging.getLogger(__name__)


_EDUCATION_DESCRIPTIONS = {
    "escolar": (
        "Escolar (hasta 13 años) — usa vocabulario simple y cotidiano, sin álgebra abstracta, "
        "ejemplos concretos del día a día (objetos, cantidades pequeñas, situaciones familiares)."
    ),
    "media": (
        "Media preuniversitaria (14-17 años) — usa vocabulario técnico básico, álgebra introductoria, "
        "ejemplos del mundo real y aplicaciones prácticas."
    ),
    "universitaria": (
        "Universitaria (18+) — usa terminología formal, demostraciones rigurosas, "
        "notación matemática avanzada y referencias a teoremas o definiciones formales."
    ),
}


def _existing_question_texts(resource, limit=80):
    """Enunciados ya existentes del recurso (no archivados) para evitar repetir."""
    return list(
        Question.objects.filter(resource=resource)
        .exclude(status="archivada")
        .order_by("-id")
        .values_list("text", flat=True)[:limit]
    )


def generate_questions_for_resource(resource, level, mode="ambas", count=3, api_key=None, status="publicada", education_level=None, custom_instructions=None, transcript=None, use_transcript=True, reference_guides=None, use_guides=True, existing_questions=None, avoid_existing=True):
    """Genera preguntas para un recurso usando Gemini o OpenAI en el estado especificado.

    Si no se provee ni se encuentra una API key en settings/entorno, y settings.DEBUG es True,
    se genera un conjunto de preguntas simuladas (mock) realistas basadas en el recurso.
    """
    is_testing = "test" in sys.argv or getattr(settings, "TESTING", False) or "test" in getattr(settings, "SETTINGS_MODULE", "")

    gemini_key = api_key
    if gemini_key is None:
        gemini_key = getattr(settings, "GEMINI_API_KEY", None)
        if is_testing and gemini_key == os.environ.get("GEMINI_API_KEY", ""):
            gemini_key = ""
        elif gemini_key is None and not is_testing:
            gemini_key = os.environ.get("GEMINI_API_KEY", "")
        elif gemini_key is None:
            gemini_key = ""

    openai_key = api_key
    if openai_key is None:
        openai_key = getattr(settings, "OPENAI_API_KEY", None)
        if is_testing and openai_key == os.environ.get("OPENAI_API_KEY", ""):
            openai_key = ""
        elif openai_key is None and not is_testing:
            openai_key = os.environ.get("OPENAI_API_KEY", "")
        elif openai_key is None:
            openai_key = ""


    # Si no hay llaves configuradas y estamos en DEBUG o ejecutando tests, usar el generador simulado
    if not gemini_key and not openai_key:
        if settings.DEBUG or is_testing:
            return _generate_mock_questions(resource, level, mode, count, status)
        raise ValueError("No se configuraron las llaves GEMINI_API_KEY u OPENAI_API_KEY.")

    # Transcript: se PREFIERE el guardado en el recurso (bajado aparte desde una IP
    # residencial y persistido). Solo si no hay guardado se intenta en vivo —que en
    # la nube suele estar bloqueado por YouTube—. Va DESPUÉS del camino mock para no
    # hacer red durante los tests.
    if transcript is None and use_transcript:
        transcript = (getattr(resource, "transcript", "") or "").strip() or None
        if not transcript and getattr(resource, "video_url", None):
            from apps.content.services.transcript_service import fetch_transcript
            transcript = fetch_transcript(resource.video_url, max_chars=8000)

    # Guías de referencia del recurso (estilo a mimetizar + contenido como fuente).
    if reference_guides is None and use_guides:
        from apps.content.services.guide_service import build_reference_block
        reference_guides = build_reference_block(resource)

    # Preguntas ya existentes del recurso: se le pasan a la IA para que NO las repita.
    if existing_questions is None and avoid_existing:
        existing_questions = _existing_question_texts(resource)

    questions_data = generate_question_candidates(
        resource=resource,
        level=level,
        mode=mode,
        count=count,
        api_key=api_key,
        education_level=education_level,
        custom_instructions=custom_instructions,
        transcript=transcript,
        reference_guides=reference_guides,
        gemini_key=gemini_key,
        openai_key=openai_key,
        existing_questions=existing_questions,
    )

    created_questions = _save_questions(resource, level, mode, questions_data, status)
    return created_questions


def generate_question_candidates(
    resource,
    level,
    mode="ambas",
    count=3,
    api_key=None,
    education_level=None,
    custom_instructions=None,
    transcript=None,
    reference_guides=None,
    gemini_key=None,
    openai_key=None,
    existing_questions=None,
):
    """Genera candidatos sin persistirlos para permitir una auditoría previa."""
    if gemini_key is None:
        gemini_key = api_key or getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", "")
    if openai_key is None:
        openai_key = api_key or getattr(settings, "OPENAI_API_KEY", None) or os.environ.get("OPENAI_API_KEY", "")

    prompt = _build_prompt(
        resource,
        level,
        mode,
        count,
        education_level,
        custom_instructions,
        transcript=transcript,
        reference_guides=reference_guides,
        existing_questions=existing_questions,
    )
    prompt += (
        "\nIncluye además `cognitive_type` en cada objeto con uno de: "
        "recuerdo, comprension, aplicacion, analisis."
    )
    if gemini_key:
        return _call_gemini_api(prompt, gemini_key)
    if openai_key:
        return _call_openai_api(prompt, openai_key)
    raise ValueError("No se configuraron las llaves GEMINI_API_KEY u OPENAI_API_KEY.")



def _build_prompt(resource, level, mode, count, education_level=None, custom_instructions=None, transcript=None, reference_guides=None, existing_questions=None):
    """Construye el prompt pedagógico para la IA."""
    level_name = dict(Question.LEVEL_CHOICES).get(level, f"Nivel {level}")
    edu_desc = _EDUCATION_DESCRIPTIONS.get(education_level or "", _EDUCATION_DESCRIPTIONS["media"])

    existing_block = ""
    if existing_questions:
        listado = "\n".join(f"- {texto}" for texto in existing_questions if texto)
        if listado:
            existing_block = (
                "\n- PREGUNTAS YA EXISTENTES EN ESTE RECURSO (NO las repitas ni generes "
                "variantes triviales —mismo enunciado con otros números o nombres—; aporta "
                "preguntas genuinamente distintas que cubran otros aspectos del tema):\n"
                f"{listado[:4000]}\n"
            )

    transcript_block = ""
    if transcript:
        transcript_block = (
            "\n- Transcripción real del video (FUENTE PRINCIPAL): basa las preguntas en lo "
            "que efectivamente se explica y se resuelve aquí —el método, los pasos y los "
            "ejemplos concretos usados—, no solo en el título o la descripción:\n"
            f"{transcript[:6000]}\n"
        )

    guides_block = ""
    if reference_guides:
        guides_block = (
            "\n- GUÍA(S) DE REFERENCIA del profesor (IMITA SU ESTILO): replica el tipo de "
            "ejercicios, el formato de los enunciados y la forma de evaluar de estas guías, "
            "y usa su contenido como base de las preguntas. Este estilo tiene prioridad:\n"
            f"{reference_guides[:5000]}\n"
        )

    # Bloques con LaTeX: se definen como raw strings para que las barras
    # invertidas y las llaves de LaTeX no choquen con el f-string del prompt.
    notation_block = (
        r"""NOTACIÓN MATEMÁTICA (OBLIGATORIO — la plataforma renderiza LaTeX con KaTeX):
- Escribe TODA expresión matemática en LaTeX entre delimitadores, nunca en texto plano:
    · En línea (dentro de una frase):  $...$       ej.  la solución es $x = \frac{-b}{2a}$
    · En bloque (ecuación centrada):   $$...$$      ej.  $$\int_0^1 x^2\,dx = \frac{1}{3}$$
- Úsalo en el enunciado, en las 4 alternativas y en la explicación.
- Aprovecha: potencias $x^2$, subíndices $a_1$, fracciones $\frac{a}{b}$, raíces $\sqrt{x}$ y $\sqrt[3]{x}$,
  sumatorias $\sum_{i=1}^n i$, integrales $\int$, derivadas $\frac{d}{dx}f(x)$, límites $\lim_{x\to 0}$,
  matrices $\begin{pmatrix}1&2\\3&4\end{pmatrix}$, símbolos $\pi$, $\theta$, $\leq$, $\Rightarrow$.
- Prohibido escribir matemática como "x^2", "raíz de x" o "1/2": usa siempre LaTeX.
- JSON: escapa las barras invertidas como dobles. Debe ir "$\\frac{a}{b}$" (con \\), nunca "$\frac{a}{b}$"."""
    )

    json_example = (
        r"""[
  {
    "text": "¿Cuál es el valor de $\\int_0^1 2x\\,dx$?",
    "explanation": "1. La integral de $2x$ es $x^2$.\n2. Evaluamos entre $0$ y $1$: $1^2 - 0^2 = 1$.\n3. El resultado es $1$.",
    "choices": [
      {"text": "$1$", "is_correct": true},
      {"text": "$2$", "is_correct": false},
      {"text": "$\\frac{1}{2}$", "is_correct": false},
      {"text": "$x^2$", "is_correct": false}
    ]
  }
]"""
    )

    prompt = f"""Eres un experto pedagogo en matemáticas y ciencias para la plataforma 'ProfeOnline'.
Tu tarea es generar exactamente {count} preguntas de opción múltiple de alta calidad pedagógica sobre el siguiente contenido educativo.

REGLA CRÍTICA: Las preguntas deben evaluar si el estudiante comprendió los conceptos, NO mencionar nunca "el recurso", "la lección", "el texto", "el documento" ni ningún título. Redacta como si el estudiante ya hubiera estudiado el tema y le estuvieras evaluando directamente.

{notation_block}

CONTENIDO EDUCATIVO:
- Tema: {resource.topic.name if resource.topic else "General"}
- Asignatura: {resource.subject.name if resource.subject else "General"}
- Descripción: {resource.description}
- Desarrollo del tema:
{resource.content[:2000]}
{transcript_block}
{guides_block}
{existing_block}

DIRECTRICES DEL NIVEL PEDAGÓGICO:
Genera las preguntas para el Nivel {level} ({level_name}). Los tres niveles forman una
progresión; respeta el alcance del nivel solicitado y no lo mezcles con los otros.

Nivel 1 — Comprensión conceptual y funcional.
El estudiante identifica los conceptos centrales, comprende para qué sirven, cuándo se
utilizan y cuál es su lógica básica. Las preguntas deben evaluar que pueda explicar el
contenido con sus propias palabras, reconocer su utilidad y distinguir un concepto de
otro: significado, propósito, condiciones de uso y relaciones entre ideas. NO pidas
resolución numérica ni cálculos en este nivel. Los distractores deben reflejar
confusiones conceptuales típicas (confundir dos términos parecidos, atribuir mal una
propiedad, equivocarse en "cuándo se aplica").

Nivel 2 — Dominio procedimental y resolución técnica.
El estudiante aplica fórmulas, reglas, algoritmos o procedimientos para resolver
ejercicios de dificultad progresiva. No basta con reemplazar datos en una fórmula: la
pregunta debe exigir que identifique qué procedimiento corresponde, ordene la información
disponible, desarrolle los pasos de forma lógica y obtenga el resultado correcto. Cuando
sea pertinente, evalúa también la capacidad de justificar por qué se usa una fórmula,
interpretar cada variable, cuidar las unidades de medida, verificar si el resultado es
razonable y detectar errores de cálculo o de planteamiento. Varía la dificultad: desde
ejercicios estructurados donde se indica qué fórmula usar, hasta otros donde el estudiante
deba decidir el método adecuado. Los distractores deben representar errores procedimentales
reales (error de signo, fórmula equivocada, paso omitido, unidades mal convertidas,
resultado no razonable).

Nivel 3 — Transferencia y aplicación en contextos reales.
El estudiante usa lo aprendido para analizar situaciones reales o casos prácticos. La
pregunta debe presentar un escenario nuevo y exigir que interprete la información, escoja
el método adecuado entre varios posibles, justifique sus decisiones y adapte el
conocimiento al contexto. Prioriza enunciados contextualizados y de varios pasos, donde
el dato relevante deba extraerse del problema (no venir "servido"). Los distractores deben
reflejar errores de interpretación o de modelado (elegir el método equivocado, usar un
dato irrelevante, trasladar mal el contexto a la fórmula).

NIVEL EDUCATIVO DEL ESTUDIANTE:
{edu_desc}

DIRECTRICES DEL MODO DE PREGUNTA:
Modo solicitado: {mode} (puede usarse para 'preparacion', 'evaluacion' o 'ambas').

DIRECTRICES DE LAS ALTERNATIVAS:
1. Proporciona exactamente 4 alternativas por pregunta.
2. Exactamente UNA alternativa debe ser correcta (`is_correct` = true).
3. Las otras 3 alternativas (distractores) deben ser incorrectas pero plausibles, representando errores típicos de los estudiantes (por ejemplo, error de signo, olvidar un paso, etc.).
4. Incluye una explicación clara de la respuesta correcta.

DIRECTRICES DE LA EXPLICACIÓN (importante para la legibilidad):
- Cuando la resolución tenga varios pasos, numéralos ("1. ", "2. ", "3. ...") y separa cada
  paso con un salto de línea real (carácter \\n en el JSON). NO juntes todos los pasos en un
  solo párrafo corrido.
- Cada paso debe ser una idea concreta y corta (un cálculo o una afirmación por línea).
- Toda fórmula o cálculo dentro de la explicación también va en LaTeX ($...$ / $$...$$).

FORMATO DE SALIDA REQUERIDO (JSON):
Debes responder ÚNICAMENTE con una estructura JSON válida que sea una lista de objetos con el siguiente formato, sin bloques de código markdown, explicaciones previas o posteriores:

{json_example}
"""
    if custom_instructions:
        prompt += f"\n\nINSTRUCCIONES ADICIONALES DEL PROFESOR:\n{custom_instructions}\n"
    return prompt


# Reintentos ante límite de cuota (429) o saturación temporal (503) de la API.
_RETRY_STATUSES = (429, 503)
_MAX_RETRIES = 5
_BACKOFF_BASE = 4.0  # segundos: 4, 8, 16, 32...


def _sanitize_key(text, key):
    """Evita que la API key quede en mensajes de error o logs."""
    if key and text:
        return text.replace(key, "***")
    return text


def _post_json_with_retry(url, headers, payload, key=None):
    """POST con reintentos exponenciales ante 429/503; nunca expone la API key.

    Devuelve el ``response`` exitoso. Lanza ``RuntimeError`` (con la key saneada)
    si tras los reintentos la API sigue limitada o responde con error.
    """
    for attempt in range(_MAX_RETRIES):
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        if response.status_code in _RETRY_STATUSES and attempt < _MAX_RETRIES - 1:
            wait = _BACKOFF_BASE * (2 ** attempt)
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    wait = max(wait, float(retry_after))
                except (TypeError, ValueError):
                    pass
            logger.warning(
                "IA saturada (HTTP %s). Reintento %d/%d en %.0fs.",
                response.status_code, attempt + 1, _MAX_RETRIES - 1, wait,
            )
            time.sleep(wait)
            continue
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(_sanitize_key(str(exc), key)) from None
        return response

    raise RuntimeError("La IA sigue limitada (429/503) tras varios reintentos.")


def _call_gemini_api(prompt, key):
    """Llama a Gemini 2.5 Flash. La key va en header (no en la URL) y con reintentos."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": key}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    try:
        response = _post_json_with_retry(url, headers, payload, key=key)
        data = response.json()
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_response.strip())
    except RuntimeError:
        raise
    except Exception as e:
        msg = _sanitize_key(str(e), key)
        logger.error("Error llamando a Gemini API: %s", msg)
        raise RuntimeError(f"Error de generación con Gemini: {msg}") from None


def _call_openai_api(prompt, key):
    """Llama a OpenAI (GPT-4o-mini). Key en header Authorization y con reintentos."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
    }
    try:
        response = _post_json_with_retry(url, headers, payload, key=key)
        data = response.json()
        text_response = data["choices"][0]["message"]["content"]
        # OpenAI puede devolver un objeto con una clave raíz como "questions".
        parsed = json.loads(text_response.strip())
        if isinstance(parsed, dict):
            for value in parsed.values():
                if isinstance(value, list):
                    return value
        return parsed
    except RuntimeError:
        raise
    except Exception as e:
        msg = _sanitize_key(str(e), key)
        logger.error("Error llamando a OpenAI API: %s", msg)
        raise RuntimeError(f"Error de generación con OpenAI: {msg}") from None


def _save_questions(
    resource,
    level,
    mode,
    questions_data,
    status="publicada",
    publication_item=None,
    audit_data_by_index=None,
):
    """Guarda las preguntas y alternativas en la base de datos."""
    created_questions = []

    # Asegurar que questions_data sea una lista
    if isinstance(questions_data, dict):
        if "questions" in questions_data:
            questions_data = questions_data["questions"]
        elif "preguntas" in questions_data:
            questions_data = questions_data["preguntas"]
        else:
            # Buscar cualquier lista dentro del dict
            for v in questions_data.values():
                if isinstance(v, list):
                    questions_data = v
                    break

    if not isinstance(questions_data, list):
        raise ValueError("El formato retornado por la IA no contiene una lista de preguntas válida.")

    # Determinar el orden inicial para nuevas preguntas
    last_order = Question.objects.filter(resource=resource, level=level).count()

    audit_data_by_index = audit_data_by_index or {}
    for item_index, item in enumerate(questions_data):
        text = item.get("text") or item.get("enunciado")
        explanation = item.get("explanation") or item.get("explicacion", "")
        choices = item.get("choices") or item.get("alternativas") or item.get("options")

        if not text or not choices:
            continue

        question = Question.objects.create(
            resource=resource,
            level=level,
            mode=mode,
            text=text,
            explanation=explanation,
            status=status,
            order=last_order + 1,
            publication_item=publication_item,
            generation_key=(
                hashlib.sha256(
                    f"{level}|{mode}|{' '.join(text.lower().split())}".encode("utf-8")
                ).hexdigest()
                if publication_item
                else ""
            ),
            audit_data=audit_data_by_index.get(item_index, {}),
        )
        last_order += 1

        choice_objs = []
        for idx, choice_data in enumerate(choices):
            if isinstance(choice_data, dict):
                c_text = choice_data.get("text") or choice_data.get("texto")
                c_correct = choice_data.get("is_correct") or choice_data.get("correcta") or False
            else:
                # Si viene como simple string, asumimos primera correcta o falsa
                c_text = str(choice_data)
                c_correct = idx == 0

            choice_objs.append(
                Choice(
                    question=question,
                    text=c_text,
                    is_correct=bool(c_correct),
                    order=idx + 1
                )
            )

        Choice.objects.bulk_create(choice_objs)
        created_questions.append(question)

    return created_questions


def _generate_mock_questions(resource, level, mode, count, status="publicada"):
    """Genera preguntas simuladas basadas en el tema y título del recurso."""
    title_lower = resource.title.lower()
    subject_name = resource.subject.name if resource.subject else ""
    topic_name = resource.topic.name if resource.topic else ""

    # Determinar la temática principal
    is_math = "matematica" in subject_name.lower() or any(
        kw in title_lower or kw in topic_name.lower()
        for kw in ["fracci", "ecuaci", "multiplic", "divis", "algebr", "aritme", "geomet", "angulo", "triang", "funcion"]
    )

    questions_data = []

    for i in range(count):
        num = i + 1
        if is_math:
            if level == 1:
                text = f"¿Cuál de las siguientes opciones define correctamente el concepto principal de '{resource.title}'?"
                choices = [
                    {"text": f"Es la representación conceptual de la operación fundamental explicada en '{resource.title}'.", "is_correct": True},
                    {"text": "Es simplemente un método gráfico sin valor de cálculo algebraico.", "is_correct": False},
                    {"text": "Es el valor numérico obtenido únicamente cuando el divisor es cero.", "is_correct": False},
                    {"text": "Corresponde a la suma indeterminada de variables sin coeficientes.", "is_correct": False},
                ]
                explanation = "La definición conceptual se fundamenta en la operación explicada directamente en el desarrollo teórico."
            elif level == 2:
                # Ejercicios mecánicos simples
                val1 = random.randint(2, 9)
                val2 = random.randint(2, 9)
                ans = val1 * val2
                text = f"Si aplicamos el método básico de '{resource.title}' para resolver con los valores {val1} y {val2}, ¿cuál es el resultado directo?"
                choices = [
                    {"text": f"El resultado es {ans}.", "is_correct": True},
                    {"text": f"El resultado es {ans + val1}.", "is_correct": False},
                    {"text": f"El resultado es {ans - val2}.", "is_correct": False},
                    {"text": f"El resultado es {val1 + val2}.", "is_correct": False},
                ]
                explanation = f"El ejercicio se resuelve multiplicando directamente los valores propuestos: {val1} * {val2} = {ans}."
            else:
                # Problemas de aplicación
                text = (
                    f"Un estudiante tiene una situación práctica sobre '{resource.title}': necesita calcular el rendimiento total. "
                    "Si dispone de 120 unidades iniciales y cada paso duplica el remanente en base a la proporción establecida, ¿cuántas unidades tendrá al cabo del proceso?"
                )
                choices = [
                    {"text": "Tendrá 240 unidades, aplicando la duplicación directa.", "is_correct": True},
                    {"text": "Tendrá 120 unidades, pues no hay variación neta.", "is_correct": False},
                    {"text": "Tendrá 480 unidades, duplicando dos veces erróneamente.", "is_correct": False},
                    {"text": "Tendrá 60 unidades, debido a una reducción por mala interpretación del enunciado.", "is_correct": False},
                ]
                explanation = "Aplicando la proporción de duplicación directa, 120 unidades * 2 = 240 unidades en total."
        else:
            # Ciencia o general
            if level == 1:
                text = f"De acuerdo con la teoría presentada en '{resource.title}', ¿cuál de los siguientes enunciados describe su principio fundamental?"
                choices = [
                    {"text": "Describe el comportamiento y las características estructurales del fenómeno observado.", "is_correct": True},
                    {"text": "Postula que todos los elementos reaccionan de manera aleatoria y sin leyes fijas.", "is_correct": False},
                    {"text": "Determina que el fenómeno solo ocurre bajo condiciones extremas de laboratorio.", "is_correct": False},
                    {"text": "Establece que la energía se disipa por completo sin dejar rastro medible.", "is_correct": False},
                ]
                explanation = "El principio básico se centra en estructurar y clasificar el comportamiento del fenómeno para su estudio sistemático."
            elif level == 2:
                text = f"En relación al recurso '{resource.title}', si se observa el fenómeno bajo un aumento de 5 unidades de control, ¿cuál es el efecto esperado?"
                choices = [
                    {"text": "Un incremento proporcional en la velocidad de reacción y estabilidad.", "is_correct": True},
                    {"text": "Una anulación completa de todas las propiedades químicas y físicas.", "is_correct": False},
                    {"text": "Un descenso que congela el sistema de manera permanente.", "is_correct": False},
                    {"text": "Una duplicación del volumen sin alterar la densidad molecular.", "is_correct": False},
                ]
                explanation = "El aumento del control estabiliza el fenómeno y acelera proporcionalmente su velocidad de acuerdo con la gráfica teórica."
            else:
                text = (
                    f"Al diseñar un experimento real basado en '{resource.title}', un investigador coloca una muestra expuesta y otra de control. "
                    "Si la muestra expuesta reacciona positivamente y el control se mantiene neutro, ¿qué conclusión pedagógica se deriva?"
                )
                choices = [
                    {"text": "Que la variable independiente modificada es la responsable directa del cambio.", "is_correct": True},
                    {"text": "Que el experimento falló y debe repetirse completamente.", "is_correct": False},
                    {"text": "Que ambas muestras sufrieron contaminación externa simultánea.", "is_correct": False},
                    {"text": "Que no existe relación causal alguna entre las variables analizadas.", "is_correct": False},
                ]
                explanation = "La diferencia en los resultados de la muestra de prueba y de control valida la hipótesis de la variable independiente."

        questions_data.append({
            "text": f"[Simulado N{level}] {text}",
            "explanation": explanation,
            "choices": choices
        })

    return _save_questions(resource, level, mode, questions_data, status)
