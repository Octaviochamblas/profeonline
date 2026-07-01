# Pauta de contenido — ProfeOnline

> **Referencia única** para generar contenido de cualquier recurso nuevo.
> Aplica a Matemática, Física y Química. Sigue este formato y el recurso
> será automáticamente compatible con el sistema de gamificación.

---

## 0. Estructura completa de la página de recurso

Cada recurso se muestra en la ruta `/aprender/<slug>/` y está compuesto por las
siguientes secciones, en este orden. Las columnas indican de dónde viene cada dato
y qué reglas aplican al generarlo.

| # | Sección visible | Modelo / campo | Formato | Propósito pedagógico |
|---|---|---|---|---|
| 1 | **Encabezado** | `KnowledgeNode.name` + `competencia` + breadcrumb | Texto plano, etiqueta M1/M2/U | Orientar al alumno: nombre exacto del tema y su categoría curricular. |
| 2 | **Objetivo** | `NodeContent.objetivo` | Texto plano, 1 frase | Declarar qué logrará el alumno. Empieza siempre con verbo infinitivo ("Identificar…", "Calcular…"). |
| 3 | **Introducción** | `NodeContent.introduccion` | Markdown, sin LaTeX denso | Conectar el concepto con la experiencia cotidiana del alumno de ~10 años. Máximo 3 párrafos, analogías concretas. |
| 4 | **Resumen IA** | `NodeContent.resumen` | Markdown, 2-3 oraciones | Tarjeta de repaso generada o revisada manualmente. Explica qué es el concepto y cuándo se aplica. |
| 5 | **Explicación** | `NodeContent.explicacion` | Markdown + LaTeX completo | Contenido técnico para el alumno que quiere profundidad: definición formal, propiedades, contexto. Puede ser largo. |
| 6 | **Cómo hacerlo paso a paso** | `NodeContent.procedimiento` | Lista de strings, cada uno puede tener LaTeX | Guía operacional memorizable: qué hacer en orden para resolver un problema de este tipo. Mínimo 2 pasos, recomendado 3-4. |
| 7 | **Ejemplos — Tipo A (abiertos)** | `NodeContent.ejemplos` items con `enunciado` | Acordeón "Ver solución" | Ejercicio abierto: el alumno lee el enunciado, piensa, y hace clic para ver los pasos. Mínimo 2 por recurso. |
| 8 | **Ejemplos — Tipo B (Sí/No)** | `NodeContent.ejemplos` items con `respuesta` | Botones interactivos Sí / No con reveal | El título es la pregunta. El alumno responde y recibe feedback inmediato + explicación. Mínimo 2 por recurso, siempre al final de la lista de ejemplos. |
| 9 | **Ejemplos Verdadero/Falso** | `NodeContent.errores_frecuentes` | Acordeón V/F — el alumno abre para ver por qué es falso | Exactamente 5 afirmaciones, todas falsas. El alumno las evalúa y descubre el error conceptual. Sin XP — es refuerzo comprensivo. |
| 10 | **Material adicional** | `NodeResource` (videos, documentos) | Lista de enlaces | Videos de YouTube u otros recursos vinculados al nodo en la DB. Aparece solo si el nodo tiene recursos asociados. |
| 11 | **Practica** | `NodeExercise` (banco JSONL) | Acordeón por nivel, quiz interactivo | Ejercicios medibles: respuestas generan XP y desbloquean estrellas. Dividido en nivel 1 (⭐), nivel 2 (⭐⭐) y nivel 3 (⭐⭐⭐). |

### Reglas de presencia (cuándo aparece cada sección)

| Sección | Condición para aparecer |
|---|---|
| Encabezado | Siempre (viene del `KnowledgeNode`, obligatorio). |
| Objetivo | Si `NodeContent.objetivo` no está vacío. |
| Introducción | Si `NodeContent.introduccion` no está vacío. |
| Resumen IA | Si `NodeContent.resumen` no está vacío. Se genera con `generate_node_summaries`; se puede escribir a mano en el YAML. |
| Explicación | Si `NodeContent.explicacion` no está vacío. |
| Procedimiento | Si `NodeContent.procedimiento` tiene al menos 1 paso. |
| Ejemplos | Si `NodeContent.ejemplos` tiene al menos 1 item. Tipo A y Tipo B se distinguen por la presencia del campo `respuesta`. |
| Ejemplos V/F | Si `NodeContent.errores_frecuentes` tiene al menos 1 afirmación. |
| Material adicional | Si el nodo tiene `NodeResource` asociados distintos de los del banco de ejercicios. |
| Practica | Si el nodo tiene `NodeExercise` en el banco con `status: ready`. |

