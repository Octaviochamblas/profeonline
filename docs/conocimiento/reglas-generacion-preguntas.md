# Reglas de generación de preguntas de evaluación (para agentes IA)

> Vía alternativa a `poblacion-evaluacion-formal.md`: en vez de que el comando
> `generate_node_assessment_questions` llame a la API de Gemini, un agente de código
> (Claude, Codex, Antigravity — cualquiera) lee este documento y el contenido del nodo, y
> escribe las preguntas directamente. Mismo destino (`NodeAssessmentQuestion` /
> `NodeAssessmentChoice`), mismas reglas pedagógicas, mismo formato de salida — la única
> diferencia es quién redacta. Estas reglas son las mismas que ya están codificadas en
> `_build_node_assessment_prompt` (`apps/content/services/ai_generation_service.py`); si
> alguna vez se edita el prompt, actualizar también este documento.

## Regla crítica #1 — no te extralimites del contenido del recurso

Cada pregunta debe poder responderse **solo** con lo que dice el contenido del nodo. Antes de
escribir una pregunta, lee estos campos de `KnowledgeNode.content` (modelo `NodeContent`) y no
uses nada que no esté ahí:

- `objetivo`
- `introduccion`
- `resumen`
- `explicacion`
- `procedimiento` (lista de pasos)
- `ejemplos` (lista de ejemplos resueltos)

Prohibido:
- Traer fórmulas, propiedades, casos especiales o ejemplos numéricos que no aparezcan en esos
  campos, aunque sean matemáticamente ciertos y "vengan a cuento".
- Asumir que el alumno ya vio contenido de OTRO nodo del árbol (nodos futuros o hermanos) salvo
  que esté explícitamente resumido aquí.
- Rellenar con conocimiento general de matemáticas para compensar un `content` pobre o
  incompleto. Si el nodo no tiene material suficiente para un nivel (p. ej. `procedimiento`
  vacío y se pide Nivel 2), es una señal de que falta poblar el contenido del nodo primero
  (`estrategia-poblacion.md`) — no un problema a resolver inventando.
- Mencionar "el recurso", "la lección", "el texto", "el video" o cualquier título: redacta
  como si el alumno ya estudió el tema y lo estás evaluando directamente.

## Los 3 niveles

Un nodo tiene exactamente 3 niveles, cada uno con 7 preguntas. No mezclar el alcance de un nivel
con otro.

**Nivel 1 — Definición (comprensión conceptual y funcional).**
El estudiante identifica los conceptos centrales, comprende para qué sirven, cuándo se utilizan
y cuál es su lógica básica. **NO** pidas resolución numérica ni cálculos en este nivel. Los
distractores deben reflejar confusiones conceptuales típicas (confundir dos términos parecidos,
atribuir mal una propiedad, equivocarse en "cuándo se aplica").

**Nivel 2 — Ejercicios simples (dominio procedimental y resolución técnica).**
El estudiante aplica fórmulas, reglas o procedimientos —tomados de `procedimiento`/`ejemplos`
del nodo— para resolver ejercicios. No basta con reemplazar datos en una fórmula: debe exigir
identificar qué procedimiento corresponde y desarrollar los pasos. Los distractores deben
representar errores procedimentales reales (error de signo, fórmula equivocada, paso omitido).

**Nivel 3 — Problemas de aplicación (transferencia a contextos reales).**
El estudiante usa lo aprendido para analizar una situación nueva. Prioriza enunciados
contextualizados y de varios pasos donde el dato relevante deba extraerse del problema, no venir
"servido". Los distractores deben reflejar errores de interpretación o de modelado.

## Reglas de las alternativas

1. Exactamente 4 alternativas por pregunta.
2. Exactamente una alternativa correcta (`is_correct` / `correcta` = true).
3. Las 3 alternativas incorrectas (distractores) deben ser plausibles: errores típicos de
   estudiante, nunca disparates obvios que se puedan descartar sin pensar.
4. Sin alternativas "todas las anteriores" / "ninguna de las anteriores".

## Reglas de la explicación

- Cuando la resolución tenga varios pasos, numéralos ("1. ", "2. ", "3. ...") y separa cada paso
  con un salto de línea real (carácter `\n`, no todo en un párrafo corrido).
