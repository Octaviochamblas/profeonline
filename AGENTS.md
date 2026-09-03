# Guía para Codex — ProfeOnline

## 📋 Documentación y flujo de tareas

> **Lee primero `docs/README.md`** — es el índice maestro: da el contexto del proyecto y el mapa
> de qué leer según tu tarea. Las reglas de trabajo vigentes están en `docs/gobernanza/`.

El trabajo se gestiona con un **Kanban-pipeline** en `docs/backlog/` (cada etapa = dueño activo;
la IA dueña mueve la tarjeta con `git mv` al pasar su gate):

- **`backlog/1-por-iniciar/`** — backlog de ideas. Cada idea es un `.md` propio (usar `_plantilla.md`).
- **`backlog/2-arquitectura/`** — 🏛️ Claude redacta handoff + criterios (🧩 Codex hace preflight).
- **`backlog/3-construccion/`** — 🔨 Antigravity implementa en una rama.
- **`backlog/4-auditoria/`** — 🧩 Codex audita el diff (tests, N+1, migraciones).
- **`backlog/5-cierre/`** — 🏛️ Claude auditoría final + `squash-merge`.
- **`backlog/6-finalizados/`** — terminadas.
- **`reportes-sesion/`** — un reporte por sesión (`AAAA-MM-DD.md`).

### Reglas (seguir siempre)

1. **Al INICIAR una sesión:** seguir el *protocolo barato de lectura* de `docs/README.md`:
   `docs/_coordinacion/ESTADO.md` + el reporte más reciente de `reportes-sesion/` + la tarjeta
   activa (Codex no recuerda sesiones anteriores). **No "leer todo".**
2. **Idea nueva** → crear un `.md` en `backlog/1-por-iniciar/` basado en `_plantilla.md`.
3. **Cada IA, al pasar su gate, mueve la tarjeta** con `git mv` a la siguiente etapa
   (detalle del pipeline en `docs/gobernanza/proceso-multiagente.md`).
4. **Al cerrar (merge)** → completar **"Qué se hizo"** y mover con `git mv` a `backlog/6-finalizados/`.
5. **Al FINALIZAR una sesión:** escribir `reportes-sesion/AAAA-MM-DD.md`
   (usar `_plantilla-reporte.md`) con todo lo avanzado **desde el reporte anterior**.

> Mover archivos siempre con `git mv` para conservar el historial.

## ⚙️ Convenciones técnicas del proyecto

- **Settings:** `config.settings.local` (dev, por defecto en `manage.py`) /
  `config.settings.production` (producción en Railway).
- **Tests:** La suite completa (`python manage.py test`) + `check --deploy` son la
  **barrera real en CI** (`.github/workflows/django_ci.yml`); Railway está configurado con
  *Wait for CI* para no desplegar si CI falla. El **pre-commit** se mantiene rápido a
  propósito: solo corre `check` + `makemigrations --check` (el entry usa
  `.venv\\Scripts\\python.exe`). Aun así, corre los tests localmente antes de pushear.
- **Despliegue:** push a `main` → Railway despliega. El *Custom Start Command*
  corre `migrate && ensure_admin && ensure_site && seed_math_resources && gunicorn`.
