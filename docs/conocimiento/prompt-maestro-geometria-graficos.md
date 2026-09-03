# 📐 Prompt Maestro — Estándar de Gráficos, Infografías y Contenido para Geometría (Eje 04)

> **Documento de Referencia Permanente** para la generación de diagramas geométricos vectoriales SVG (`intro.svg`, `ejemplos.svg`, `resumen.svg`) y archivos de contenido YAML en la Biblioteca de Conocimiento de ProfeOnline.

---

## 🎯 Objetivo y Filosofía Visual

En **Geometría**, los diagramas no son simples tarjetas de texto con fórmulas: **son construcciones geométricas vectoriales rigurosas**.

> [!IMPORTANT]
> **REGLA DE ORO OBLIGATORIA:**
> Está **estrictamente prohibido** construir arcos angulares, sectores o polígonos complejos mediante comandos SVG manuales arbitrarios (`<path d="M... A...">`), ya que producen distorsiones de dirección (*sweep-flag*) y desbordes de arcos tipo globo.
> **Todo dibujo geométrico DEBE generarse obligatoriamente mediante el motor de Matplotlib + $\LaTeX$ vectorial** (`matplotlib.patches.Wedge`, `Polygon`, `FancyArrowPatch` con `mathtext.fontset='cm'`).

---

## 🧠 Estándar de Construcción con Matplotlib + $\LaTeX$

1. **Sectores Angulares Exactos (`Wedge`):**
   Los arcos de abertura angular se generan exclusivamente con `matplotlib.patches.Wedge(center, radius, theta1, theta2)`, garantizando que el sector quede milimétricamente confinado dentro de los lados del ángulo o polígono, sin desbordes.
2. **Polígonos y Lados (`Polygon`):**
   Las figuras cerradas (triángulos, cuadriláteros) se generan con `matplotlib.patches.Polygon([pts], closed=True)`.
3. **Vectores y Rayos (`annotate` / `FancyArrowPatch`):**
   Los rayos y flechas direccionales se trazan con puntas de flecha proporcionales (`arrowstyle="-|>"` con `mutation_scale=14`).
4. **Rótulos Matemáticos en $\LaTeX$ Nativo (Computer Modern):**
   Todos los ángulos ($\alpha, \beta, \gamma, \theta$), vértices ($A, B, C, O$) y vectores ($\vec{OA}, \vec{OB}$) se posicionan como texto $\LaTeX$ puro (`ax.text(x, y, r'$\alpha$', fontsize=15, color='...')`).
5. **Incrustación Vectorial en SVG:**
   La figura de Matplotlib se guarda en memoria como SVG (`fig.savefig(buf, format='svg', transparent=True)`) y se incrusta limpiamente en el lienzo SVG principal como una imagen vectorial data-URI (`<image href="data:image/svg+xml;base64,..." />`).

---

## 🛠️ Plantilla Canónica del Motor de Geometría

```python
import io, base64, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge, FancyArrowPatch

matplotlib.rcParams['mathtext.fontset'] = 'cm'

def render_matplotlib_geometry_data_uri(fig):
    """Convierte una figura matplotlib en data-URI vectorial SVG con dimensiones exactas."""
    buf = io.BytesIO()
    fig.savefig(buf, format='svg', transparent=True, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)
    buf.seek(0)
    svg_bytes = buf.read()
    svg_text = svg_bytes.decode('utf-8')

    w_match = re.search(r'width="([0-9.]+)pt"', svg_text)
    h_match = re.search(r'height="([0-9.]+)pt"', svg_text)
    w_pt = float(w_match.group(1)) if w_match else 200
    h_pt = float(h_match.group(1)) if h_match else 150

    w_px = w_pt * 1.3333
    h_px = h_pt * 1.3333

    b64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}", w_px, h_px
```

---

## 📋 Estructura Canónica de las 3 Imágenes

