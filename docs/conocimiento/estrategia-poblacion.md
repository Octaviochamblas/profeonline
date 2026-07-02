# Estrategia de población de contenido

> **Referencia complementaria** a `pauta-contenido.md` (que define el formato).
> Este documento define *cómo trabajar* para poblar los ~1.900 recursos de la biblioteca.

---

## Escala del proyecto

| Indicador | Valor |
|---|---|
| Total de recursos en la DB | ~1.911 (solo MAT) |
| Bloques | 43 |
| Recursos con contenido hoy | 15 (ENTEROS_CONJUNTO) |
| Ejercicios por recurso completo | 10 (YAML + JSONL) |

Trabajar de a **1 bloque por sesión**, en **tandas de 3-5 recursos** por consulta a la IA,
es el ritmo sostenible que mantiene calidad sin perder contexto.

---

## El workflow de 5 pasos

```
[NotebookLM] → Prompt 1 → YAML borrador
      ↓
[ChatGPT]    → Prompt 2 → YAML revisado y corregido
      ↓
[NotebookLM/ChatGPT] → Prompt 3 → JSONL borrador
      ↓
[ChatGPT]    → Prompt 4 → JSONL revisado y corregido
      ↓
[manage.py]  → Paso 5   → Cargar en DB local → verificar → push → cargar en prod
```

- **NotebookLM** genera el contenido pedagógico fundamentado en los libros cargados.
- **ChatGPT** audita formato, precisión matemática y calidad didáctica.
- **manage.py** carga en DB para verificar en el navegador antes de hacer push.

---

## Estrategia de batching (tandas)

**Regla de oro: 3-5 recursos por consulta.**

- Con menos de 3: la IA tiene poco contexto y los ejemplos quedan genéricos.
- Con más de 5: la calidad cae al final del batch y el contexto de NotebookLM se satura.

**Agrupa por sub-tema conceptual**, no por orden secuencial. Así el material del
libro que NotebookLM busca es coherente en toda la tanda.

Ejemplo para el bloque B0202 (Teoría de Números):
```
Tanda 1: Divisibilidad — fundamentos (múltiplo, divisor, división exacta, obtención)
Tanda 2: Criterios de divisibilidad por 2, 3, 4, 5, 6
Tanda 3: Criterios de divisibilidad por 8, 9, 10, 11, 25
Tanda 4: Números primos y compuestos (definición, identificación, el 1)
Tanda 5: Factorización prima (concepto, unicidad, método tabla, método árbol)
Tanda 6: Factorización — cantidad de divisores
Tanda 7: MCM (concepto, lista, tabla, potencias)
Tanda 8: MCD (concepto, lista, tabla, potencias, Euclides, coprimos)
Tanda 9: Aplicaciones MCM y MCD
```

---

## Orden de prioridad de bloques

Criterios para decidir qué poblar primero:
1. **Bloques cortos** — dan velocidad y confianza (< 30 recursos).
2. **Dependencias pedagógicas** — el alumno necesita A antes de B.
3. **Lo que más enseñas** — mayor retorno inmediato.

| Prioridad | Bloque | Recursos | Razón |
|---|---|---|---|
| 🟢 Piloto | MAT.NUM.B0201 Enteros | 36 (15 hechos) | Ya iniciado |
| 🟢 Siguiente | MAT.NUM.B0202 Teoría de Números | 40 | Continúa NUM |
| 🟡 | MAT.GEO.B0411 Trigonometría Rect. | 23 | Bloque más corto |
| 🟡 | MAT.EST.B0502 MTC | 27 | Bloque corto |
| 🟡 | MAT.NUM.B0203 Racionales | 74 | Alta frecuencia en 7°-8° |
| 🟡 | MAT.ALG.B0301 Nomenclatura Alg. | 34 | Base del eje álgebra |
| ⚪ | Resto ALG (B0302-B0315) | ~600 | Después de fundar NUM |
| ⚪ | GEO, EST, FUND | ~700 | Último |

---

## Convención de archivos

### YAML (uno por recurso)
```
docs/conocimiento/contenido/<semantic-id-en-kebab>.yaml
```
Regla de conversión: puntos → guiones, underscores → guiones, todo minúsculas.
```
MAT.NUM.DIVISIBILIDAD.MULTIPLO_CONCEPTO
  → mat-num-divisibilidad-multiplo-concepto.yaml

MAT.NUM.NUMEROS_PRIMOS.PRIMO_DEFINICION
  → mat-num-numeros-primos-primo-definicion.yaml
```