### Anatomía de cada tipo de ejemplo

```
TIPO A — Ejemplo abierto
┌─────────────────────────────────────────────────────┐
│ "Ejemplo N"                             [Ver solución] │
│ Enunciado de la pregunta o situación real.            │
└─────────────────────────────────────────────────────┘
 Al hacer clic en "Ver solución":
 → Aparecen los solucion_pasos uno a uno en lista.

TIPO B — Sí / No interactivo
┌─────────────────────────────────────────────────────┐
│ ¿La pregunta va directamente aquí en el título?     │
│                   [  Sí  ]   [  No  ]               │
└─────────────────────────────────────────────────────┘
 Al responder:
 → Feedback inmediato (correcto / incorrecto)
 → Aparecen los solucion_pasos explicando por qué.

EJEMPLOS VERDADERO / FALSO (errores_frecuentes)
┌─────────────────────────────────────────────────────┐
│ ▶ "El cero es par porque termina en cero."          │
└─────────────────────────────────────────────────────┘
 Al expandir el acordeón:
 → Se muestra "FALSO" y la explicación del error.
 (No hay botón: el alumno sabe que todas son falsas.)

PRACTICA — Niveles y estrellas
┌─────────────────────────────────────────────────────┐
│ ⭐ Nivel 1 — Comprensión (4 preguntas)              │
│ ⭐⭐ Nivel 2 — Procedimiento (3 preguntas)           │
│ ⭐⭐⭐ Nivel 3 — Aplicación PAES (3 preguntas)        │
└─────────────────────────────────────────────────────┘
 Cada nivel toma preguntas al azar del grupo correspondiente.
 Aprobar los 3 niveles → XP + skill desbloqueada.
```

### Mapa: campo YAML/JSONL → sección visible

```
KnowledgeNode.name        →  Encabezado (título h1)
NodeContent.objetivo      →  Sección 2 "Objetivo"
NodeContent.introduccion  →  Sección 3 "Introducción"
NodeContent.resumen       →  Sección 4 "Resumen IA"
NodeContent.explicacion   →  Sección 5 "Explicación"
NodeContent.procedimiento →  Sección 6 "Cómo hacerlo paso a paso"
NodeContent.ejemplos      →  Sección 7 (Tipo A) + Sección 8 (Tipo B)
NodeContent.errores_frecuentes → Sección 9 "Ejemplos Verdadero/Falso"
NodeResource (DB)         →  Sección 10 "Material adicional"
NodeExercise (banco JSONL)→  Sección 11 "Practica"
```

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
resumen: |
  Tarjeta de repaso en 2-3 oraciones: explica qué es el concepto y cómo se aplica.
  Usa lenguaje claro para enseñanza media y evita repetir textualmente el título.
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
| `introduccion` | Sí | Lenguaje accesible y concreto. Las analogías son opcionales y solo se usan si aclaran el concepto; nunca sustituyen la definición matemática. |
| `resumen` | Sí | Tarjeta de repaso de 2-3 oraciones. Debe explicar qué es el concepto y cómo se aplica. |
| `explicacion` | Sí | Markdown + LaTeX. Debe comenzar con una definición formal y profesional; después desarrolla una interpretación didáctica, ejemplos y propiedades. |
| `procedimiento` | Sí | Lista de pasos en orden. Mínimo 2, recomendado 3-4. |
| `ejemplos` | Sí | **Mínimo 4**: 2 Tipo A (abiertos) + 2 Tipo B (Sí/No interactivos). Los Tipo B van al final. |
| `errores_frecuentes` | Sí | **Exactamente 5**. Son las afirmaciones de la sección "Ejemplos Verdadero/Falso". Siempre falsas. |
| `fuente` | Recomendado | Nombre del libro y página. Ayuda a verificar. |
| `estado` | Sí | Usa `publicado` cuando el contenido está revisado. |

#### Calidad editorial obligatoria

- La estructura común no autoriza prosa repetida: objetivo, introducción, resumen,
  explicación, ejemplos y errores deben responder al concepto específico del recurso.
