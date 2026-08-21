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
# ⚠️ TERCERA REGLA DURA (agregada 2026-08-07, actualizada 2026-08-18): Expresiones matemáticas en LaTeX
# TODAS las expresiones matemáticas (variables, ecuaciones, polinomios, números con exponentes,
# números decimales con barra periódica como $0,\overline{3}$ o $2,45\overline{8}$, fracciones, alternativas, enunciados)
# en las secciones `checkpoints` ("Comprueba tu avance"), `ejemplos` ("Ejemplos")
# y `errores_frecuentes` / `afirmaciones_verdaderas` ("Ejemplos Verdadero/Falso") DEBEN estar encerradas
# obligatoriamente entre signos de dólar ($...$ o $$...$$) para su renderizado profesional mediante KaTeX.
# Está ESTRICTAMENTE PROHIBIDO dejar comandos LaTeX (\overline, \frac, etc.) en texto plano sin delimitar por $.
#
# ⚠️ CUARTA REGLA DURA (agregada 2026-08-16): Prohibición estricta de ejemplos pasivos ("Ver solución")
# TODOS los ejercicios en la sección `ejemplos` DEBEN ser interactivos para que el estudiante responda
# activamente antes de ver la retroalimentación. Está ESTRICTAMENTE PROHIBIDO redactar ejemplos de respuesta
# abierta que carezcan de opciones y caigan en el botón pasivo "Ver solución".
# - En selección múltiple (Tipo A): DEBE definirse la lista `alternativas:` (mínimo 3 opciones) y `respuesta:`
#   coincidiendo exactamente con la opción correcta.
# - En ejercicios Sí/No (Tipo B): `respuesta:` DEBE ser exactamente "Sí" o "No" (o definir `alternativas:`).
#
# ⚠️ QUINTA REGLA DURA (agregada 2026-08-17): Estructura obligatoria QUÉ y CÓMO en "Al terminar debes poder"
# El campo `al_terminar_debes_poder` DEBE estructurarse obligatoriamente con las dos etiquetas explícitas:
# 1. `QUÉ:` — Acción o capacidad matemática concreta lograda por el estudiante.
# 2. `CÓMO:` — Mecanismo, algoritmo o criterio técnico específico de resolución en $LaTeX$.
# Si el nodo cuenta con infografía de síntesis, la etiqueta `![...](/static/img/nodos/...)` se ubica al inicio.
# Queda ESTRICTAMENTE PROHIBIDO redactar párrafos de texto corrido sin estas dos etiquetas, ya que la plataforma
# las utiliza para construir y enmarcar automáticamente las dos tarjetas visuales independientes (`🎯 QUÉ` y `⚙️ CÓMO`).
#
# ⚠️ SEXTA REGLA DURA (agregada 2026-08-17, actualizada 2026-08-18): Estándar Zero-Overflow y Períodos en SVG
# Todo archivo SVG generado para los nodos (`static/img/nodos/*.svg`) DEBE cumplir estrictamente con:
# 1. Anclaje derecho seguro: Todo texto o badge ubicado en el extremo derecho de un contenedor/píldora DEBE
#    usar obligatoriamente `text-anchor="end"` con padding interior (`x = rect_x + rect_width - 16`).
# 2. Límite de caracteres por contenedor y subcaja (Fórmula Universal Zero-Overflow):
#    Para cualquier contenedor o sub-caja interna (cajas comparativas $p$ vs $\neg p$, badges, píldoras, etc.)
#    de ancho $W_{\text{box}}$ y fuente $F_s$:
#    $$N_{\text{max}} \le \frac{W_{\text{box}} - (2 \times \text{padding})}{F_s \times 0.60}$$
#    En cajas centrales de 650px a 12px, el largo máximo no debe superar los 65 caracteres. Dividir fórmulas
#    largas en dos líneas o simplificar rotulaciones para no tocar los bordes del recuadro.
# 3. Representación de Períodos Decimales en SVG:
#    PROHIBIDO usar caracteres combinados Unicode (como `\u0304` / COMBINING MACRON `̄`) sobre números en SVG,
#    ya que solo cubren un dígito en números multídígito y causan desalineación visual.
#    En su lugar, usar OBLIGATORIAMENTE `<tspan style="text-decoration: overline">54</tspan>` o una línea vectorial
#    `<line>` para garantizar una barra continua, nítida y perfectamente alineada sobre todos los dígitos periódicos.
# 4. Tipografía Matemática Vectorial (Subíndices y Superíndices):
#    PROHIBIDO usar notación plana de programador con guiones bajos o símbolos crudos (`E_%`, `E_rel`, `E_abs`,
#    `v_real`, `v_aprox`, `x_def`, `x_exc`, `d_k`, `d_{k+1}`, `10^-k`, `10^k`) dentro de elementos SVG.
#    En su lugar, usar OBLIGATORIAMENTE `<tspan baseline-shift="sub" font-size="70%">...</tspan>` para subíndices y
#    `<tspan baseline-shift="super" font-size="70%">...</tspan>` para superíndices (o variantes con estilo),
#    garantizando una tipografía matemática profesional, estética y perfectamente renderizada en navegadores.
# 5. Margen de seguridad: Ningún texto puede quedar a menos de 15px de los bordes del canvas (`viewBox`) o de su caja contenedora.
# 7. Textos multilinea y Salto Automático (Zero-Clipping):
#    Dado que SVG 1.1 `<text>` no realiza salto de línea automático, está ESTRICTAMENTE PROHIBIDO
#    colocar textos explicativos largos en un solo `<text>` plano sin saltos. Todo texto descriptivo,
#    definición o aviso debe dividirse obligatoriamente en múltiples elementos `<tspan x="..." y="...">`
#    con límites estrictos de caracteres por línea ($\le 68$ caracteres para cajas de ancho completo
#    de 640px y $\le 34$ caracteres para tarjetas de 305px), recalculando la altura del contenedor
#    y la posición $Y$ de las cajas siguientes.
# 8. Fracciones Matemáticas Verticales en SVG:
#    PROHIBIDO usar notación plana horizontal de programador con barra inclinada (`a / b`, `1 / (√3 - 1)`,
#    `6 / √3`, `(a·d + b·c) / 12`, `(3² - 5) = 4`) dentro de diagramas SVG.
#    En su lugar, toda fracción o división en SVG DEBE representarse obligatoriamente en formato vertical
#    apilado: un elemento `<text>` para el numerador en la parte superior, una línea horizontal vectorial
#    `<line x1="..." y1="..." x2="..." y2="..." stroke="..." stroke-width="1.5"/>` en el medio, y un elemento
#    `<text>` para el denominador en la parte inferior, con los signos operativos ($\cdot$, $=$, $+$, $-$)
# ⚠️ SÉPTIMA REGLA DURA (agregada 2026-08-19): Estándar LaTeX Vectorial en Imágenes SVG (Computer Modern)
# Toda fórmula matemática o expresión con radicales, fracciones, potencias o variables dentro de los diagramas
# e infografías SVG (`static/img/nodos/*.svg`) DEBE renderizarse con tipografía formal $\LaTeX$ (Computer Modern).
# Queda ESTRICTAMENTE PROHIBIDO usar notación plana de programador como `3√(x)`, `4x^(2/3)`, `ⁿ√(xᵐ)`, `x^(m/n)`.
# Al generar los fragmentos con el motor de Python (`matplotlib.mathtext`), se DEBE asegurar apagar totalmente los
# ejes (`ax.set_axis_off()`) para evitar la aparición accidental de marcas de graduación o números en el origen `(0, 0)`.
#
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
    respuesta: "Sí"          # o "No" obligatoriamente
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
  ![Resumen del cuadrado de binomio](/static/img/nodos/cuadrado-de-binomio-resumen.svg)

  QUÉ: Desarrollar y expandir algebraicamente el cuadrado de un binomio suma $(a + b)^2$ y resta $(a - b)^2$.

  CÓMO: Aplicar el algoritmo notable calculando el cuadrado del primer término, sumando o restando el doble producto de ambos términos y sumando el cuadrado del segundo término ($a^2 \pm 2ab + b^2$).
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
| `ejemplos` | Sí | **Mínimo 4**: 2 Tipo A (selección múltiple con lista `alternativas:`) + 2 Tipo B (con `respuesta: "Sí"` o `"No"`). **PROHIBIDO:** redactar ejemplos pasivos sin opciones que caigan en "Ver solución". **Obligatorio:** enunciados, alternativas y pasos de solución deben expresar las fórmulas y términos en $LaTeX$. |
| `errores_frecuentes` | Sí | **Exactamente 5**. Afirmaciones falsas particularizadas en $LaTeX$. Deben ser **afirmaciones matemáticas declarativas directas pero FALSAS** que un alumno pudiera dar por verdaderas. Está **estrictamente prohibido** usar palabras como *"Confundir..."*, *"Pensar que..."*, *"Olvidar..."*, *"Creer..."*, *"Asumir..."*, *"Omitir..."*, *"Errar..."*, *"Cometer errores..."*, *"Error..."*, *"La suposición..."*, *"Suposición..."*, *"Suponer..."*, *"La creencia..."*, *"Creencia..."* ni ninguna palabra o forma de redacción que haga referencia o delate que lo que se está diciendo es falso solo por la forma de decirlo (meta-lenguaje). Se mezclan con `afirmaciones_verdaderas` en la sección "Ejemplos Verdadero/Falso". |
| `afirmaciones_verdaderas` | Sí | **Mínimo 2**. Afirmaciones ciertas sobre el tema en $LaTeX$, breves y verificables. Sin ellas, la sección V/F muestra solo "Falso" siempre. |
| `al_terminar_debes_poder` | Sí | **Obligatorio: Estructura explícita `QUÉ:` y `CÓMO:`** (e infografía de síntesis al inicio si aplica). Define la acción concreta (`QUÉ`) y el algoritmo o mecanismo técnico de resolución (`CÓMO`) con términos matemáticos precisos en $LaTeX$. **PROHIBIDO:** redactar párrafos de texto corrido sin estas etiquetas. Alimenta automáticamente las dos tarjetas visuales independientes `🎯 QUÉ` y `⚙️ CÓMO`. |
| `fuente` | Recomendado | Nombre del libro y página. Ayuda a verificar. |
| `estado` | Sí | Usa `publicado` cuando el contenido está revisado. |