| Imagen | Propósito | Componente Geométrico Clave |
|---|---|---|
| **`intro.svg`** | Anatomía y Definición | Lienzo Matplotlib con la construcción geométrica base (rayos, arcos $\theta$, vértices $O$, triángulo con $\alpha, \beta, \gamma$) + tarjeta hero $\LaTeX$ y panel de convenciones. |
| **`ejemplos.svg`** | Casos y Aplicaciones Visuales | **2 tarjetas simétricas con figuras dedicadas generadas por Matplotlib** (ej. $90^\circ$ perpendicular con símbolo $\llcorner$, $180^\circ$ opuestos, segmentos paralelos con $\parallel$, polígonos homotéticos) + desarrollo paso a paso y badge de resultado formal. |
| **`resumen.svg`** | Síntesis y Anti-patrones | Comparativa lado a lado entre el **Caso Válido** ($\checkmark$) y el **Caso Inválido / Error Frecuente** ($\times$) generados por Matplotlib + advertencias. |

---

## 🎨 Estándar Riguroso para `ejemplos.svg` (Zero-Empty-Cards)

> [!CAUTION]
> **PROHIBICIÓN ESTRICTA DE TARJETAS DE EJEMPLOS VACÍAS O SIN FIGURA:**
> Cada tarjeta conceptual ❶ y ❷ de `ejemplos.svg` DEBE contener una **figura geométrica vectorial completa generada con Matplotlib + $\LaTeX$** (`plot_ejemplo1()`, `plot_ejemplo2()` con dimensiones controladas $\approx 295 \times 135\text{px}$ e incrustadas como data-URI).
> Está **estrictamente prohibido dejar tarjetas de ejemplos vacías o solo con texto**.

### Componentes Obligatorios de cada Tarjeta de Ejemplo:
1. **Encabezado:** Badge circular numérico (❶ / ❷) + Título del ejemplo + Subtítulo conceptual.
2. **Figura Geométrica (Matplotlib):** Diagrama vectorial limpio que ilustra exactamente el problema geométrico abordado ($\approx 295 \times 135\text{px}$).
3. **Desglose Paso a Paso:** 2 a 3 pasos claros en lenguaje natural (`Paso 1: ...`, `Paso 2: ...`) con tipografía limpia en `<text class="desc">` y espaciado vertical regular ($\Delta y \approx 14\text{px}$).
4. **Insignia de Resultado (`badge-ok` / `badge-warn`):**
   - Título verde o rojo: `✓ CONCLUSIÓN Y RESULTADO` / `✗ CONCLUSIÓN Y RESULTADO`.
   - **Renderizado $\LaTeX$ puro en Computer Modern:** Renderizar **únicamente la expresión, fórmula o igualdad matemática final** (ej: `$\frac{AD}{DB} = \frac{AE}{EC} = 0{,}5 \Longrightarrow \overline{DE} \parallel \overline{BC}$` o `$\frac{AD}{DB} \neq \frac{AE}{EC} \Longrightarrow \overline{DE} \not\parallel \overline{BC}$`).
   - **PROHIBIDO:** Embutir oraciones completas en español dentro del modo matemático (`$La pendiente es m^\prime = 3, pues...$`), ya que colapsa los espacios, convierte el texto en cursiva y destruye la legibilidad.

---

## 🏛️ Estándar Riguroso para `resumen.svg` (Estructura de 3 Niveles — Zero-Collision)

> [!CAUTION]
> **PROHIBICIÓN ESTRICTA DE LISTAS DE VIÑETAS CON COORDENADAS ESTÁTICAS:**
> Queda **terminantemente prohibido** colocar viñetas o listas de texto arbitrarias (`<circle cx="50" cy="214">`, `<text y="216">`) debajo de títulos como `PUNTOS CLAVE PARA LA EVALUACIÓN` con coordenadas estáticas fijas, ya que producen colisión y solapamiento directo sobre el título.
> Todo `resumen.svg` en Geometría DEBE estructurarse obligatoriamente bajo el **patrón canónico de 3 niveles**:

### Estructura Canónica de 3 Niveles en `resumen.svg`:
1. **Nivel 1 (Superior — Hero Box, `y=64`, `height=72`):**
   - Tarjeta blanca destacada con borde suave.
   - Título superior: `TEOREMA CENTRAL` o `RELACIÓN FUNDAMENTAL`.
   - Fórmula central renderizada en Computer Modern $\LaTeX$ escalada proporcionalmente ($W_{\max} = 580\text{px}, H_{\max} = 38\text{px}$).
