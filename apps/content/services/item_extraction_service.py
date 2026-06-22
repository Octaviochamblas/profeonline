"""Servicio para la extracción de ítems de aprendizaje de una guía privada usando IA."""

import os
import sys
import logging
from django.conf import settings

from apps.content.models.question import Question
from apps.content.services.ai_generation_service import (
    _call_gemini_api,
    _call_openai_api,
    _loads_ai_json,
    _sanitize_key,
)

logger = logging.getLogger(__name__)


def get_topic_education_level(topic):
    """Calcula el nivel educativo efectivo del tema en base a sus recursos y asignatura.

    Orden de fallback:
    1. Si hay recursos asociados al tema y todos coinciden en nivel, usar ese.
    2. Si los recursos difieren o no hay recursos, usar el del tema o Subject.education_level.
    """
    resources = list(topic.resources.select_related("subject", "topic__subject"))
    if resources:
        levels = set()
        for r in resources:
            level = r.get_education_level()
            if level:
                levels.add(level)
        if len(levels) == 1:
            return next(iter(levels))

    if topic.education_level:
        return topic.education_level

    if topic.subject and getattr(topic.subject, "education_level", ""):
        return topic.subject.education_level

    return ""


def propose_items_from_guide(quiz_guide, topic, api_key=None) -> list[dict]:
    """Analiza una guía de referencia (QuizGuide) para proponer ítems de aprendizaje sobre un tema.

    Si no hay API keys y estamos en DEBUG/Testing, devuelve ítems simulados mediante un mock determinista.
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

    if not gemini_key and not openai_key:
        if settings.DEBUG or is_testing:
            return _generate_mock_items(topic)
        raise ValueError("No se configuraron las llaves GEMINI_API_KEY u OPENAI_API_KEY.")

    education_level = get_topic_education_level(topic)
    prompt = _build_item_prompt(quiz_guide, topic, education_level)

    active_key = gemini_key or openai_key
    try:
        if gemini_key:
            return _call_gemini_api(prompt, gemini_key)
        if openai_key:
            return _call_openai_api(prompt, openai_key)
    except Exception as e:
        msg = _sanitize_key(str(e), active_key)
        logger.error("Error al proponer ítems de aprendizaje por IA: %s", msg)
        raise RuntimeError(f"Error en la extracción de ítems de la IA: {msg}") from None


def _build_item_prompt(quiz_guide, topic, education_level) -> str:
    """Construye el prompt pedagógico para la IA pidiéndole extraer ítems de aprendizaje."""
    resources = list(topic.resources.all())
    resources_block = "\n".join(
        f"- ID: {r.id} · Título: {r.title}" for r in resources
    )

    edu_labels = {
        "escolar": "Escolar (hasta 13 años) - Dificultad recomendada: basica o intermedia.",
        "media": "Media preuniversitaria (14-17 años) - Dificultad recomendada: intermedia o avanzada.",
        "universitaria": "Universitaria (18+) - Dificultad recomendada: avanzada o desafio.",
    }
    edu_desc = edu_labels.get(education_level, "Media preuniversitaria (14-17 años) - Dificultad recomendada: intermedia o avanzada.")

    notation_instructions = (
        r"""NOTACIÓN MATEMÁTICA (OBLIGATORIO — KaTeX render):
- Escribe TODA expresión matemática en LaTeX entre delimitadores, nunca en texto plano:
  · En línea (dentro de una frase):  $...$
  · En bloque (ecuación centrada):   $$...$$
- JSON: escapa las barras invertidas como dobles. Debe ir "$\\frac{a}{b}$", nunca "$\frac{a}{b}$"."""
    )

    json_example = (
        r"""[
  {
    "title": "Cálculo de la derivada de una función afín",
    "level": 1,
    "difficulty": "intermedia",
    "objective": "Identificar el valor de la pendiente $m$ a partir de la ecuación explícita $y = mx + n$.",
    "recommendation": "Comenzar con ejemplos de coeficiente entero y luego introducir fracciones.",
    "common_errors": "Confundir la pendiente $m$ con el coeficiente de posición $n$.",
    "suggested_resource_ids": [10, 15],
    "detected_exercise_count": 5
  }
]"""
    )

    prompt = f"""Eres un experto pedagogo curricular en matemáticas y ciencias de la plataforma educativa 'ProfeOnline'.

Tu tarea es analizar el texto de la siguiente GUÍA DE REFERENCIA PRIVADA y proponer una lista de ÍTEMS DE APRENDIZAJE estructurados para el tema '{topic.name}' de la asignatura '{topic.subject.name if topic.subject else "General"}'.

¿QUÉ ES UN ÍTEM DE APRENDIZAJE?
Es un objetivo pedagógico evaluable concreto. Por ejemplo, en el tema 'Ecuaciones de segundo grado', un ítem de nivel 1 puede ser 'Identificación de coeficientes', de nivel 2 'Uso de la fórmula general', y de nivel 3 'Modelamiento en problemas reales'.

