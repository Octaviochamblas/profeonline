# Pauta de contenido — ProfeOnline

> **Referencia única** para generar contenido de cualquier recurso nuevo.
> Aplica a Matemática, Física y Química. Sigue este formato y el recurso
> será automáticamente compatible con el sistema de gamificación.

---

## 1. Por qué este formato es gamificable

La plataforma tiene dos capas que se alimentan de archivos distintos:

| Capa | Archivo fuente | Carga con | Aparece en |
|---|---|---|---|
| **Aprendizaje** | `docs/conocimiento/contenido/*.yaml` | `load_node_content` | Página `/aprender/<slug>` |
| **Práctica/Evaluación** | `docs/conocimiento/ejercicios/*.jsonl` | `load_exercise_bank --file` | Sección "Practica" + sistema de niveles/estrellas |

El sistema de gamificación (XP, estrellas, racha, skills) se activa cuando el alumno
interactúa con los ejercicios del banco. Los campos del YAML alimentan la comprensión;
el JSONL alimenta la evaluación medible. Los dos deben existir para que un recurso
esté "completo" en la plataforma.

---

## 2. Archivo YAML — contenido pedagógico

### Ubicación
```
docs/conocimiento/contenido/<semantic_id_en_kebab>.yaml
```
Ejemplo: `mat-num-enteros-conjunto-pares.yaml`

### Estructura completa (estándar vigente desde 2026-08-04 — 12 secciones)

> **Historial:** hasta 2026-08-04 la estructura era de 4 campos de texto libre
> (`objetivo`, `introduccion`, `resumen`, `explicacion`). Esa estructura sigue
> existiendo como *fallback* de renderizado para los nodos aún no migrados
> (`node_detail.html` cae a ella si faltan los campos nuevos), pero **ya no es
> el estándar para contenido nuevo**. Todo recurso nuevo debe usar los 12
> campos de abajo.