2. **Nivel 2 (Central — Comparativa Lado a Lado, `y=144`, `height=232`):**
   - **Tarjeta Izquierda (✓ Caso Válido / Teorema Cumplido, `width=315`, `x=25`):**
     - Encabezado verde: `✓ [Nombre del caso válido]`.
     - Construcción vectorial en Matplotlib ($295 \times 98\text{px}$) ilustrando el cumplimiento de la propiedad.
     - Descripción concisa en 2 líneas.
     - Badge inferior verde con fórmula matemática en $\LaTeX$ Computer Modern.
   - **Tarjeta Derecha (✗ Anti-patrón / Error Típico / Rectas Secantes, `width=315`, `x=360`):**
     - Encabezado rojo/ámbar: `✗ [Nombre del anti-patrón o caso fallido]`.
     - Construcción vectorial en Matplotlib ($295 \times 98\text{px}$) ilustrando el error frecuente o la ausencia de la propiedad.
     - Descripción concisa en 2 líneas advirtiendo por qué no se cumple.
     - Badge inferior rojo con la relación de advertencia en $\LaTeX$.
3. **Nivel 3 (Inferior — Alert Box, `y=384`, `height=82`):**
   - Recuadro ámbar completo de ancho $650\text{px}$.
   - Título: `⚠️ REGLA DE ORO PARA LA EVALUACIÓN`.
   - Descripción de 1 línea con el criterio práctico clave.
   - Fórmula matemática síntesis en $\LaTeX$ Computer Modern.

---

## 🖼️ Estándar Riguroso para `intro.svg` (Zero-Banner-Collision)

1. **Banner Superior Limpio (`y=16`, `height=48` a `52`):**
   - Badge temático (`TEOREMA DE TALES`, `CONGRUENCIA DE TRIÁNGULOS`).
   - Título del nodo en texto plano SVG (`font-size="13.5"`, `font-weight="800"`).
   - **PROHIBIDO:** Incrustar imágenes $\LaTeX$ dentro del banner superior que invadan o colisionen con el título. Toda fórmula debe ubicarse en tarjetas interiores dedicadas.
2. **Tarjeta Izquierda (Lienzo Conceptual, `width=315`, `height=274`):**
   - Título: `FIGURA GEOMÉTRICA CONCEPTUAL`.
   - Figura de Matplotlib grande y limpia ($295 \times 195\text{px}$).
   - Sub-caja inferior con la relación o razón en $\LaTeX$ ($288 \times 32\text{px}$).
3. **Tarjeta Derecha (Propiedades Fundamentales, `width=315`, `height=274`):**
   - Viñetas de colores (`#2563eb`, `#16a34a`, `#7c3aed`, `#dc2626`) con texto estructurado en 2 líneas auto-envueltas ($\le 38$ caracteres por línea).
4. **Tarjeta Inferior de Alerta / Definición Central (`y=358`, `height=106`):**
   - Título del principio o teorema con icono de alerta `⚠️`.
   - Enunciado claro y fórmula display en $\LaTeX$ centrada.

---

## 📐 Regla Estricta de Auto-Wrapping y Prevención de Desbordes (Zero-Overflow)

### 🛡️ Especificación de Dimensiones y Anchos Seguros
1. **Tarjeta Lateral de `intro.svg` (`rect width="310"` en `x="315"`):**
   - Espacio disponible para texto: $W_{\text{disponible}} = 310 - 36\text{px} = 274\text{px}$.
   - A `font-size="10.5"`, el límite estricto por línea es **36 a 38 caracteres**.
   - Toda descripción que supere los 36 caracteres DEBE dividirse en múltiples líneas `<text>` o `<tspan>` con salto de línea vertical (`line_height=14px`).
2. **Caja Completa de Advertencias (`resumen.svg` y `intro.svg`, `width="640"`):**
   - Espacio disponible para texto: $W_{\text{disponible}} \approx 590\text{px}$.
   - A `font-size="11.5"`, el límite estricto por línea es **68 a 72 caracteres**.