> **Nota — por qué existe `afirmaciones_verdaderas` (2026-08-04):** la sección
> "Ejemplos Verdadero/Falso" se construía únicamente desde `errores_frecuentes`,
> así que la respuesta correcta era siempre "Falso". La vista
> (`apps/learn/views.py::_true_false_items`) ahora mezcla ambos campos y los
> presenta en orden aleatorio por cada carga de página.

> **Nota — redacción del campo `al_terminar_debes_poder`:** Este campo no debe ser una frase genérica ni un molde de relleno. Debe responder siempre a dos aspectos integrados:
> 1. **QUÉ (Objetivo):** Acción o capacidad concreta que logrará el alumno (ej: *determinar el dominio*, *graficar la traslación*, *modelar la potencia eólica*).
> 2. **CÓMO (Mecanismo explícito):** El procedimiento matemático o algoritmo técnico específico para resolverlo (ej: *igualando a cero el binomio interno $(x-h)=0$*, *excluyendo las raíces del denominador*, *clasificando en orden decreciente de exponentes y sumando los coeficientes de los términos semejantes*).
> 3. **SIN AMBIGÜEDAD (Precisión de objetos y operaciones):** El CÓMO debe especificar con claridad los objetos matemáticos involucrados (ej. *exponentes*, *grados*, *coeficientes numéricos*, *bases*) y la operación matemática exacta ejecutada, evitando abstracciones vagas.