### JSONL (un archivo por bloque, con todos los recursos)
```
docs/conocimiento/ejercicios/<eje-bloque-kebab>-banco-gen-<N>.jsonl
```
Si el bloque supera ~100 líneas (10 recursos × 10 ejercicios = 100 líneas),
dividir en `-banco-gen-1.jsonl`, `-banco-gen-2.jsonl`, etc.
```
MAT.NUM.B0202 Teoría de Números
  → mat-num-teoria-numeros-banco-gen-1.jsonl   (recursos 1-20)
  → mat-num-teoria-numeros-banco-gen-2.jsonl   (recursos 21-40)
```

---

## Prompts completos

### Prompt 1 — NotebookLM → YAML (borrador de contenido)

```
Eres un especialista en didáctica matemática. Usando el material cargado en este
notebook, genera el archivo YAML de contenido pedagógico para los siguientes recursos:

RECURSOS A GENERAR:
1. [SEMANTIC_ID_1] — [Nombre del recurso 1]
2. [SEMANTIC_ID_2] — [Nombre del recurso 2]
3. [SEMANTIC_ID_3] — [Nombre del recurso 3]

Para CADA recurso genera exactamente este bloque YAML (separa bloques con ---):

semantic_id: [ID exacto]
objetivo: "[Una frase. Empieza con verbo infinitivo: Identificar / Calcular / Aplicar / Demostrar]"
introduccion: |
  [Párrafo 1: analogía cotidiana que un alumno de 10 años entienda. Sin LaTeX.]

  [Párrafo 2: qué hace especial a este concepto. Máximo 3 párrafos en total.]
resumen: |
  [2-3 oraciones: QUÉ es el concepto y CÓMO se aplica. Para enseñanza media.]
explicacion: |
  [Texto técnico completo con Markdown. Usa **negrita** y $LaTeX$ inline.
  Debe ser riguroso. Incluye definición formal, propiedades y contexto.]
procedimiento:
  - "Paso 1: [descripción concisa, puede tener $LaTeX$]"
  - "Paso 2: [siguiente paso]"
  - "Paso 3: [paso final o conclusión]"
ejemplos:
  - titulo: "Ejemplo 1"
    enunciado: "[Pregunta o situación real. El alumno lee y piensa.]"
    solucion_pasos:
      - "[Primer paso de la resolución]"
      - "[Segundo paso]"
      - "[Resultado final con conclusión]"
  - titulo: "Ejemplo 2"
    enunciado: "[Segunda pregunta abierta diferente]"
    solucion_pasos:
      - "[Resolución paso a paso]"
      - "[Conclusión]"
  - titulo: "¿[Pregunta de Sí o No directamente aquí]?"
    respuesta: "Sí"
    solucion_pasos:
      - "[Por qué la respuesta es Sí — explicación paso a paso]"
  - titulo: "¿[Segunda pregunta de Sí o No]?"
    respuesta: "No"
    solucion_pasos:
      - "[Por qué la respuesta es No — explicación paso a paso]"
errores_frecuentes:
  - "[Afirmación FALSA que un alumno podría creer. Sin LaTeX pesado.]"
  - "[Segunda afirmación falsa — concepto distinto]"
  - "[Tercera afirmación falsa]"
  - "[Cuarta afirmación falsa]"
  - "[Quinta afirmación falsa]"
fuente: "[Nombre del libro y número de página]"
estado: publicado

REGLAS OBLIGATORIAS:
- errores_frecuentes: exactamente 5, todas deben ser FALSAS
- ejemplos: mínimo 2 Tipo A (con enunciado) + 2 Tipo B (con respuesta Sí/No). Tipo B siempre AL FINAL
- introduccion: sin LaTeX denso, lenguaje cotidiano, máximo 3 párrafos
- LaTeX en bloques literales YAML (|): usar \\ doble (\\mathbb{Z}, \\frac{a}{b})
- NO generes comentarios ni texto extra — solo el bloque YAML
```

---

### Prompt 2 — ChatGPT → Auditoría YAML