```yaml
semantic_id: MAT.NUM.<BLOQUE>.<RECURSO>
resumen_inicial: "Una sola frase con la idea central del recurso, sin jerga."
explicacion_simple: |
  Texto muy simple, como para un alumno de 10 años, con una analogía concreta
  del mundo real. Sin LaTeX ni tecnicismos. 3-4 frases.
explicacion_formal: |
  Texto técnico en Markdown + LaTeX ($...$). Aquí sí se espera profundidad y
  precisión matemática. Puede incluir la definición formal y por qué funciona.
definiciones_clave: |
  Términos nuevos del recurso, en **negrita**, con su definición precisa.
propiedades_relaciones: |
  Cómo se relaciona este concepto con otros ya vistos (qué implica, qué lo
  implica, casos especiales).
ejemplo_guiado:
  enunciado: "Un problema concreto que se resuelve paso a paso."
  pasos:
    - "Paso 1 del razonamiento, con el cálculo explícito."
    - "Paso 2."
    - "Conclusión con el resultado final."
# ⚠️ REGLA DURA (agregada 2026-08-05 tras auditoría — ver
# docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.md): `enunciado` debe
# traer datos propios (números, coeficientes o una expresión concreta) que el
# alumno pueda seguir resolviendo. NUNCA describir el problema pegando el nombre
# del recurso en una frase molde ni reusar los mismos 4 `pasos` genéricos
# ("Identificar los datos...", "Aplicar la regla...", "Efectuar las
# operaciones...", "Verificar...") de un recurso a otro solo cambiando el título.
# Ejemplo MALO real (rechazar): enunciado "Simplifica o resuelve la expresión
# aplicando concepto de m.c.d. algebraico." — no hay expresión que resolver.
# Ejemplo BUENO real: enunciado "En un curso hay 15 hombres y 20 mujeres. Escribe
# la razón entre la cantidad de hombres y mujeres en su forma simplificada." con
# pasos que operan esos números concretos.
#
# ⚠️ SEGUNDA REGLA DURA (agregada 2026-08-05, tras auditar Geometría): tener números
# concretos NO basta. `enunciado` + `pasos` deben ser ÚNICOS para ESTE recurso — está
# PROHIBIDO copiar el mismo ejemplo_guiado en varios recursos del mismo sub-tema
# (aunque tenga datos numéricos reales). Caso real rechazado: "Calcula el área de un
# círculo de radio r=5cm" se copió sin cambios en 30 recursos de Geometría, incluyendo
# uno sobre ángulo exterior entre secantes — sin relación con el área. El ejemplo debe
# resolver específicamente EL CONCEPTO de ESTE recurso, no un tema genérico de la
# familia. Antes de cargar, verificar que ningún otro YAML del mismo sub-tema tenga
# el mismo `enunciado`.
checkpoints:                       # Exactamente 2, validados por node_checkpoint_service
  - placement: after_explicacion_formal
    question: "Pregunta conceptual sobre lo explicado arriba."
    choices:                       # Exactamente 4, 1 sola con is_correct: true
      - {text: "Alternativa correcta", is_correct: true}
      - {text: "Distractor 1", is_correct: false}
      - {text: "Distractor 2", is_correct: false}
      - {text: "Distractor 3", is_correct: false}
    explanation: "La correcta es Alternativa correcta: por qué."  # debe MENCIONAR el texto de la correcta
    reinforcement_section: "Explicación formal"
  - placement: after_ejemplo_guiado
    question: "Pregunta que reutiliza el mismo procedimiento del ejemplo guiado con otro número."
    choices: [...]                 # mismo formato, 4 alternativas
    explanation: "..."
    reinforcement_section: "Ejemplo guiado"
procedimiento:
  - "Paso 1: descripción concisa del primer paso (puede tener $LaTeX$)."
  - "Paso 2: ..."
errores_correccion: |
  Texto explicativo (1-2 frases) sobre los 1-2 errores más frecuentes y cómo
  evitarlos. NO reemplaza `errores_frecuentes` (ese es el que alimenta el V/F).
ejemplos:
  # TIPO A — Selección múltiple, 3 alternativas (estándar desde 2026-08-03)
  - titulo: "Ejemplo 1"
    enunciado: "La pregunta o situación real que el alumno debe analizar."
    alternativas:
      - "Alternativa correcta"
      - "Distractor 1"
      - "Distractor 2"
    respuesta: "Alternativa correcta"   # debe calzar EXACTO (texto) con una de `alternativas`
    solucion_pasos:
      - "Explicación del primer paso."
      - "Explicación del segundo paso."
  # TIPO B — Ejemplo Sí/No interactivo (True/False en la UI)
  - titulo: "¿Texto de la pregunta directamente en el título?"
    respuesta: "Sí"          # o "No"
    solucion_pasos:
      - "Por qué la respuesta es Sí/No."
errores_frecuentes:
  - "Afirmación falsa que un alumno podría creer (sin LaTeX o mínimo)."
  - "Segunda afirmación falsa."
  - "Tercera afirmación falsa."
  - "Cuarta afirmación falsa."
  - "Quinta afirmación falsa."
afirmaciones_verdaderas:           # NUEVO desde 2026-08-04 — ver nota abajo
  - "Afirmación cierta sobre el tema, breve y verificable."
  - "Segunda afirmación cierta."
al_terminar_debes_poder: |
  1-2 frases: qué debe saber hacer el alumno al terminar este recurso.
fuente: "Libro / apunte de referencia con página si aplica"
estado: publicado    # o borrador
```

### Reglas campo a campo

