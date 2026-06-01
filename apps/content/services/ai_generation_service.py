"""Servicio para la generación asistida de preguntas por IA."""

import json
import logging
import os
import random
import sys
import requests
from django.conf import settings
from apps.content.models import Choice, Question

logger = logging.getLogger(__name__)


def generate_questions_for_resource(resource, level, mode="ambas", count=3, api_key=None):
    """Genera preguntas en estado 'borrador' para un recurso usando Gemini o OpenAI.

    Si no se provee ni se encuentra una API key en settings/entorno, y settings.DEBUG es True,
    se genera un conjunto de preguntas simuladas (mock) realistas basadas en el recurso.
    """
    gemini_key = api_key or getattr(settings, "GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    openai_key = api_key or getattr(settings, "OPENAI_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")

    # Si no hay llaves configuradas y estamos en DEBUG o ejecutando tests, usar el generador simulado
    if not gemini_key and not openai_key:
        is_testing = "test" in sys.argv or getattr(settings, "TESTING", False) or "test" in getattr(settings, "SETTINGS_MODULE", "")
        if settings.DEBUG or is_testing:
            return _generate_mock_questions(resource, level, mode, count)
        raise ValueError("No se configuraron las llaves GEMINI_API_KEY u OPENAI_API_KEY.")

    prompt = _build_prompt(resource, level, mode, count)

    if gemini_key:
        questions_data = _call_gemini_api(prompt, gemini_key)
    else:
        questions_data = _call_openai_api(prompt, openai_key)

    created_questions = _save_questions(resource, level, mode, questions_data)
    return created_questions


def _build_prompt(resource, level, mode, count):
    """Construye el prompt pedagógico para la IA."""
    level_name = dict(Question.LEVEL_CHOICES).get(level, f"Nivel {level}")

    prompt = f"""Eres un experto pedagogo en matemáticas y ciencias para la plataforma 'ProfeOnline'.
Tu tarea es generar exactamente {count} preguntas de opción múltiple de alta calidad pedagógica para el recurso titulado "{resource.title}".

INFORMACIÓN DEL RECURSO:
- Título: {resource.title}
- Tema: {resource.topic.name if resource.topic else "General"}
- Asignatura: {resource.subject.name if resource.subject else "General"}
- Descripción: {resource.description}
- Contenido del recurso:
{resource.content[:2000]}

DIRECTRICES DEL NIVEL PEDAGÓGICO:
Nivel solicitado: {level_name} (Nivel {level})
- Nivel 1 — Definición: Preguntas conceptuales, de términos clave, definiciones o fundamentos teóricos expuestos en el recurso.
- Nivel 2 — Ejercicios simples: Ejercicios directos, cálculos mecánicos o aplicación simple de fórmulas con números sencillos.
- Nivel 3 — Problemas de aplicación: Problemas planteados en un contexto o situación real donde el estudiante deba interpretar el enunciado y aplicar el contenido del recurso para resolverlo.

DIRECTRICES DEL MODO DE PREGUNTA:
Modo solicitado: {mode} (puede usarse para 'preparacion', 'evaluacion' o 'ambas').

DIRECTRICES DE LAS ALTERNATIVAS:
1. Proporciona exactamente 4 alternativas por pregunta.
2. Exactamente UNA alternativa debe ser correcta (`is_correct` = true).
3. Las otras 3 alternativas (distractores) deben ser incorrectas pero plausibles, representando errores típicos de los estudiantes (por ejemplo, error de signo, olvidar un paso, etc.).
4. Incluye una explicación breve y clara de la respuesta correcta.

FORMATO DE SALIDA REQUERIDO (JSON):
Debes responder ÚNICAMENTE con una estructura JSON válida que sea una lista de objetos con el siguiente formato, sin bloques de código markdown, explicaciones previas o posteriores:

[
  {{
    "text": "Enunciado de la pregunta...",
    "explanation": "Explicación de por qué la opción correcta es la adecuada y cómo resolver el problema...",
    "choices": [
      {{"text": "Opción 1 (correcta)", "is_correct": true}},
      {{"text": "Opción 2 (incorrecta)", "is_correct": false}},
      {{"text": "Opción 3 (incorrecta)", "is_correct": false}},
      {{"text": "Opción 4 (incorrecta)", "is_correct": false}}
    ]
  }}
]
"""
    return prompt


def _call_gemini_api(prompt, key):
    """Llama a la API de Gemini 1.5 Flash."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_response.strip())
    except Exception as e:
        logger.error(f"Error llamando a Gemini API: {e}")
        raise RuntimeError(f"Error de generación con Gemini: {str(e)}") from e


def _call_openai_api(prompt, key):
    """Llama a la API de OpenAI (GPT-4o-mini)."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text_response = data["choices"][0]["message"]["content"]
        # OpenAI devuelve un objeto que podría tener una clave raíz como "questions"
        parsed = json.loads(text_response.strip())
        if isinstance(parsed, dict):
            # Si el JSON es un diccionario, intentamos extraer la lista
            for value in parsed.values():
                if isinstance(value, list):
                    return value
        return parsed
    except Exception as e:
        logger.error(f"Error llamando a OpenAI API: {e}")
        raise RuntimeError(f"Error de generación con OpenAI: {str(e)}") from e


def _save_questions(resource, level, mode, questions_data):
    """Guarda las preguntas y alternativas en la base de datos como borradores."""
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

    for item in questions_data:
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
            status="borrador",
            order=last_order + 1
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


def _generate_mock_questions(resource, level, mode, count):
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

    return _save_questions(resource, level, mode, questions_data)