```
Eres un profesor de matemáticas de enseñanza media. Audita estos YAMLs de contenido
pedagógico y corrígelos si encuentras errores.

[PEGAR AQUÍ EL YAML GENERADO POR NOTEBOOKLM]

Verifica para cada recurso:
1. OBJETIVO: ¿Empieza con verbo infinitivo? ¿Es una sola frase clara?
2. INTRODUCCIÓN: ¿Lenguaje de ~10 años? ¿Analogías concretas? ¿Sin LaTeX denso? ¿Máximo 3 párrafos?
3. RESUMEN: ¿Explica QUÉ es el concepto y CÓMO se aplica? ¿2-3 oraciones?
4. EXPLICACIÓN: ¿Técnicamente correcta? ¿Suficientemente profunda?
5. PROCEDIMIENTO: ¿Pasos en orden lógico? ¿Mínimo 2 pasos?
6. EJEMPLOS: ¿Al menos 2 Tipo A (con enunciado:) y 2 Tipo B (con respuesta: Sí o No)?
   ¿Los Tipo B están AL FINAL de la lista?
7. ERRORES FRECUENTES: ¿Exactamente 5? ¿Son TODAS afirmaciones falsas?
8. LaTeX: ¿En bloques YAML literales (|) los backslashes están escritos como \\ doble?
9. ESTADO: ¿Dice "publicado"?

Devuelve el YAML corregido completo. Solo el YAML, sin explicaciones adicionales.
```

---

### Prompt 3 — NotebookLM o ChatGPT → JSONL (banco de ejercicios)

```
Eres un especialista en evaluación educativa (estilo PAES Chile). Genera el banco de
ejercicios en formato JSONL para estos recursos:

RECURSOS:
1. [SEMANTIC_ID_1] — [Nombre del recurso 1]
2. [SEMANTIC_ID_2] — [Nombre del recurso 2]

Genera exactamente 10 líneas JSON por recurso:
- 3 con item_group "conceptuales"        (format: multiple_choice, difficulty: basica)
- 1 con item_group "reconocimiento"      (format: multiple_choice, difficulty: basica)
- 3 con item_group "procedimiento_basico"(format: true_false,      difficulty: basica)
- 3 con item_group "tipo_paes"           (format: multiple_choice, difficulty: media, paes_style: true)

PLANTILLA multiple_choice:
{"stable_id":"ABBR-GEN-CONC-1","semantic_id":"[ID]","item_group":"conceptuales","format":"multiple_choice","difficulty":"basica","competencia":"M1","prompt":"[pregunta]","choices":["A","B","C","D"],"correct_answer":"A","solution_steps":"[explicación]","status":"ready","source_kind":"manual"}

PLANTILLA true_false:
{"stable_id":"ABBR-GEN-PROC-1","semantic_id":"[ID]","item_group":"procedimiento_basico","format":"true_false","difficulty":"basica","prompt":"[afirmación a evaluar]","correct_answer":"Verdadero","solution_steps":"[explicación]","status":"ready","source_kind":"manual"}

PLANTILLA tipo_paes (multiple_choice + paes_style):
{"stable_id":"ABBR-GEN-PAES-1","semantic_id":"[ID]","item_group":"tipo_paes","format":"multiple_choice","difficulty":"media","competencia":"M1","paes_style":true,"prompt":"[situación real aplicada]","choices":["A","B","C","D"],"correct_answer":"A","solution_steps":"[explicación]","status":"ready","source_kind":"manual"}

CONVENCIÓN de stable_id:
- ABBR: 3-6 letras uppercase del recurso (MULT, DIV, PRIM, MCM, MCD, CRIT2, etc.)
- Grupos: CONC, REC, PROC, PAES
- Ejemplo: MULT-GEN-CONC-1, MULT-GEN-CONC-2, MULT-GEN-CONC-3, MULT-GEN-REC-1, etc.

REGLAS:
- correct_answer en multiple_choice: IDÉNTICO letra por letra a uno de los choices
- correct_answer en true_false: "Verdadero" o "Falso" (mayúscula, en español)
- LaTeX en JSON: doble backslash \\frac{a}{b}, \\mathbb{Z}, \\sqrt{x}
- Distractores: plausibles, basados en errores conceptuales comunes
- tipo_paes: contexto aplicado o situación real, no solo definición
- Devuelve UNA línea JSON por ejercicio. Sin texto adicional.
```

---