- Cada paso: una idea concreta y corta.
- Toda fórmula o cálculo también va en LaTeX.

## Notación matemática (obligatorio — la plataforma renderiza LaTeX con KaTeX)

- Toda expresión matemática en LaTeX, nunca en texto plano ("x^2" o "raíz de x" están prohibidos):
  - En línea: `$...$` — ej. la solución es `$x = \frac{-b}{2a}$`
  - En bloque: `$$...$$` — ej. `$$\int_0^1 x^2\,dx = \frac{1}{3}$$`
- Úsalo en el enunciado, en las 4 alternativas y en la explicación.
- **Si estás escribiendo un archivo JSON** (ver formato de salida abajo), las barras invertidas
  de LaTeX van dobles: `"$\\frac{a}{b}$"`, nunca `"$\frac{a}{b}$"` (si no, el JSON no parsea o el
  texto sale corrupto — ver el bug de escapes resuelto en `_loads_ai_json` para contexto). Si en
  cambio estás usando el shell de Django / ORM directamente en Python, un string normal o raw
  (`r"..."`) con una sola barra está bien — la duplicación es solo para la sintaxis JSON.
- **Para destacar una palabra clave usa doble asterisco: `**palabra**`.** El renderer
  (`markdown_inline`, Python-Markdown) solo convierte doble asterisco en negrita (`<strong>`); un
  solo asterisco se muestra en cursiva, no en negrita.

## Formato de salida

Dos caminos, iguales en contenido:

**A) Archivo JSON + `load_json_questions.py`** (más simple, recomendado para lotes):

```json
[
  {
    "level": 1,
    "text": "¿Cuál es el valor de $x$ en la ecuación $2x = 4$?",
    "explanation": "1. Dividimos ambos lados por $2$.\n2. $x = \\frac{4}{2} = 2$.",
    "choices": [
      {"text": "$2$", "is_correct": true},
      {"text": "$4$", "is_correct": false},
      {"text": "$0$", "is_correct": false},
      {"text": "$-2$", "is_correct": false}
    ]
  }
]
```

```bash
python load_json_questions.py <semantic_id> <ruta_al_json>
```

⚠️ Este loader **no es idempotente**: no revisa duplicados ni usa `generation_key` como sí hace
el comando `generate_node_assessment_questions`. Correrlo dos veces sobre el mismo nodo duplica
las preguntas. Antes de cargar, confirma que el nodo no tenga ya preguntas de ese nivel (admin
`/admin/content/nodeassessmentquestion/` o `NodeAssessmentQuestion.objects.filter(node=node,
level=level).count()`), y bórralas primero si vas a reemplazar.

**B) Django shell / ORM directo** — igual de válido, sin el riesgo de duplicado si usas
`update_or_create` o revisas antes de crear:

```python
from apps.content.models import KnowledgeNode, NodeAssessmentQuestion, NodeAssessmentChoice

node = KnowledgeNode.objects.get(semantic_id="MAT.NUM.ENTEROS_CONJUNTO.NATURALES")
q = NodeAssessmentQuestion.objects.create(
    node=node, level=1, status="publicada",
    text="¿Cuál es el valor de $x$ en la ecuación $2x = 4$?",
    explanation="1. Dividimos ambos lados por $2$.\n2. $x = \\frac{4}{2} = 2$.",
)
for texto, correcta in [("$2$", True), ("$4$", False), ("$0$", False), ("$-2$", False)]:
    NodeAssessmentChoice.objects.create(question=q, text=texto, is_correct=correcta)
```

## Control de calidad antes de publicar

Mismo checklist que `poblacion-evaluacion-formal.md §Control de calidad post-piloto`:
1. Lee 5-10 preguntas al azar por nivel en el admin: ¿el enunciado tiene sentido?, ¿la
   alternativa marcada correcta realmente lo es?, ¿el LaTeX renderiza bien en KaTeX?
2. Rinde una evaluación real en el navegador de punta a punta (formulario → envío → resultado).
3. Verifica que ninguna pregunta usa contenido fuera de lo que dice `node.content` (Regla
   crítica #1) — este es el chequeo que un generador vía Gemini no puede autoevaluarse y que
   aquí sí puede hacer el agente antes de guardar.
