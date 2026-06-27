# Pipeline de ejercicios — NotebookLM → Claude → JSONL → DB

Flujo para poblar el banco de ejercicios (`NodeExercise`) a partir de los libros cargados en NotebookLM,
sin publicar nada automáticamente.

```
NotebookLM (10 libros)  →  tabla CSV/Markdown de ejercicios candidatos
        │
Claude (normalizador)   →  .jsonl validado (1 línea por ejercicio)
        │
load_exercise_bank      →  NodeExercise (status: draft/ready/review_required)
        │
revisión humana         →  status=published (a mano, nunca automático)
```

- **Identidad:** todo se ancla por `semantic_id` (del árbol en `docs/conocimiento/*.yaml`), nunca por
  `code` ni nombre.
- **Grupos:** cada ejercicio entra a un `item_group` (códigos estándar abajo).
- **Seguridad:** el importador **nunca publica**. Marca `review_required` si falta `correct_answer`, o si
  viene `legal_review`/`rewrite_required`. Un `status: published` entrante baja a `ready`.

## Códigos de `item_group` (plantilla estándar)

`conceptuales` · `reconocimiento` · `procedimiento_basico` · `variacion_controlada` ·
`contextualizados` · `tipo_paes` · `mixto`
(progresión: comprender → reconocer → resolver → variar → aplicar → evaluar).

> Los "errores frecuentes" se transforman en **preguntas conceptuales** (enfoque positivo). No usar
> lenguaje visible de "errores/fallas"; etiquetar internamente con `conceptual_checks`.

---

## Prompt A — Extracción general (en NotebookLM)

```text
Actúa como extractor pedagógico para ProfeOnline (PAES Matemática).

Revisa SOLO las fuentes cargadas en este notebook y extrae ejercicios relacionados con los recursos
atómicos del árbol taxonómico adjunto. No inventes ejercicios. No resumas capítulos.

Para cada ejercicio (o familia de ejercicios repetitivos), entrega una fila con:
1. source_title           5. candidate_resource_name   9. paes_style (sí/no)        13. solution_steps
2. source_location        6. item_group sugerido       10. prompt                   14. conceptual_checks
3. source_reference       7. question_type             11. choices                  15. prerequisites_detected
4. candidate_semantic_id  8. difficulty                12. correct_answer           16. confidence (alta/media/baja)
                                                                                     17. needs_human_review (sí/no)
                                                                                     18. rewrite_required (sí/no)
                                                                                     19. legal_review (sí/no)

Reglas:
- Si no estás seguro del semantic_id, escribe "REVISAR" (hasta 3 candidatos si aplica).
- Si falta la respuesta, deja correct_answer vacío y needs_human_review = sí.
- No mezcles ejercicios de recursos distintos en una fila.
- Si hay muchos ejercicios repetitivos, agrúpalos como familia e indica el patrón.
- Salida en tabla Markdown o CSV.
```

## Prompt B — Filtrado por recurso (en NotebookLM)

```text
Filtra solo los ejercicios que ENTRENEN el recurso:

  <SEMANTIC_ID>  —  <NOMBRE DEL RECURSO>

Excluye los que sean principalmente de otros recursos (lístalos).
Organízalos en item_groups: conceptuales, reconocimiento, procedimiento_basico,
variacion_controlada, contextualizados, tipo_paes, mixto.
Si un ejercicio exige un prerrequisito (p. ej. MCM), indícalo en prerequisites_detected.
Máximo 80 ejercicios o familias.
```

## Prompt C — Detección de patrones (en NotebookLM)

```text
Además de ejercicios concretos, identifica PATRONES de ejercicios en las fuentes.
Para cada patrón entrega: pattern_name, semantic_id, item_group, descripción, variables, restricciones
de los valores, ejemplo fácil/medio/avanzado, prerrequisitos, habilidad que entrena, y si puede
convertirse en generador automático. (Estos patrones se cargan como NodeExercise con kind=template.)
```

## Prompt D — Normalizador (Claude) → JSONL

```text
Actúa como normalizador pedagógico de ProfeOnline.
Recibes: (1) el árbol taxonómico con semantic_id/name/competencia/dificultad/jerarquía, y
(2) la extracción de NotebookLM.

Convierte la extracción en un banco importable. Reglas:
- No inventes semantic_id. Cada ejercicio se asocia a UN semantic_id principal.
- Si no hay seguridad suficiente → status = "review_required".
- item_group ∈ {conceptuales, reconocimiento, procedimiento_basico, variacion_controlada,
  contextualizados, tipo_paes, mixto}.
- Si el ejercicio está duplicado o casi idéntico → duplicate_candidate = true.
- Si parece copiado literal de fuente protegida → legal_review = true y rewrite_required = true.
- Si sirve mejor como patrón generativo → kind = "template" y llena "pattern".
- Si falta respuesta/solución → status = "review_required".
- Conserva source_title y source_location. No publiques nada (status máximo: "ready").

Devuelve JSONL (una línea por ejercicio) con el esquema de abajo.
```

---

## Esquema JSONL (campos de `NodeExercise`)

```json
{
  "stable_id": "NAT-CONC-1",
  "semantic_id": "MAT.NUM.ENTEROS_CONJUNTO.NATURALES",
  "item_group": "conceptuales",
  "kind": "item",
  "format": "multiple_choice",
  "difficulty": "basica",
  "competencia": "M1",
  "prompt": "…",
  "choices": ["…", "…"],
  "correct_answer": "…",
  "solution_steps": "…",
  "explanation": "…",
  "conceptual_checks": ["…"],
  "prerequisites": ["MAT.NUM…"],
  "pattern": {},
  "paes_style": false,
  "source_title": "…",
  "source_location": "…",
  "source_reference": "…",
  "source_kind": "notebooklm_extraction",
  "status": "ready",
  "legal_review": false,
  "rewrite_required": false,
  "duplicate_candidate": false,
  "notes": ""
}
```

Valores válidos:
- `kind`: `item` | `template`
- `format`: `multiple_choice` | `open_answer` | `true_false` | `matching` | `completion` | `development`
- `difficulty`: `basica` | `media` | `avanzada` · `competencia`: `M1` | `M2` | `U` | (vacío)
- `source_kind`: `notebooklm_extraction` | `manual` | `generated` | `rewritten`
- `status` (entrante): `draft` | `ready` | `review_required` (nunca `published`)

## Importar

```bash
# Un archivo
python manage.py load_exercise_bank --file docs/conocimiento/ejercicios/<archivo>.jsonl
# Todos los .jsonl de un directorio
python manage.py load_exercise_bank --dir docs/conocimiento/ejercicios
```

- Idempotente por `stable_id` (reejecutar actualiza, no duplica).
- **No degrada** un ejercicio ya `published` (la publicación es manual y "pegajosa").
- Tras importar, revisar y publicar a mano (admin → Ejercicios del nodo, o `status=published`).

Ejemplo real: [`docs/conocimiento/ejercicios/mat-num-enteros-conjunto-naturales.jsonl`](../ejercicios/mat-num-enteros-conjunto-naturales.jsonl).