- **Email:** API HTTP de Brevo (`BREVO_API_KEY`); Railway bloquea puertos SMTP.
- **Errores:** Sentry (`SENTRY_DSN`) — proyecto `python-django` en org `particular-lw`.
- **Login con Google:** allauth, credenciales en `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.
- **CSP:** con nonce por petición (`apps/core/middleware.py`).
- **Auditorías:** vigentes en `docs/auditorias/`; las antiguas en `docs/auditorias/_archivo-2026-05-30/`.
- **Recursos teóricos:** la API reconoce el perfil versionado
  `guide.profile="teorico-interactivo-v1"` y debe validar su estructura, tres
  comprobaciones y briefs visuales. Contrato backend en
  `docs/gobernanza/estandar-editorial-recursos-teoricos.md`; plantilla de autoría
  en el repo hermano `profeonline-uploader/docs/estandar-recurso-teorico-interactivo.md`.
- **Ejemplos en recursos (12 secciones):** Todos los ejercicios de la sección `ejemplos`
  deben ser interactivos (Tipo A con `alternativas:` o Tipo B con `respuesta: "Sí"` / `"No"`).
  Está **estrictamente prohibido** redactar ejemplos de respuesta abierta o pasivos que
  caigan en el botón "Ver solución" (pauta en `docs/conocimiento/pauta-contenido.md`).
- **Al terminar debes poder (12 secciones):** Debe estar estructurado obligatoriamente con
  las dos etiquetas explícitas `QUÉ:` (acción o capacidad matemática) y `CÓMO:` (mecanismo o
  algoritmo técnico de resolución en $LaTeX$). Prohibido redactar párrafos de texto corrido
  sin estas etiquetas (pauta en `docs/conocimiento/pauta-contenido.md`).
  - **Prohibición de Frase Literal "en LaTeX":** La directiva de usar $LaTeX$ es una norma tipográfica para delimitar fórmulas ($...$). Queda **estrictamente prohibido escribir frases literales como `"en LaTeX"`, `"en $LaTeX$"` o `"en $\LaTeX$"`** al final o dentro de las oraciones explicativas dirigidas al estudiante.
- **Formato Estricto de Procedimientos (`procedimiento: list[str]`):** El campo `procedimiento` en archivos YAML de contenido y en base de datos (`NodeContent.procedimiento`) DEBE ser obligatoriamente una **lista de cadenas (`list[str]`)** con los pasos numerados. Queda **estrictamente prohibido guardarlo como string multilínea (`str`)**, ya que la plantilla Django iteraría carácter por carácter generando cientos de etiquetas `<li>` vacías que expanden y desconfiguran la página.
- **Renderizado Limpio de Ejemplos de Selección Múltiple (Tipo A):** En los ejercicios interactivos de `ejemplos`, las alternativas se normalizan para extraer el texto limpio de cada opción y asignar la respuesta correcta a `respuesta:` (a partir de `is_correct: True`). Queda **estrictamente prohibido renderizar representaciones crudas de diccionarios de Python (`{'text': ...}`) en los botones de opciones del cliente**.
- **Complemento Didáctico Obligatorio en Recursos Teóricos:** En todo archivo YAML de contenido (`docs/conocimiento/contenido/`), la sección `explicacion_formal` DEBE incluir obligatoriamente al final un bloque de cita destacado con la etiqueta `> **Complemento didáctico:** <texto explicativo, intuición matemática, mnemotecnia o advertencia conceptual en $LaTeX$>`. Queda **estrictamente prohibido** omitir el bloque de Complemento didáctico en cualquier recurso teórico (pauta en `docs/conocimiento/pauta-contenido.md`).
- **Notación de Arcos en LaTeX (KaTeX):** Para representar arcos de circunferencia, se DEBE usar obligatoriamente `\overset{\frown}{AB}` o `\overset{\frown}{TA}` (o texto natural "arco $AB$"). Queda **estrictamente prohibido usar comandos LaTeX no estándar como `\wideparen{...}`**, ya que el renderizador de KaTeX no los interpreta nativamente y los dibuja como texto de error en color marrón/rojo.
- **Fórmulas y Matemáticas en YAML (KaTeX):** Toda expresión matemática, fracción o número decimal con barra periódica ($0,\overline{3}$, $2,45\overline{8}$) en enunciados, alternativas, explicaciones o títulos de `ejemplos` y `checkpoints` DEBE estar estrictamente delimitada con signos de dólar (`$...$` o `$$...$$`). Prohibido dejar comandos LaTeX como `\overline` en texto plano.
- **Signos de Moneda / Dinero en YAML (KaTeX):** Todo monto monetario con signo peso (ej: $\$500.000$) DEBE estar estrictamente delimitado dentro de un bloque LaTeX como `$\$500.000$` o `$\$500.000\text{ pesos}$`. Está **estrictamente prohibido escribir `\$500.000` o `$500.000` suelto en texto plano sin cerrar**, ya que Markdown consume la barra invertida (`\`) y el renderizador de KaTeX en el cliente toma el signo `$` como apertura de fórmula matemática, devorando todo el texto en español siguiente (eliminando espacios, volviendo cursivas las palabras y convirtiendo guiones bajos en subíndices).
- **Infografías y Diagramas SVG:** Todo SVG (`static/img/nodos/`) debe respetar el estándar
  *Zero-Overflow*: textos derechos anclados con `text-anchor="end"`, padding seguro $\ge 15\text{px}$,
  y control estricto de longitud de caracteres por caja contenedora y subcaja interna
  ($N_{\text{max}} \le \frac{W_{\text{box}} - 2 \times \text{padding}}{\text{font-size} \times 0.60}$).
  Prohibido desbordar los bordes de subcajas, cards o del canvas.
  - **Uso Obligatorio del Motor Central (`scratch/svg_latex_helper.py`):** Toda generación futura de diagramas SVG (`intro`, `ejemplos`, `resumen`) DEBE importar y utilizar obligatoriamente las funciones del motor central `scratch/svg_latex_helper.py` (`build_intro_latex_svg`, `build_ejemplos_latex_svg`, `build_resumen_latex_svg`). Este módulo implementa por diseño el estándar *Zero-Overflow*, auto-wrapping dinámico, escape de entidades XML, sanitización de mathtext y renderizado vectorial $\LaTeX$.
  - **Renderizado $\LaTeX$ Vectorial en Tarjetas y Cajas de Diagramas (`card1_latex`, `card2_latex` en `intro.svg`, `ejemplos.svg`):** Toda expresión matemática, fórmula, ecuación, fracción, radical o ejemplo algebraico dentro de las tarjetas conceptuales ❶ y ❷ de `intro.svg` y `ejemplos.svg` DEBE renderizarse obligatoriamente como un fragmento vectorial $\LaTeX$ con tipografía Computer Modern (`render_latex_data_uri` vía `card1_latex` / `card2_latex`). Está **estrictamente prohibido escribir fórmulas o expresiones matemáticas en texto plano o con barras/radicales ASCII/Unicode (`5 / x³`, `2 · ³√x`, `a / x^k`, `a · x^-k`, `ⁿ√x`) dentro de las tarjetas o descripciones**.
  - **Renderizado $\LaTeX$ Vectorial de Badges e Insignias (`ejemplos.svg`):** Toda insignia de resultado o badge verde (`badge-ok`) en `ejemplos.svg` DEBE renderizarse obligatoriamente como un fragmento vectorial $\LaTeX$ con tipografía Computer Modern (`<image href="data:image/svg+xml;base64,..." />` generado con `render_latex_data_uri`). Está **estrictamente prohibido renderizar expresiones matemáticas o conjuntos solución en `<text>` plano o usar operadores crudos de programador (`<=`, `>=`, `!=`, `+inf`, `-inf`, `U`, `]-inf`, `[a, +inf[`) en badges o cajas**.
  - **Títulos y Encabezados de Alerta Limpios (`intro.svg`, `resumen.svg`):** Los parámetros de título (`title`, `alert_title`, `card1_title`, `card2_title`) deben redactarse exclusivamente en **lenguaje natural en español formal** (ej: `⚠️ Regla de Oro: Inecuaciones con Valor Absoluto Mayor o Igual`, `⚠️ Regla de Oro: Reescribir Fracciones y Radicales como Potencias`), sin incrustar notación de programador (`|x| >= k`, `(x <= -k o x >= k)`, `a / x^k`, `ⁿ√x`). Toda la matemática asociada debe enviarse a través de los campos formales `card1_latex`, `card2_latex`, `sub_latex` y `main_latex` para su renderizado tipográfico $\LaTeX$.
  - **Escape Estricto de Entidades XML (Zero-Broken-Images):** Todo texto dentro de `<tspan>` o `<text>` en SVG 1.1 DEBE escapar estrictamente los caracteres reservados de XML (`<` $\to$ `&lt;`, `>` $\to$ `&gt;`, `&` $\to$ `&amp;`, `"` $\to$ `&quot;`). Prohibido insertar `<` o `>` sueltos dentro del XML de un SVG, ya que corrompe el parser del navegador y produce una imagen rota.
  - **Auto-Wrapping y Salto de Línea en SVG (Zero-Clipping):** Dado que SVG 1.1 `<text>` no realiza salto de línea automático, está **estrictamente prohibido colocar textos explicativos largos en un solo `<text>` plano**. Todo texto descriptivo, definición o aviso debe formatearse obligatoriamente mediante múltiples elementos `<tspan x="..." y="...">` con límites de caracteres por línea ($\le 68$ caracteres para cajas de ancho completo $\approx 640\text{px}$ y $\le 34$ caracteres para tarjetas divididas $\approx 305\text{px}$), recalculando dinámicamente la altura de la caja contenedora y la posición $Y$ de las cajas siguientes.
  - **Períodos Decimales en SVG:** En números periódicos en SVG, está **estrictamente prohibido usar caracteres combinados Unicode (`\u0304`)**; usar siempre `<tspan style="text-decoration: overline">...</tspan>` o un elemento vectorial `<line>` para cubrir la totalidad del período.
  - **Prohibición de Notación Plana de Programador:** En expresiones matemáticas dentro de SVGs, está **estrictamente prohibido usar notación plana de programador con guiones bajos o símbolos crudos** (`E_%`, `E_rel`, `v_real`, `x_def`, `d_k`, `10^-k`, `10^k`, `3√(x)`, `4x^(2/3)`, `ⁿ√(xᵐ)`, `x^(m/n)`, `<=`, `>=`, `!=`, `+inf`, `-inf`, `U`); usar siempre etiquetas tipográficas vectoriales o **renderizado vectorial $\LaTeX$ con Computer Modern** (`matplotlib.mathtext` con `ax.set_axis_off()` incrustado como vector data-URI/image).
- **Estándar $\LaTeX$ Vectorial en Imágenes SVG (Computer Modern):** Toda fórmula matemática o expresión con radicales, fracciones, potencias o variables dentro de los diagramas e infografías SVG DEBE renderizarse con tipografía formal $\LaTeX$ (Computer Modern). Al generar los fragmentos con el motor de Python, se debe asegurar apagar totalmente los ejes (`ax.set_axis_off()`) para evitar la aparición accidental de marcas de graduación o números en el origen `(0, 0)`.
- **Fracciones Matemáticas en Diagramas SVG:** Toda fracción, división o cociente algebraico o numérico
  en diagramas SVG (`static/img/nodos/`) DEBE representarse obligatoriamente en formato vertical apilado
  con numerador superior, línea horizontal vectorial de fracción (`<line>`) y denominador inferior, con
  los operadores matemáticos ($\cdot$, $=$, $+$, $-$, $\implies$) alineados al centro de la barra. Está **estrictamente
  prohibido** usar notación plana con barra inclinada (`a / b`, `1 / (√3 - 1)`, `6 / √3`, `(a·d + b·c) / 12`)
  en infografías o diagramas explicativos. En contenido YAML, usar siempre $\LaTeX$ vertical $\frac{a}{b}$ en `$...$`.
  - **Geometría de Fracciones y Prevención de Solapamiento (Zero-Collision):**
    1. *Ancho de barra y texto:* La barra de fracción `<line>` debe cubrir holgadamente el texto más ancho ($W_{\text{line}} \ge \max(W_{\text{num}}, W_{\text{den}}) + 20\text{px}$). Prohibido centrar texto largo sobre una línea corta.
    2. *Espaciado horizontal acumulativo:* Al encadenar operadores y fracciones (`N = \frac{A}{B} ⟹ Escala = 1 : N`), la coordenada $X$ de cada elemento siguiente DEBE calcularse sumando el ancho real del elemento anterior más un espacio de separación seguro ($X_{\text{siguiente}} = X_{\text{inicio}} + W_{\text{fracción}} + \text{gap} \ge 25\text{px}$). Prohibido usar desplazamientos fijos pequeños que causen que el texto del numerador/denominador invada o solape el signo igual u otros operadores contiguos.
    3. *Alineación vertical y separación:* Para una barra en $y_{\text{barra}}$ y fuente de tamaño $F$: numerador en $y_{\text{barra}} - 7\text{px}$, denominador en $y_{\text{barra}} + F + 3\text{px}$, y operadores centrados con la barra en $y_{\text{barra}} + \frac{F}{3}$. La caja o badge contenedora de la fórmula debe tener altura mínima $H \ge 65\text{px}$ para contener la fracción sin rozar los bordes.
    4. *Prohibición de guiones bajos crudos:* Prohibido escribir `D_real`, `D_plano`, `c_A`, `Parte_i` en SVG. Usar siempre etiquetas tipográficas `<tspan baseline-shift="sub" font-size="70%">...</tspan>` o etiquetas descriptivas en lenguaje natural (`Medida real`, `Medida en el plano`).
- **Diagramas y Elementos Visuales en Geometría (Eje 04):** En recursos de Geometría, las infografías vectoriales SVG DEBEN contener construcciones geométricas vectoriales exactas siguiendo el estándar de `docs/conocimiento/prompt-maestro-geometria-graficos.md`:
  1. *Uso Obligatorio de Matplotlib + $\LaTeX$:* Todo diagrama geométrico (triángulos, polígonos, rayos, ángulos, secantes, segmentos paralelos) DEBE generarse a través del motor de Matplotlib (`matplotlib.patches.Wedge`, `Polygon`, `FancyArrowPatch`) con `mathtext.fontset='cm'`. Queda **estrictamente prohibido construir arcos o polígonos con comandos SVG manuales arbitrarios** para evitar distorsiones y desbordes.
  2. *Tarjetas de Ejemplos con Gráficos Dedicados (`ejemplos.svg` — Zero-Empty-Cards):* Cada tarjeta conceptual ❶ y ❷ de `ejemplos.svg` DEBE contener obligatoriamente una construcción geométrica vectorial completa generada con Matplotlib (`plot_ejemplo1()`, `plot_ejemplo2()` incrustadas como data-URI), acompañada de desarrollo paso a paso en lenguaje natural y una insignia de resultado (`badge-ok`). Queda **estrictamente prohibido dejar tarjetas de ejemplos vacías o solo con texto**.
  3. *Insignias de Resultado Matemáticas Puras en `ejemplos.svg` (`badge-ok`):* Las insignias de resultado verde en `ejemplos.svg` deben renderizar **exclusivamente fórmulas o igualdades matemáticas en Computer Modern $\LaTeX$** (`$m' = 3$`, `$O \in L \implies H(L) = L$`). Queda **estrictamente prohibido embutir oraciones completas en español dentro del modo matemático de $\LaTeX$**, ya que destruye los espacios y la legibilidad.
  4. *Escalamiento Proporcional Automático (Zero-Overflow):* Toda inserción de fórmulas o figuras en SVG DEBE escalar proporcionalmente (`scale = min(1.0, W_max / w, H_max / h)`), limitando fórmulas en tarjetas de ejemplos a $W \le 260\text{px}$ y badges a $W \le 250\text{px}$.
  5. *Separación Total entre Cuadros de Texto y Geometría (Zero-Overlap):* En los gráficos generados con Matplotlib, la figura geométrica DEBE situarse en la mitad superior del canvas ($c_y \approx 1.30$, $r \approx 0.72$), reservando la franja inferior ($y \in [0.10, 0.35]$) para badges o cuadros de texto explicativos (`bbox=dict(...)`). Queda **estrictamente prohibido superponer cuadros de texto o badges encima de figuras geométricas, circunferencias, centros o radios**.
  6. *Estructura Estricta de Verdadero / Falso en YAML (`errores_frecuentes` y `afirmaciones_verdaderas`):* Los campos `errores_frecuentes` y `afirmaciones_verdaderas` en los archivos YAML DEBEN ser **listas de cadenas de texto (strings)** con afirmaciones directas en $LaTeX$. Queda **estrictamente prohibido estructurarlos como diccionarios (`- error: ..., correccion: ...`)**, ya que la vista del frontend inyecta el objeto directamente produciendo errores de renderizado en las tarjetas V/F.
  7. *Sintaxis de Fórmulas en YAML (Comillas Simples):* Toda cadena con fórmulas $\LaTeX$ que contenga barras invertidas (`\overline`, `\vec`, `\parallel`, `\prime`) DEBE delimitarse con **comillas simples** (`'...'`) en YAML para evitar errores de escape.

## 💸 Economía de tokens (seguir SIEMPRE)

El consumo de tokens es una prioridad. Reglas para no dispararlo:

1. **Nunca usar llamadas "de relleno"** (`echo q1`, `echo flush`, etc.) para forzar/ordenar
   la salida de otras herramientas. Si los resultados llegan desordenados, esperar; no
   spamear comandos vacíos. Cada llamada cuesta tokens.
2. **Búsquedas acotadas:** Grep/Glob con `path`, `glob` y `head_limit` reducidos; pedir
   contexto (`-C`) solo cuando hace falta. Evitar barridos de todo el repo.
3. **Leer antes de editar** el fragmento exacto para que el `Edit` no falle y no haya que
   re-leer y reintentar. No re-leer archivos ya leídos sin cambios.
4. **Avisar ANTES de operaciones caras** (suites largas, builds, lectura de archivos
   grandes, muchas capturas, agentes/subagentes) y proponer una alternativa más barata para
   que el usuario decida.
5. **Si una sola tarea empieza a inflarse** (muchos reintentos o llamadas), detenerse, avisar
   al usuario el gasto aproximado y barajar un enfoque más económico antes de continuar.
6. **Previsualizar visualmente con URL local** (levantar runserver y pasar el link) en vez de
   capturas, salvo que el usuario pida una imagen.
