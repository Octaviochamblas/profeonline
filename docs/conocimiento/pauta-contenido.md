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
  Texto explicativo claro y didáctico que transmite la lógica intuitiva, el propósito
  y el sentido del procedimiento algebraico. Sin adelantarse a resolver un ejemplo
  numérico o algebraico particular (eso pertenece a `ejemplo_guiado`). 3-4 frases.
explicacion_formal: |
  Texto técnico en Markdown + LaTeX ($...$). Aquí se exige precisión matemática,
  el desglose simbólico y didáctico de las fórmulas presentadas. Debe incluir:
  1. Definición formal en LaTeX ($...$ o $$...$$). **IMPORTANTE:** Usar notación
     algebraica escolar/PAES ($\mathbb{R}, \mathbb{Z}^+$, conjuntos, polinomios).
     Está **estrictamente prohibido** usar herramientas de cálculo avanzado
     (derivadas, derivadas parciales, integrales, límites) salvo que el tema lo
     exija expresamente (ej. tasa de cambio instantánea en física/cálculo).
  2. **Desglose simbólico**: Explicación de qué significa cada elemento, variable o notación (ej. $\prod$, $\min$, $\operatorname{gcd}$).
  3. **Complemento didáctico**: Una síntesis al final que explique en lenguaje accesible qué asegura esa fórmula en la práctica.
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
#
# ⚠️ TERCERA REGLA DURA (agregada 2026-08-07): Expresiones matemáticas en LaTeX
# TODAS las expresiones matemáticas (variables, ecuaciones, polinomios, números con exponentes,
# alternativas, enunciados) en las secciones `checkpoints` ("Comprueba tu avance"), `ejemplos` ("Ejemplos")
# y `errores_frecuentes` / `afirmaciones_verdaderas` ("Ejemplos Verdadero/Falso") DEBEN estar encerradas
# obligatoriamente entre signos de dólar ($...$ o $$...$$) para su renderizado profesional mediante KaTeX.
checkpoints:                       # Exactamente 2, validados por node_checkpoint_service
  - placement: after_explicacion_formal
    question: "Pregunta conceptual sobre $a^2 + b^2$ explicada arriba."
    choices:                       # Exactamente 4, 1 sola con is_correct: true
      - {text: "$(a + b)^2 = a^2 + 2ab + b^2$", is_correct: true}
      - {text: "$a^2 + b^2$", is_correct: false}
      - {text: "$a^2 - 2ab + b^2$", is_correct: false}
      - {text: "$2a + 2b$", is_correct: false}
    explanation: "La alternativa correcta es '$(a + b)^2 = a^2 + 2ab + b^2$'."  # debe MENCIONAR el texto de la correcta
    reinforcement_section: "Explicación formal"
  - placement: after_ejemplo_guiado
    question: "Pregunta que reutiliza el procedimiento con $(x + 5)^2$."
    choices: [...]                 # mismo formato, 4 alternativas en LaTeX
    explanation: "La alternativa correcta es '$...$'."
    reinforcement_section: "Ejemplo guiado"
procedimiento:
  - "Paso 1: descripción concisa del primer paso con $LaTeX$."
  - "Paso 2: ..."
errores_correccion: |
  Texto explicativo (1-2 frases) sobre los 1-2 errores más frecuentes y cómo
  evitarlos. NO reemplaza `errores_frecuentes` (ese es el que alimenta el V/F).
ejemplos:
  # TIPO A — Selección múltiple, 3 alternativas (estándar desde 2026-08-03)
  - titulo: "Ejemplo 1"
    enunciado: "¿Cuál es el desarrollo de $(x + 3)^2$?"
    alternativas:
      - "$x^2 + 6x + 9$"
      - "$x^2 + 9$"
      - "$x^2 + 3x + 9$"
    respuesta: "$x^2 + 6x + 9$"   # debe calzar EXACTO (texto) con una de `alternativas`
    solucion_pasos:
      - "1. Cuadrado del primero: $x^2$."
      - "2. Doble producto: $2(x)(3) = 6x$."
      - "3. Cuadrado del segundo: $3^2 = 9$. Resultado: $x^2 + 6x + 9$."
  # TIPO B — Ejemplo Sí/No interactivo (True/False en la UI)
  - titulo: "¿Es $(x + 4)^2 = x^2 + 8x + 16$ una identidad correcta?"
    respuesta: "Sí"          # o "No"
    solucion_pasos:
      - "Sí, aplicando el producto notable se obtiene $x^2 + 8x + 16$."