| Campo | Obligatorio | Notas |
|---|---|---|
| `semantic_id` | Sí | Debe existir en la DB (`KnowledgeNode`). Formato: `MAT.NUM.BLOQUE.RECURSO` |
| `resumen_inicial` | Sí | Una frase, sin jerga. Es lo primero que lee el alumno. |
| `explicacion_simple` | Sí | Lenguaje de 10 años, con analogía concreta. Sin LaTeX pesado. |
| `explicacion_formal` | Sí | Markdown + LaTeX. Definición precisa y por qué funciona. |
| `definiciones_clave` | Sí | Términos nuevos en **negrita** con su definición. |
| `propiedades_relaciones` | Sí | Cómo se conecta con otros conceptos ya vistos. |
| `ejemplo_guiado` | Sí | Objeto `{enunciado, pasos}`. Un solo problema resuelto paso a paso **con datos concretos** (números/expresión propios del enunciado, no el nombre del recurso repetido en una frase molde — ver regla dura junto al YAML de ejemplo arriba). |
| `checkpoints` | Sí | **Exactamente 2** (`after_explicacion_formal` y `after_ejemplo_guiado`), 4 alternativas cada uno, 1 sola correcta, `explanation` debe mencionar el texto exacto de la correcta. Validado por `node_checkpoint_service.normalize_node_checkpoints`; si es inválido, `load_node_content` rechaza el archivo completo. |
| `procedimiento` | Sí | Lista de pasos en orden. Mínimo 2, recomendado 3-4. |
| `errores_correccion` | Sí | Texto breve sobre 1-2 errores típicos. No sustituye `errores_frecuentes`. |
| `ejemplos` | Sí | **Mínimo 4**: 2 Tipo A (selección múltiple, 3 alternativas) + 2 Tipo B (Sí/No interactivos). Los Tipo B van al final. |
| `errores_frecuentes` | Sí | **Exactamente 5**. Afirmaciones falsas (errores típicos). Se mezclan con `afirmaciones_verdaderas` en la sección "Ejemplos Verdadero/Falso". |
| `afirmaciones_verdaderas` | Sí | **Mínimo 2**. Afirmaciones ciertas sobre el tema, breves y verificables. Sin ellas, la sección V/F muestra solo "Falso" siempre (comportamiento legado, ver nota abajo). |
| `al_terminar_debes_poder` | Sí | 1-2 frases con la meta de aprendizaje del recurso. |
| `fuente` | Recomendado | Nombre del libro y página. Ayuda a verificar. |
| `estado` | Sí | Usa `publicado` cuando el contenido está revisado. |

> **Nota — por qué existe `afirmaciones_verdaderas` (2026-08-04):** la sección
> "Ejemplos Verdadero/Falso" se construía únicamente desde `errores_frecuentes`,
> así que la respuesta correcta era siempre "Falso". La vista
> (`apps/learn/views.py::_true_false_items`) ahora mezcla ambos campos y los
> presenta en orden aleatorio por cada carga de página. Mismo motivo por el
> que las alternativas de `checkpoints` y de `ejemplos` (Tipo A) también se
> aleatorizan en la vista (`_checkpoint_context`, `_shuffled_ejemplos`): antes
> la alternativa correcta quedaba casi siempre primera porque así se redactó.
> **No hace falta variar el orden al escribir el YAML** — pon la alternativa
> correcta donde te resulte más natural redactar; la vista se encarga de
> desordenarla en cada visita.

### Sobre `ejemplos`: Tipo A vs Tipo B

```yaml
# TIPO A — Selección múltiple, 3 alternativas
- titulo: "Ejemplo 1"          # Siempre "Ejemplo N"
  enunciado: "La pregunta real que el alumno lee y piensa."
  alternativas: [...]          # Exactamente 3, únicas, sin repetir
  respuesta: "..."             # Debe calzar EXACTO (mismo texto) con una de `alternativas`
  solucion_pasos: [...]        # Se muestra como argumento al responder (correcto o no)

# TIPO B — Pregunta de Sí/No (interactiva)
- titulo: "¿La pregunta va aquí directamente?"   # El título ES la pregunta
  respuesta: "Sí"              # "Sí" o "No" — respuesta correcta
  solucion_pasos: [...]        # Se muestra al responder
```

Ambos tipos aparecen como botones en la UI (3 alternativas en Tipo A, Sí/No en Tipo B). El
alumno responde y recibe feedback inmediato (correcto/incorrecto) junto con `solucion_pasos`
como argumento. **No generar `enunciado` en Tipo B** — el `titulo` ya es la pregunta.

> **Historial:** hasta 2026-08-03 el Tipo A era una pregunta abierta sin alternativas, resuelta
> con un botón "Ver solución" sin corrección. Se reemplazó por selección múltiple de 3
> alternativas para que el alumno reciba feedback de correcto/incorrecto, igual que el Tipo B.
> Un `ejemplos` sin `alternativas` ni `respuesta` en {Sí, No, Verdadero, Falso} sigue
> renderizando como el formato abierto legado — no se rompe nada, pero ya no es el estándar
> para contenido nuevo.