REQUERIMIENTOS:
1. Analiza con detalle el material de referencia y extrae los ítems de aprendizaje clave que evalúa.
2. Cada ítem debe clasificarse en un nivel pedagógico (level):
   - 1: Comprensión conceptual y funcional (sin cálculos).
   - 2: Dominio procedimental y resolución técnica.
   - 3: Transferencia y aplicación en contextos reales o problemas complejos.
3. Calibra la dificultad de cada ítem según el nivel educativo de destino.
   - Nivel educativo del tema: {education_level} ({edu_desc})
   - Opciones válidas de dificultad (usa EXACTAMENTE estas claves, sin acentos): 'basica', 'intermedia', 'avanzada', 'desafio'.
   - Asegúrate de distribuir las dificultades de manera balanceada en base al nivel educativo de destino (por ejemplo, si es universitario, tiende a 'avanzada' y 'desafio'). No clasifiques todo como 'intermedia'.
4. Sugiere a cuáles recursos del tema corresponde asociar cada ítem, utilizando únicamente IDs válidos del listado provisto abajo.
5. Estima cuántos ejercicios o preguntas se detectaron en la guía que corresponden a cada ítem en el campo 'detected_exercise_count'.

{notation_instructions}

RECURSOS DISPONIBLES EN EL TEMA (puedes sugerir asociar a estos IDs):
{resources_block}

GUÍA DE REFERENCIA PRIVADA (TEXTO A ANALIZAR):
{quiz_guide.content_text}

FORMATO DE RESPUESTA REQUERIDO (JSON):
Debes responder ÚNICAMENTE con una estructura JSON válida que sea una lista de objetos con el siguiente formato, sin bloques de código markdown, explicaciones previas o posteriores:

{json_example}
"""
    return prompt


def _generate_mock_items(topic) -> list[dict]:
    """Genera ítems simulados de forma determinista para pruebas y desarrollo.

    Calibra la dificultad y los nombres basándose en el nivel educativo del tema.
    """
    education_level = get_topic_education_level(topic)

    # Determinar dificultades recomendadas según el nivel educativo (claves canónicas del modelo)
    if education_level == "escolar":
        diff_1 = "basica"
        diff_2 = "basica"
        diff_3 = "intermedia"
    elif education_level == "universitaria":
        diff_1 = "avanzada"
        diff_2 = "avanzada"
        diff_3 = "desafio"
    else:
        diff_1 = "basica"
        diff_2 = "intermedia"
        diff_3 = "avanzada"

    resources = list(topic.resources.all())
    resource_ids = [r.id for r in resources][:2]

    # Generación de títulos con LaTeX basándose en el tema
    math_name = topic.name.lower()
    if "algebra" in math_name or "algebraico" in math_name or "ecuaci" in math_name:
        items = [
            {
                "title": f"Reconocimiento de expresiones en {topic.name}",
                "level": 1,
                "difficulty": diff_1,
                "objective": "Identificar los componentes básicos de una expresión algebraica como términos y coeficientes en $a_n x^n$.",
                "recommendation": "Reforzar el concepto de término semejante.",
                "common_errors": "Confundir el signo negativo como un elemento separado de la constante.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 4,
            },
            {
                "title": f"Evaluación procedimental de {topic.name}",
                "level": 2,
                "difficulty": diff_2,
                "objective": "Resolver operaciones y reducciones algebraicas utilizando la regla distributiva: $a(b + c) = ab + ac$.",
                "recommendation": "Ejercitar con números fraccionarios simples.",
                "common_errors": "No distribuir el signo en todos los términos internos del paréntesis.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 6,
            },
            {
                "title": f"Aplicación práctica de {topic.name}",
                "level": 3,
                "difficulty": diff_3,
                "objective": "Modelar y resolver problemas reales de optimización lineal o sistemas representados por expresiones matemáticas.",
                "recommendation": "Proponer problemas cotidianos de compras o geometría.",
                "common_errors": "Mala traducción del lenguaje natural al lenguaje algebraico.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 3,
            },
        ]
    else:
        items = [
            {
                "title": f"Fundamentos conceptuales de {topic.name}",
                "level": 1,
                "difficulty": diff_1,
                "objective": f"Identificar y explicar los conceptos centrales de {topic.name} sin cálculos complejos.",
                "recommendation": "Utilizar analogías visuales sencillas.",
                "common_errors": "Mezclar definiciones afines pero distintas.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 3,
            },
            {
                "title": f"Resolución de ejercicios técnicos de {topic.name}",
                "level": 2,
                "difficulty": diff_2,
                "objective": f"Aplicar algoritmos estándar de resolución para obtener resultados numéricos en {topic.name}.",
                "recommendation": "Cuidar las unidades y formatos numéricos.",
                "common_errors": "Omisión de pasos mecánicos o errores de cálculo aritmético.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 5,
            },
            {
                "title": f"Resolución de problemas complejos de {topic.name}",
                "level": 3,
                "difficulty": diff_3,
                "objective": f"Transferir y adaptar los conocimientos de {topic.name} a escenarios multidisciplinares o casos de análisis avanzado.",
                "recommendation": "Guías estructuradas con problemas de varios pasos.",
                "common_errors": "Mal planteamiento del modelo de solución.",
                "suggested_resource_ids": resource_ids,
                "detected_exercise_count": 2,
            },
        ]

    return items