- Está prohibido publicar marcadores como `Problema modelo`, `Opción 1`,
  `algoritmo correspondiente`, `Ejercicio número`, `Ejemplo ilustrativo` o referencias
  al `semantic_id` como si fueran contenido para el alumno.
- La explicación sigue el orden **definición formal → desarrollo didáctico**. El tono
  didáctico puede ser cercano, pero evita magia, monstruos, explosiones, personajes o
  metáforas que deformen el significado matemático.
- La **definición formal** enuncia el concepto de manera general mediante variables,
  condiciones, propiedades o cuantificadores. No contiene ejercicios resueltos, valores
  particulares ni frases como `por ejemplo`; todo caso concreto pertenece al desarrollo
  didáctico o a la sección de ejemplos.
- Los títulos de ejemplos describen el caso trabajado. No se usan títulos genéricos
  como `Ejemplo 1`, `Ejercicio 2` o `Caso 3`.
- Antes de declarar un bloque completo se auditan archivos vacíos, campos ausentes,
  duplicados exactos, placeholders y la cuota estructural de cada recurso.

### Reglas de render que NO se pueden romper

Estas reglas son obligatorias para toda generación nueva de contenido. Existen
porque ya hubo errores reales en contenido generado: fórmulas que se veían como
texto plano (`a^2`), resúmenes con markdown literal (`**concepto**`) y listas
mal formadas.

| Zona | Regla obligatoria | Correcto | Incorrecto |
|---|---|---|---|
| `resumen` | Se renderiza como Markdown real. Puedes usar `**negrita**`, listas y `$LaTeX$`, pero solo si aportan claridad. | `Un **binomio** tiene dos términos.` | `Un ** ""` |
| `resumen` | No envolver todo el texto en comillas. No usar placeholders como `""`. | `Un polinomio ordenado...` | `"Un polinomio ordenado..."` |
| `resumen` | Si incluyes lista Markdown, deja una línea en blanco antes de `-` o `1.`. | `Idea clave:\n\n- Ordenar\n- Reducir` | `Idea clave:\n- Ordenar\n- Reducir` |
| `resumen`, `explicacion`, `procedimiento`, `ejemplos`, `errores_frecuentes` | Toda fórmula, operación o notación matemática debe ir delimitada con `$...$` o `$$...$$`. | `$a^2 + 3a - 1$` | `a^2 + 3a - 1` |
| `ejemplos.tipo_a.enunciado` | Si el enunciado contiene una operación o expresión, esa parte debe ir en LaTeX inline. | `Suma: $(2a^3 - 5) + (a^2 + 3a + 2)$.` | `Suma: (2a^3 - 5) + (a^2 + 3a + 2).` |
| `ejemplos.solucion_pasos` | Cada paso con cálculo debe llevar sus fragmentos matemáticos en `$...$`. | `Resultado: $2a^3 + a^2 + 3a - 3$.` | `Resultado: 2a^3 + a^2 + 3a - 3.` |
| `ejemplos` | Usar exclusivamente el esquema vigente: `titulo`, `enunciado`, `respuesta`, `solucion_pasos`. No usar claves heredadas `title`, `text` ni `steps`, porque rompen el render en `learn`. | `titulo: "Producto con dos variables"` | `title: "Example"`, `text: ...`, `steps: ...` |
| contenido general | No usar Markdown vacío o decorativo. Toda negrita debe contener una expresión útil. | `**Términos semejantes**` | `** **`, `** ""` |

### Observaciones operativas importantes

- Existe un autoformateo defensivo en ejemplos cortos para cubrir algunos textos
  crudos heredados, pero es solo red de seguridad. No reemplaza escribir bien el
  YAML de origen.
- La política correcta es: si una secuencia debe verse como matemática, escríbela
  como matemática desde el YAML.
- En Álgebra y Funciones esto es especialmente importante para exponentes,
  fracciones, raíces, productos implícitos, conjuntos y ecuaciones.

### Sobre `ejemplos`: Tipo A vs Tipo B

```yaml
# TIPO A — Pregunta abierta
- titulo: "Suma de polinomios con término faltante"  # Describe el caso; nunca "Ejemplo N"
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
- [ ] YAML tiene los 9 campos obligatorios completos
- [ ] `introduccion` usa lenguaje simple (sin jerga, analogías concretas)
- [ ] `resumen` explica qué es el concepto y cómo se aplica en 2-3 oraciones
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