---

## 3. Archivo JSONL — banco de ejercicios

### Ubicación
```
docs/conocimiento/ejercicios/<bloque>-banco-gen-<N>.jsonl
```
Ejemplo: `mat-num-enteros-conjunto-banco-gen-1.jsonl`

Un archivo puede contener ejercicios de varios recursos. Un recurso puede
estar distribuido en varios archivos. Lo importante es el `stable_id` único.

### Los 4 grupos pedagógicos (item_group)

Cada recurso debe tener **exactamente 10 ejercicios**: uno por celda de esta tabla.

| `item_group` | Nivel Bloom | Quiz level | Cantidad | Formato |
|---|---|---|---|---|
| `conceptuales` | Comprender | 1 | 3 | `multiple_choice` |
| `reconocimiento` | Reconocer | 1 | 1 | `multiple_choice` |
| `procedimiento_basico` | Resolver | 2 | 3 | `true_false` |
| `tipo_paes` | Aplicar | 3 | 3 | `multiple_choice` |

> **Por qué 10:** Los niveles de evaluación toman 5 preguntas al azar de un pool.
> 3+1 = 4 en nivel 1, 3 en nivel 2, 3 en nivel 3. A medida que el banco crezca
> con más ejercicios por grupo, las evaluaciones se vuelven más variadas.

### Estructura de cada línea

```jsonc
// multiple_choice
{
  "stable_id": "ABBR-GEN-GRUPO-N",
  "semantic_id": "MAT.NUM.BLOQUE.RECURSO",
  "item_group": "conceptuales",        // conceptuales | reconocimiento | procedimiento_basico | tipo_paes
  "format": "multiple_choice",
  "difficulty": "basica",              // basica | media | alta
  "competencia": "M1",                 // M1 | M2 | U (según PAES)
  "prompt": "Texto de la pregunta (soporta $LaTeX$).",
  "choices": [
    "Alternativa A",
    "Alternativa B",
    "Alternativa C",
    "Alternativa D"
  ],
  "correct_answer": "Alternativa A",   // debe coincidir EXACTAMENTE con uno de choices
  "solution_steps": "Explicación breve de por qué esa es la correcta.",
  "status": "ready",
  "source_kind": "manual"
}

// true_false (procedimiento_basico)
{
  "stable_id": "ABBR-GEN-PROC-N",
  "semantic_id": "MAT.NUM.BLOQUE.RECURSO",
  "item_group": "procedimiento_basico",
  "format": "true_false",
  "difficulty": "basica",
  "prompt": "¿Afirmación que el alumno evalúa como verdadera o falsa?",
  "correct_answer": "Verdadero",       // "Verdadero" o "Falso"
  "solution_steps": "Explicación.",
  "status": "ready",
  "source_kind": "manual"
}

// tipo_paes — igual que multiple_choice pero con paes_style: true
{
  ...
  "item_group": "tipo_paes",
  "difficulty": "media",
  "paes_style": true,
  "prompt": "Enunciado con contexto aplicado (situación real o matemática compleja).",
  ...
}
```

### Convención de `stable_id`

```
{ABBR}-GEN-{GROUP}-{N}
```

| Segmento | Descripción | Ejemplo |
|---|---|---|
| `ABBR` | Abreviatura del recurso (3-6 letras) | `NAT`, `CARD`, `TRIC`, `VADEF` |
| `GEN` | Indica que fue generado como banco general | fijo |
| `GROUP` | Código del grupo | `CONC`, `REC`, `PROC`, `PAES` |
| `N` | Número secuencial dentro del grupo | `1`, `2`, `3` |

**El `stable_id` debe ser globalmente único.** Si un recurso ya tiene ejercicios con
`ABBR-CONC-1` etc. (sin `GEN`), los nuevos van con `ABBR-GEN-CONC-1`.

---

## 4. Cómo se conecta con la gamificación

