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

### Estructura completa

```yaml
semantic_id: MAT.NUM.<BLOQUE>.<RECURSO>
objetivo: "Una sola frase que describe qué logrará el alumno al terminar."
introduccion: |
  Texto muy simple, como para un alumno de 10 años.
  Sin LaTeX ni tecnicismos. Usa analogías concretas.
  Máximo 3 párrafos cortos.
explicacion: |
  Texto técnico completo en Markdown (soporta **negrita**, $LaTeX$, listas).
  Aquí sí se espera profundidad. Puede ser largo.
procedimiento:
  - "Paso 1: descripción concisa del primer paso (puede tener $LaTeX$)."
  - "Paso 2: ..."
  - "Paso 3: ..."
ejemplos:
  # TIPO A — Ejemplo abierto (se muestra solución al hacer clic)
  - titulo: "Ejemplo 1"
    enunciado: "La pregunta o situación real que el alumno debe analizar."
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
fuente: "Libro / apunte de referencia con página si aplica"
estado: publicado    # o borrador
```

### Reglas campo a campo

| Campo | Obligatorio | Notas |
|---|---|---|
| `semantic_id` | Sí | Debe existir en la DB (`KnowledgeNode`). Formato: `MAT.NUM.BLOQUE.RECURSO` |
| `objetivo` | Sí | Una frase. Empieza con verbo infinitivo ("Identificar…", "Calcular…"). |
| `introduccion` | Sí | Lenguaje de 10 años. Sin LaTeX pesado. Usa analogías del mundo real. |
| `explicacion` | Sí | Markdown + LaTeX. Puede ser denso — es para el alumno que quiere profundidad. |
| `procedimiento` | Sí | Lista de pasos en orden. Mínimo 2, recomendado 3-4. |
| `ejemplos` | Sí | **Mínimo 4**: 2 Tipo A (abiertos) + 2 Tipo B (Sí/No interactivos). Los Tipo B van al final. |
| `errores_frecuentes` | Sí | **Exactamente 5**. Son las afirmaciones de la sección "Ejemplos Verdadero/Falso". Siempre falsas. |
| `fuente` | Recomendado | Nombre del libro y página. Ayuda a verificar. |
| `estado` | Sí | Usa `publicado` cuando el contenido está revisado. |

### Sobre `ejemplos`: Tipo A vs Tipo B

```yaml
# TIPO A — Pregunta abierta
- titulo: "Ejemplo 1"          # Siempre "Ejemplo N" para los abiertos
  enunciado: "La pregunta real que el alumno lee y piensa."
  solucion_pasos: [...]        # Se oculta hasta hacer clic en "Ver solución"

# TIPO B — Pregunta de Sí/No (interactiva)
- titulo: "¿La pregunta va aquí directamente?"   # El título ES la pregunta
  respuesta: "Sí"              # "Sí" o "No" — respuesta correcta
  solucion_pasos: [...]        # Se muestra al responder
```

El Tipo B aparece como botones Sí/No en la UI. El alumno responde y recibe
feedback inmediato. **No generar `enunciado` en Tipo B** — el `titulo` ya es la pregunta.

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
YAML (NodeContent)           JSONL (NodeExercise)
──────────────────           ────────────────────
introduccion  ──→ comprensión inicial
explicacion   ──→ conocimiento de fondo
procedimiento ──→ pasos memorizables
ejemplos      ──→ práctica no medida (UI interactiva, sin XP)
errores_frecuentes ──→ Ejemplos Verdadero/Falso (UI, sin XP)

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
- [ ] YAML tiene los 8 campos obligatorios completos
- [ ] `introduccion` usa lenguaje simple (sin jerga, analogías concretas)
- [ ] `ejemplos`: mínimo 2 Tipo A + 2 Tipo B (al final)
- [ ] `errores_frecuentes`: exactamente 5 afirmaciones falsas
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
