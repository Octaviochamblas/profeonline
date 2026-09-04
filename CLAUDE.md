# Guía para Claude — ProfeOnline

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
   activa (Claude no recuerda sesiones anteriores). **No "leer todo".**
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
  `.venv\\Scripts\\python.exe`).
- **Regla de ejecución de tests (obligatoria, medida 2026-07-10):** la suite completa
  demora ~6 min (~630 tests); un módulo aislado demora segundos. Por eso:
  1. **Durante el desarrollo**, correr SOLO el módulo afectado
     (ej. `python manage.py test apps.learn` ≈ 2 s). NUNCA la suite completa por cada
     iteración o fix pequeño.
  2. **La suite completa se corre UNA sola vez, justo antes de pushear** (o se delega a CI,
     que la corre igual y bloquea el deploy si falla).
  3. **No borrar tests para "acelerar"**: los ~630 cubren funcionalidades vivas y son la
     única barrera pre-deploy.
  4. `--parallel` NO funciona en Windows local (falla con `cannot pickle 'traceback'`);
     no insistir con él.
- **Despliegue:** push a `main` → Railway despliega. El *Custom Start Command*
  (dashboard de Railway) corre `migrate && ensure_admin && ensure_site && gunicorn ... --timeout 120`.
  El *Pre-Deploy Command* (también dashboard, **no** hay archivo de config: el dashboard
  gana sobre `railway.json`/`nixpacks`) corre `import_knowledge_tree && load_node_content
  && load_exercise_bank && publish_knowledge_nodes` — idempotentes, sincronizan
  `docs/conocimiento/` con la BD en una fase aparte que no bloquea el puerto.
- **Subir contenido = solo YAML + SVG, SIN migración.** El *Pre-Deploy Command* (arriba)
  sincroniza `docs/conocimiento/` en cada deploy. **Prohibido** agregar migraciones
  `apps/content/migrations/0XXX_load_*` / `0XXX_sync_*`: son datos, no esquema, y cada
  una infla el build de la BD de test en CI para siempre. Las 96 históricas (`0052`–`0147`)
  quedaron colapsadas en `0052_squash_content_loads.py` (no-op con `replaces`). Un push
  que solo toca `docs/**` o `static/img/nodos/**` no dispara CI (`paths-ignore`).
- **Email:** API HTTP de Brevo (`BREVO_API_KEY`); Railway bloquea puertos SMTP.
- **Errores:** Sentry (`SENTRY_DSN`) — proyecto `python-django` en org `particular-lw`.
- **Login con Google:** allauth, credenciales en `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.
- **CSP:** con nonce por petición (`apps/core/middleware.py`).
- **Auditorías:** vigentes en `docs/auditorias/`; las antiguas en `docs/auditorias/_archivo-2026-05-30/`.
- **Ejemplos en recursos (12 secciones):** Todos los ejercicios de la sección `ejemplos`
  deben ser interactivos (Tipo A con `alternativas:` o Tipo B con `respuesta: "Sí"` / `"No"`).
  Está **estrictamente prohibido** redactar ejemplos de respuesta abierta o pasivos que
  caigan en el botón "Ver solución" (pauta en `docs/conocimiento/pauta-contenido.md`).
- **Al terminar debes poder (12 secciones):** Debe estar estructurado obligatoriamente con
  las dos etiquetas explícitas `QUÉ:` (acción o capacidad matemática) y `CÓMO:` (mecanismo o
  algoritmo técnico de resolución en $LaTeX$). Prohibido redactar párrafos de texto corrido
  sin estas etiquetas (pauta en `docs/conocimiento/pauta-contenido.md`).
- **Fórmulas y Matemáticas en YAML (KaTeX):** Toda expresión matemática, fracción o número decimal con barra periódica ($0,\overline{3}$, $2,45\overline{8}$) en enunciados, alternativas, explicaciones o títulos de `ejemplos` y `checkpoints` DEBE estar estrictamente delimitada con signos de dólar (`$...$` o `$$...$$`). Prohibido dejar comandos LaTeX como `\overline` en texto plano.
- **Signos de Moneda / Dinero en YAML (KaTeX):** Todo monto monetario con signo peso (ej: $\$500.000$) DEBE estar estrictamente delimitado dentro de un bloque LaTeX como `$\$500.000$` o `$\$500.000\text{ pesos}$`. Está **estrictamente prohibido escribir `\$500.000` o `$500.000` suelto en texto plano sin cerrar**, ya que Markdown consume la barra invertida (`\`) y el renderizador de KaTeX en el cliente toma el signo `$` como apertura de fórmula matemática, devorando todo el texto en español siguiente (eliminando espacios, volviendo cursivas las palabras y convirtiendo guiones bajos en subíndices).
- **Infografías y Diagramas SVG:** Todo SVG (`static/img/nodos/`) debe respetar el estándar
  *Zero-Overflow*: textos derechos anclados con `text-anchor="end"`, padding seguro $\ge 15\text{px}$,
  y control estricto de longitud de caracteres por caja contenedora y subcaja interna
  ($N_{\text{max}} \le \frac{W_{\text{box}} - 2 \times \text{padding}}{\text{font-size} \times 0.60}$).
  Prohibido desbordar los bordes de subcajas, cards o del canvas. En números periódicos en SVG, está
  **estrictamente prohibido usar caracteres combinados Unicode (`\u0304`)**; usar siempre
  `<tspan style="text-decoration: overline">...</tspan>` o un elemento vectorial `<line>` para cubrir
  la totalidad del período. En expresiones matemáticas dentro de SVGs, está **estrictamente prohibido
  usar notación plana de programador con guiones bajos o símbolos crudos** (`E_%`, `E_rel`, `v_real`,
  `x_def`, `d_k`, `10^-k`, `10^k`); usar siempre etiquetas tipográficas vectoriales
  `<tspan baseline-shift="sub" font-size="70%">...</tspan>` para subíndices y
  `<tspan baseline-shift="super" font-size="70%">...</tspan>` para superíndices.
- **Fracciones Matemáticas en Diagramas SVG:** Toda fracción, división o cociente algebraico o numérico
  en diagramas SVG (`static/img/nodos/`) DEBE representarse obligatoriamente en formato vertical apilado
  con numerador superior, línea horizontal vectorial de fracción (`<line>`) y denominador inferior, con
  los operadores matemáticos ($\cdot$, $=$, $+$, $-$) alineados al centro de la barra. Está **estrictamente
  prohibido** usar notación plana con barra inclinada (`a / b`, `1 / (√3 - 1)`, `6 / √3`, `(a·d + b·c) / 12`)
  en infografías o diagramas explicativos. En contenido YAML, usar siempre $\LaTeX$ vertical $\frac{a}{b}$ en `$...$`.

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

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