```
YAML (NodeContent)                        JSONL (NodeExercise)
──────────────────                        ────────────────────
resumen_inicial + explicacion_simple  ──→ comprensión inicial
explicacion_formal + definiciones_clave
  + propiedades_relaciones            ──→ conocimiento de fondo
ejemplo_guiado                        ──→ modelo resuelto paso a paso
checkpoints (2)                       ──→ "Comprueba tu avance" (UI, sin XP)
procedimiento                         ──→ pasos memorizables
ejemplos                              ──→ práctica no medida (UI interactiva, sin XP)
errores_frecuentes + afirmaciones_verdaderas
  ──→ Ejemplos Verdadero/Falso, mezclados y aleatorizados (UI, sin XP)
al_terminar_debes_poder               ──→ cierre / meta de aprendizaje

                             conceptuales + reconocimiento
                               ──→ QuizAttempt nivel 1 → ⭐
                             procedimiento_basico
                               ──→ QuizAttempt nivel 2 → ⭐⭐
                             tipo_paes
                               ──→ QuizAttempt nivel 3 → ⭐⭐⭐
                             Aprobar nivel 3 → XP + skill desbloqueada
```

Los campos del YAML no generan XP por sí solos. El XP viene de los ejercicios
del banco. Un recurso sin JSONL se puede leer, pero no se puede "ganar" en él.

---

## 5. Checklist antes de cargar un recurso nuevo

- [ ] `semantic_id` existe en la DB (`KnowledgeNode`)
- [ ] YAML tiene los 12 campos obligatorios completos (ver tabla arriba)
- [ ] `explicacion_simple` usa lenguaje simple (sin jerga, analogía concreta)
- [ ] `ejemplo_guiado.enunciado` trae datos concretos (números/expresión propios), no es una
      frase genérica con el nombre del recurso pegado — ni repite los mismos 4 `pasos` molde de
      otro recurso del mismo sub-tema
- [ ] `ejemplo_guiado.enunciado` es distinto (no copiado) del de cualquier otro recurso del
      mismo sub-tema, y resuelve el concepto específico de ESTE recurso
- [ ] `al_terminar_debes_poder` no está vacío (1-2 frases con la meta de aprendizaje)
- [ ] `checkpoints`: exactamente 2 (`after_explicacion_formal`, `after_ejemplo_guiado`), 4 alternativas c/u, 1 sola correcta, `explanation` menciona el texto de la correcta
- [ ] `ejemplos`: mínimo 2 Tipo A + 2 Tipo B (al final)
- [ ] `errores_frecuentes`: exactamente 5 afirmaciones falsas
- [ ] `afirmaciones_verdaderas`: mínimo 2 afirmaciones ciertas
- [ ] `estado: publicado`
- [ ] JSONL tiene 10 ejercicios por recurso: 3+1+3+3
- [ ] `correct_answer` en multiple_choice coincide letra a letra con uno de `choices`
- [ ] `stable_id` es único en todo el banco
- [ ] Cargado con `python manage.py load_node_content` y `load_exercise_bank --file`

---

## 6. Comandos de carga

```bash
# Cargar / actualizar contenido pedagógico de un recurso
python manage.py load_node_content --file docs/conocimiento/contenido/mi-recurso.yaml

# Cargar / actualizar ejercicios del banco
python manage.py load_exercise_bank --file docs/conocimiento/ejercicios/mi-banco.jsonl

# Cargar todo el contenido de una vez
python manage.py load_node_content

# Regenerar resúmenes con IA (requiere cuota Gemini disponible)
python manage.py generate_node_summaries --all
```

---

## 7. Referencia rápida de campos LaTeX

Usar `$...$` para inline y `$$...$$` para bloque en los campos de texto.
Los YAMLs literales (`|`) preservan los backslashes: escribir `\\mathbb{Z}` en YAML.
En JSONL (JSON), usar doble escape también: `"$\\\\mathbb{Z}$"`.

| Lo que quieres escribir | YAML | JSONL |
|---|---|---|
| `ℤ` | `$\\mathbb{Z}$` | `"$\\\\mathbb{Z}$"` |
| `|x|` | `$\|x\|$` | `"$\\|x\\|$"` |
| `2n+1` | `$2n+1$` | `"$2n+1$"` |
| `n ∈ ℤ` | `$n \\in \\mathbb{Z}$` | `"$n \\\\in \\\\mathbb{Z}$"` |