errores_frecuentes:
  - "El desarrollo de $(a + b)^2$ equivale a la suma de cuadrados $a^2 + b^2$ sin término central."
  - "Segunda afirmación falsa con expresiones en $LaTeX$."
  - "Tercera afirmación falsa con expresiones en $LaTeX$."
  - "Cuarta afirmación falsa con expresiones en $LaTeX$."
  - "Quinta afirmación falsa con expresiones en $LaTeX$."
afirmaciones_verdaderas:           # NUEVO desde 2026-08-04
  - "El desarrollo del cuadrado de binomio $(a + b)^2$ genera un trinomio $a^2 + 2ab + b^2$."
  - "Segunda afirmación cierta con expresiones en $LaTeX$."
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
| `explicacion_formal` | Sí | Markdown + LaTeX. Definición precisa con desglose de simbología de fórmulas y complemento didáctico final. |
| `definiciones_clave` | Sí | Términos nuevos en **negrita** con su definición. |
| `propiedades_relaciones` | Sí | Cómo se conecta con otros conceptos ya vistos. |
| `ejemplo_guiado` | Sí | Objeto `{enunciado, pasos}`. Un solo problema resuelto paso a paso **con datos concretos** (números/expresión propios del enunciado, no el nombre del recurso repetido en una frase molde — ver regla dura junto al YAML de ejemplo arriba). |
| `checkpoints` | Sí | **Exactamente 2** (`after_explicacion_formal` y `after_ejemplo_guiado`), 4 alternativas cada uno, 1 sola correcta. **Obligatorio:** todas las expresiones matemáticas en preguntas, alternativas y explicaciones deben usar $LaTeX$. `explanation` debe comenzar literalmente por "La alternativa correcta es '...'" mencionando la opción correcta. Validado por `node_checkpoint_service.normalize_node_checkpoints`. |
| `procedimiento` | Sí | Lista de pasos en orden. Mínimo 2, recomendado 3-4. Expresiones matemáticas escritas en $LaTeX$. |
| `errores_correccion` | Sí | Texto en Markdown que se muestra directamente en la sección visual **"Errores frecuentes y cómo corregirlos"**. Debe detallar 2-3 errores específicos del concepto y su respectiva forma de corregirlos (ej: `- **Error 1:** ... **Cómo corregirlo:** ...`). |
| `ejemplos` | Sí | **Mínimo 4**: 2 Tipo A (selección múltiple, 3 alternativas) + 2 Tipo B (Sí/No interactivos). Los Tipo B van al final. **Obligatorio:** enunciados, alternativas y pasos de solución deben expresar las fórmulas y términos en $LaTeX$. |
| `errores_frecuentes` | Sí | **Exactamente 5**. Afirmaciones falsas particularizadas en $LaTeX$. Deben ser **afirmaciones matemáticas declarativas directas pero FALSAS** que un alumno pudiera dar por verdaderas. Está **estrictamente prohibido** usar muletillas o aseveraciones como *"Confundir..."*, *"Pensar que..."*, *"Olvidar..."*, *"Creer..."*, *"Asumir..."*, *"Omitir..."*, *"Errar..."* o aseveraciones sobre *omitir* elementos (ya que delatan de inmediato que la frase es falsa sin leer la matemática). Se mezclan con `afirmaciones_verdaderas` en la sección "Ejemplos Verdadero/Falso". |
| `afirmaciones_verdaderas` | Sí | **Mínimo 2**. Afirmaciones ciertas sobre el tema en $LaTeX$, breves y verificables. Sin ellas, la sección V/F muestra solo "Falso" siempre. |
| `al_terminar_debes_poder` | Sí | 1-2 frases que indiquen explícitamente **QUÉ** podrá hacer el alumno y **CÓMO** lo ejecutará (el criterio, algoritmo o verificación explícita). |
| `fuente` | Recomendado | Nombre del libro y página. Ayuda a verificar. |
| `estado` | Sí | Usa `publicado` cuando el contenido está revisado. |

> **Nota — por qué existe `afirmaciones_verdaderas` (2026-08-04):** la sección
> "Ejemplos Verdadero/Falso" se construía únicamente desde `errores_frecuentes`,
> así que la respuesta correcta era siempre "Falso". La vista
> (`apps/learn/views.py::_true_false_items`) ahora mezcla ambos campos y los
> presenta en orden aleatorio por cada carga de página.

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
    "Alternativa A en $LaTeX$",
    "Alternativa B en $LaTeX$",
    "Alternativa C en $LaTeX$",
    "Alternativa D en $LaTeX$"
  ],
  "correct_choice_index": 0,           // 0, 1, 2 o 3
  "explanation": "Paso 1: ...\nPaso 2: ... (soporta $LaTeX$ y saltos de línea con \n)"
}
```