### Prompt 4 — ChatGPT → Auditoría JSONL

```
Audita este banco de ejercicios JSONL para matemáticas. Verifica cada línea:

[PEGAR AQUÍ EL JSONL]

Checklist por ítem:
1. stable_id: ¿Sigue el formato ABBR-GEN-GRUPO-N? ¿Es único?
2. format=multiple_choice: ¿correct_answer coincide EXACTAMENTE con uno de choices?
3. format=true_false: ¿correct_answer es "Verdadero" o "Falso" (mayúscula, español)?
4. item_group=tipo_paes: ¿tiene "paes_style":true?
5. LaTeX: ¿usa doble backslash \\ dentro de strings JSON?
6. Distractores: ¿son plausibles? ¿representan errores conceptuales reales?
7. Distribución por semantic_id: ¿exactamente 3 CONC + 1 REC + 3 PROC + 3 PAES?
8. tipo_paes: ¿tienen contexto aplicado, no solo definición?

Devuelve el JSONL corregido, una línea por ejercicio. Solo el JSONL, sin comentarios.
```

---

## Paso 5 — Cargar en DB y verificar

```bash
# Cargar un YAML específico
python manage.py load_node_content --file docs/conocimiento/contenido/[mi-recurso].yaml

# Cargar todos los YAMLs a la vez
python manage.py load_node_content

# Cargar el banco de ejercicios de un bloque
python manage.py load_exercise_bank --file docs/conocimiento/ejercicios/[mi-banco].jsonl

# Verificar un recurso en DB (reemplaza el semantic_id)
python manage.py shell -c "
from apps.content.models import NodeContent, KnowledgeNode
nodo = KnowledgeNode.objects.get(semantic_id='MAT.NUM.DIVISIBILIDAD.MULTIPLO_CONCEPTO')
c = nodo.content
print('objetivo:', bool(c.objetivo))
print('introduccion:', bool(c.introduccion))
print('explicacion:', bool(c.explicacion))
print('ejemplos:', len(c.ejemplos))
print('errores:', len(c.errores_frecuentes))
"

# Ver en el navegador (confirmar antes de push)
# URL: http://localhost:8000/aprender/matematicas/numeros/enteros/.../<slug>/
```

**En producción (Railway):** después de cada push que agrega YAMLs o JSONLs,
ejecutar manualmente `load_node_content` y `load_exercise_bank` — el start command
del deploy no los corre automáticamente.

---

## Checklist de calidad antes de hacer push

- [ ] Todos los archivos YAML parsean sin error (`python -c "import yaml; yaml.safe_load(open('archivo.yaml'))"`)
- [ ] El YAML tiene los 9 campos obligatorios (ver `pauta-contenido.md §2`)
- [ ] Exactamente 5 `errores_frecuentes` (todos falsos)
- [ ] Al menos 2 ejemplos Tipo A + 2 Tipo B (al final)
- [ ] El JSONL tiene 10 líneas por recurso: 3+1+3+3
- [ ] `correct_answer` en multiple_choice coincide exactamente con uno de `choices`
- [ ] `stable_id` único en todo el banco
- [ ] Cargado localmente y verificado en navegador
- [ ] Tests pasan: `python manage.py test` (o focalizado `apps/content`)

---

## Registro de avance

| Bloque | Recursos | Contenido (YAML) | Ejercicios (JSONL) | Estado |
|---|---|---|---|---|
| MAT.NUM.B0201 Enteros | 36 | 15/36 | 15/36 | 🟡 Parcial |
| MAT.NUM.B0202 Teoría de Números | 40 | 5/40 (Tanda 1: Divisibilidad fundamentos) | 5/40 | 🟡 En curso |
| MAT.GEO.B0411 Trigonometría Rect. | 23 | 0/23 | 0/23 | ⚪ Pendiente |
| MAT.EST.B0502 MTC | 27 | 0/27 | 0/27 | ⚪ Pendiente |
| MAT.NUM.B0203 Racionales | 74 | 0/74 | 0/74 | ⚪ Pendiente |
| MAT.ALG.B0301 Nomenclatura Alg. | 34 | 0/34 | 0/34 | ⚪ Pendiente |
| *(el resto de los bloques)* | ~1.600 | 0 | 0 | ⚪ Pendiente |

> Actualizar esta tabla a medida que se completan bloques.