> **Nota — signos de moneda y montos en dinero en YAML (KaTeX):** Todo monto monetario con signo peso (ej: $\$500.000$) DEBE estar estrictamente delimitado dentro de un bloque LaTeX como `$\$500.000$` o `$\$500.000\text{ pesos}$`. Está **estrictamente prohibido escribir `\$500.000` o `$500.000` suelto en texto plano sin cerrar**, ya que Markdown consume la barra invertida (`\`) y el renderizador de KaTeX en el cliente toma el signo `$` como apertura de fórmula matemática, devorando todo el texto en español siguiente (eliminando espacios, volviendo cursivas las palabras y convirtiendo guiones bajos en subíndices).

> **Nota — estándar LaTeX vectorial en diagramas e infografías SVG:** Toda fórmula matemática, ley de correspondencia, fracción apilada ($\frac{a}{b}$), radical ($\sqrt[n]{x}$), exponente o ejemplo algebraico dentro de las tarjetas ❶ y ❷ de los diagramas SVG (`card1_latex`, `card2_latex`) DEBE renderizarse obligatoriamente como fragmento vectorial $\LaTeX$ con tipografía Computer Modern (`render_latex_data_uri` vía `scratch/svg_latex_helper.py`). Está **estrictamente prohibido escribir fórmulas matemáticas en texto plano o con barras/radicales ASCII/Unicode (`5 / x³`, `2 · ³√x`, `a / x^k`, `a · x^-k`, `ⁿ√x`) dentro de las tarjetas o descripciones**. Los títulos de alerta y tarjetas deben redactarse exclusivamente en lenguaje natural en español formal.

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

---

## 4. Buenas prácticas de economía de tokens y gestión de contexto en la edición masiva

> **Remedio de token bloat:** Agregado 2026-08-13 tras análisis de consumo de tokens durante actualizaciones por lotes.

1. **Loteado acotado de actualizaciones (máximo 2-3 archivos por turno):**
   - No realizar más de 3 reemplazos/actualizaciones masivas de contenido YAML en un mismo turno de la IA para prevenir que la acumulación de diffs infle exponencialmente el contexto activo (*prompt window*).
2. **Pausas activas y confirmación entre subtemas:**
   - Detener la llamada de herramientas al completar un subtema completo (ej. `03.08.06`), reportar el avance al usuario y continuar en un turno limpio para liberar memoria.
3. **Delegación a scripts o subagentes para reescritura masiva:**
   - Si se requiere actualizar decenas de archivos YAML con la misma pauta, preferir la creación de scripts de transformación (Python) o subagentes aislados (`invoke_subagent`) para aislar la manipulación de texto largo del hilo principal.
4. **Respeto a las reglas de economía de tokens (`AGENTS.md`):**
   - Si una tarea empieza a inflar el conteo de tokens por lecturas repetidas, avisar inmediatamente al usuario y proponer la alternativa de menor consumo antes de continuar.