3. **Escalamiento Bidireccional Automático en Fórmulas $\LaTeX$:**
   Toda inserción de imágenes $\LaTeX$ en SVG DEBE calcular su escala usando:
   $$\text{scale} = \min\left(1.0, \frac{W_{\max}}{W_{\text{px}}}, \frac{H_{\max}}{H_{\text{px}}}\right)$$
   - Tarjetas de `ejemplos.svg` ($W_{\text{card}} = 315\text{px}$): $W_{\max} = 260\text{px}$, $H_{\max} = 50\text{px}$.
   - Badges de resultado: $W_{\max} = 250\text{px}$, $H_{\max} = 34\text{px}$.
   - Hero Formula en `intro.svg` / Banner: $W_{\max} = 580\text{px}$, $H_{\max} = 65\text{px}$.
   - Tarjetas de alerta / Resumen: $W_{\max} = 560\text{px}$, $H_{\max} = 50\text{px}$.

---

## 📝 Estándar Canónico para Archivos YAML de Contenido (12 Secciones)

### 1. Sección Verdadero / Falso (`errores_frecuentes` y `afirmaciones_verdaderas`)

> [!IMPORTANT]
> **ESTRUCTURA ESTRICTA DE LISTA DE CADENAS (STRINGS):**
> - **`errores_frecuentes`**: DEBE ser una **lista de cadenas (strings)** donde cada elemento es una **afirmación matemática declarativa directa pero FALSA** (ej: `- 'En una homotecia con razón negativa, los lados dejan de ser paralelos.'`).
>   - **PROHIBIDO:** Estructurar `errores_frecuentes` como diccionarios (`- error: ..., correccion: ...`), ya que la vista del frontend inyecta el objeto directamente en el componente de Verdadero/Falso produciendo strings rotos como `"{'error': '...', 'correccion': '...'}"`.
>   - **PROHIBIDO:** Usar meta-lenguaje que delate la falsedad (*"Confundir..."*, *"Pensar que..."*, *"Olvidar..."*, *"Creer..."*).
> - **`afirmaciones_verdaderas`**: DEBE ser una **lista de cadenas (strings)** con afirmaciones ciertas y precisas sobre el tema.
> - **`errores_correccion`**: Campo de texto Markdown independiente con viñetas explicativas detalladas para la sección visual de advertencias.

### 2. Sintaxis Segura de Fórmulas $\LaTeX$ en YAML (Comillas Simples)
- Toda lista en YAML con fórmulas $\LaTeX$ que contenga barras invertidas (`\overline`, `\vec`, `\parallel`, `\prime`, `\frac`) DEBE usar **comillas simples** (`'...'`) para evitar que el parser de YAML interprete secuencias de escape inválidas (como `\o` en `\overline`).
- Las comillas simples internas se escapan duplicándolas (`''`).

### 3. Comprobaciones Formativas (`checkpoints` — Zero-Placeholders & Match Literal)
- **Exactamente 4 alternativas por pregunta:** Cada pregunta debe tener 4 opciones (`choices`), 1 verdadera (`is_correct: true`) y 3 falsas (`is_correct: false`).
- **Prohibición de alternativas de relleno (*dummy options*):** Queda **terminantemente prohibido** incluir textos genéricos como `'Opción incorrecta de prueba A'`, `'Opción incorrecta secundaria 1'` o `'Valor incorrecto 1'`. Todos los distractores deben formular errores conceptuales reales verosímiles.
- **Regla Estricta de Validación Backend:** El texto del campo `explanation` DEBE contener textualmente la cadena completa de la alternativa correcta (`correct_text.casefold() in explanation.casefold()`), de lo contrario el comando `manage.py load_node_content` rechazará el archivo con error de validación.
- **Fórmulas delimitadas:** Toda expresión matemática en `question`, `choices` y `explanation` debe estar rigurosamente delimitada con signos de dólar (`$...$`).

---

## 🏛️ Estándar de Explicación Formal Estructurada (3 Niveles Obligatorios)

```yaml
explicacion_formal: |
  ### Definición formal
  [Contexto geométrico, hipótesis rigurosa, pertenencia a conjuntos espaciales o planos R², y enunciado axiomático del teorema o definición]

  $$\text{Fórmula o Relación Central en Bloque LaTeX Display}$$

  ### Desglose simbólico y geométrico
  - $Símbolo_1$: Significado formal y rol en la figura geométrica.
  - $Símbolo_2$: Propiedad o medida asociada.
  - $Símbolo_3$: Relación métrica, angular o de paralelismo/congruencia.

  ### Síntesis didáctica
  [Síntesis técnica precisa que resuma qué garantiza la propiedad o teorema en el marco de la geometría euclidiana.]
```
