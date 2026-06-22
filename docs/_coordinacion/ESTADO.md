# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| — | — | — | 🟢 libre |

<!-- Ejemplo: | 🔨 Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | 🔴 trabajando | -->

## En curso ahora
- **Guías interactivas - Fase 5 - EN AUDITORÍA 🟡 (2026-06-22):**
  🧩 Codex construyó pools ocultos editoriales, ensamblado por cuotas y distribución 20/50/30,
  no-repetición, sesiones transaccionales con timer server-side, corrección idempotente y dominio
  estructurado 60/40 aislado del progreso legacy. **502 tests OK** (1 skip), pre-commit verde,
  sin migraciones. Tarjeta en `backlog/4-auditoria/`; cierre de seguridad reservado a 🏛️ Claude.
- **Guías interactivas - Fase 4 - CERRADA 🟢 (2026-06-22):**
  🧩 Codex construyó el parser seguro AST→SymPy; 🏛️ Claude auditó como IA distinta, encontró y
  corrigió **1 hallazgo Medium de DoS** (apilamiento de exponentes que evadía el tope por-exponente y
  explotaba en `cancel`: nuevo `MAX_TOTAL_DEGREE`/`_degree_upper_bound` que corta sobre el AST antes
  del paso caro, +1 test) y cerró. **494 tests OK** (1 skip local `SIGALRM`), sin migraciones,
  `check --deploy` exit 0. Squash-merge de PR **#82** a `main`. Tarjeta en `backlog/6-finalizados/`.
  **Nota a futuro:** el timeout depende de `SIGALRM`+main thread (ok con gunicorn `sync`); documentar
  si se migra a `gthread`/`gevent`. **Siguiente: Fase 5 (evaluaciones nivel/final).**
- **Guías interactivas - Fase 3 - APROBADA TÉCNICAMENTE 🟢 (2026-06-22):**
  🧩 Codex auditó y corrigió generación/publicación manual, aislamiento y revalidación del runtime,
  panel editorial, esquema real de la guía, CSP, borrado lógico y N+1. **469 tests OK**; tarjeta en
  `backlog/5-cierre/` para auditoría final y merge de 🏛️ Claude.
- **Pendientes de KaTeX cerrados — 🟢 (2026-06-22):**
  (#2 parser) `_loads_ai_json` endurece el parseo de Gemini/OpenAI/pipeline ante cercas markdown
  y prosa (sin reparar barras a ciegas); **validado EN VIVO** con Gemini real generando álgebra en
  `$...$` y parseando bien. 5 tests nuevos. Rama `fix/parser-json-latex` (PR pendiente).
  (#1 banco existente) **Decisión del 🧑: dejar las ~1.500 preguntas en prosa como están** —
  solo el contenido nuevo sale con notación; se conserva la revisión humana (v2). Regeneración por
  recurso queda disponible a pedido.
- **KaTeX — render de fórmulas matemáticas en TODO el sitio — CERRADO 🟢 (2026-06-21):**
  KaTeX 0.16.11 **self-host** (`static/vendor/katex/`, sin CDN, CSP intacta) + `katex-init.js`
  (nonce) que renderiza `document.body` al cargar y cada `htmx:afterSwap` → cubre preguntas,
  alternativas, explicaciones, recursos y el reproductor fullscreen. Delimitadores `$...$`/`$$...$$`
  (y `\(\)`/`\[\]`). **Generación IA conectada:** el prompt compartido (`_build_prompt`) ahora
  ordena LaTeX y reestructura los niveles pedagógicos (N1 conceptual / N2 procedimental / N3
  transferencia, con distractores por nivel) y refuerza el pipeline (documento canónico + auditor
  saben de LaTeX). **403 tests OK** + QA visual
  (potencia/fracción/raíz/integral/matriz). Tarjeta en `backlog/6-finalizados/`.
  **Pendiente aparte:** migrar/regenerar el banco existente y verificar el parser JSON ante el
  escape `\\` de la IA en la primera generación real.
- **Rediseño compacto de temas — CERRADO 🟢 (PR #77, 2026-06-21):**
  progreso global corregido, indicadores por nivel, cabecera/tarjetas móviles condensadas y
  limpieza v1 de títulos con migración `0032`. **398 tests OK** y QA 320/360/390 px.
  Tarjeta en `backlog/6-finalizados/`.
- **Pipeline único de publicación educativa — BACKEND MERGEADO 🟢 (PR #72, 2026-06-19):**
  transcripción como fuente → documento canónico, metadatos, guía y preguntas con segunda auditoría;
  publicación en dos fases. 🧩 Codex construyó; 🏛️ Claude auditó y corrigió (`SET_NULL` en guía
  canónica, +tests; **suite 348 OK**). **Agente Python excluido** (duplica el uploader Node
  `profeonline-uploader`): el flujo de subida se implementó como **agente Python local**
  (`scripts/process_upload_batch.py`, commit `79836ad`, 2026-06-21) — paso 2 ✅. Concurrencia
  (`select_for_update`) diferida. Tarjeta en `backlog/6-finalizados/`.
- **Limpieza física + auditoría global — CERRADA POR CODEX 🟢 (2026-06-19):**
  respaldo de 1.351 archivadas, borrado físico sin historial afectado y auditoría de las 2.476
  activas. Resultado: 0 archivadas, 0 duplicados textuales, 43 grupos estructurales para revisión,
  0 alternativas huérfanas y producción 200. Tarjeta en `backlog/5-cierre/`.
- **Diversidad del banco de racionales — APLICADA EN PRODUCCIÓN 🟢 (2026-06-19):**
  1.351 repeticiones archivadas, 55 representantes antiguas conservadas y 1.440 preguntas nuevas
  publicadas en 16 recursos. Verificación: 1.495 publicadas, 1.351 archivadas, 0 alternativas
  inválidas; respaldo JSON local de las 1.406 preguntas originales.
- **Rama consolidada `codex/admin-options-menu` — CERRADA 🟢 (2026-06-18):**
  menú staff, plantilla allauth, robustez IA, importador JSON y generador local aditivo auditados.
  Hallazgo P0 de migración destructiva corregido; 331 tests y barrera CI local verdes.
- **Analítica del banco — CERRADO 🟢 (2026-06-18):** cobertura, resultados, efectividad por pregunta
  y tasa ponderada filtrable por alumno o grupo ad hoc, agregada por tema/recurso/pregunta. 🧩 Codex
  construyó, 🏛️ Claude auditó (fix de GET inválido + 3 tests de regresión) y cerró. **PR #69
  squash-mergeado**; suite completa verde, sin migraciones. Tarjeta en `backlog/6-finalizados/`.
- **Guías desde Google Drive — PR #68 mergeado (2026-06-18):** importar guías desde una carpeta
  de Drive (service account, navegación de subcarpetas), selector jerárquico de vínculos, soporte `.docx`
  (`python-docx`) y **publicar preguntas de inmediato por defecto**. Validado e2e contra carpeta real;
  suite completa verde, sin migraciones. Tarjeta en `backlog/3-construccion/guias-desde-drive.md`.
  **Pendiente operativo:** el 🧑 carga `GOOGLE_SERVICE_ACCOUNT_JSON` + `GUIDES_DRIVE_FOLDER_ID`
  en Railway · publicar los borradores que ya están en prod (loops viejos).
- **Banco de preguntas con generación IA — CERRADO 🟢 y desplegado (2026-06-16):** 6 PRs (#62–#67).
  Generación grounded en transcript de YouTube + guías de estilo; **2 modos** (🎬 video / 📄 documento)
  con UI (página de guías + botones por recurso + selector en el estudio); comando `backfill_transcripts`;
  fix de seguridad de la API key + backoff 429. **289 tests.** Detalle en `reportes-sesion/2026-06-16.md`.
  **Pendiente operativo del 🧑:** poblar matemática escolar (loops desde el PC) y **rotar la contraseña
  del Postgres** (quedó expuesta en una captura).
- **M5 (Analítica) y Verificación de email CERRADAS 🟢 (2026-06-03):** mergeadas vía **PR #36** y **PR #38**
  (Antigravity construyó, Codex auditó, Claude cerró). Analítica interna + verificación obligatoria de email.
- **Sprint de producto:** **Home ✅ → a11y/pulido ✅ → pulido técnico ✅ → PWA (handoff Ready)**; KaTeX condicional.
  **6 PRs cerrados hoy 🟢:** #41 (rediseño Home), #42 (contraste AA), #43 (pulido móvil),
  #44/#45 (handoffs docs), **#46 (pulido técnico a11y/SEO).** Construyó Antigravity/Claude; Claude cerró.
- **PWA (handoff Ready):** plan de Antigravity + Plan v2 de Codex, **refinado y corregido por Claude**
  (theme teal `#0f766e`, precache solo offline+iconos, apple-touch PNG). En `backlog/2-arquitectura/`.
  **Pendiente:** preflight de Codex + construcción de Antigravity (`feat/pwa-basica`).
- **Matriz P0/clave:** C1 ⚪ aceptado · C2 ⚪ aceptado · C3 🟢 · A1 🟢 · **M5 🟢**.
- **Infra viva:** prod `www.profeonline.cl` 🟢 200 · staging `web-staging-production-0dfc.up.railway.app` 🟢 200.

## Bloqueos / esperando

- **QA a11y manual (teclado + NVDA)** 🔴 requiere al 🧑 en Windows — tarjeta en `1-por-iniciar/`.
- **Mejoras de conversión** (testimonios, FAQ, precios, "sobre mí", formulario, gancho) 🔴 bloqueadas
  by contenido/decisión del 🧑 — `1-por-iniciar/mejoras-conversion-contenido.md` (+ testimonios).
- **C1/C2** ⚪ aceptados (no son bloqueo; reconsiderar al entrar datos reales).

## Handoffs abiertos (Ready para construir)

- 🔨 **Guías interactivas — Fases 4–7** (epic `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`).
  Fases 1–3 ✅. Handoffs de arquitectura redactados en `2-arquitectura/`:
  **F4** parser respuesta directa en `3-construccion/` (🟢 Ready tras preflight,
  `seguridad:requiere-claude`),
  **F5** evaluaciones nivel/final (🟢 Ready tras preflight, en `3-construccion/`), **F6** PDF (🟡),
  **F7** migración legacy + gate + piloto (🟡). Construir **en orden**, una fase por rama, cada una con preflight de Codex.
- 🔨 **PWA básica** — `backlog/2-arquitectura/pwa-progressive-web-app.md`. Ready para Codex (preflight)
  → Antigravity (rama `feat/pwa-basica`). Manifest + SW conservador + offline + iconos; sin tocar CSP.
- ✅ **Estudio de banco de preguntas — CERRADO 🟢 y ARCHIVADO (2026-06-18).** Construido y desplegado
  (PRs #62–#67): generación IA, config por recurso, edición y runtime. Tarjeta movida a
  `6-finalizados/estudio-banco-preguntas.md`. (F4 multimodal sigue bloqueada por storage externo —
  fuera de alcance por ahora.)

## Últimas entregas
- 2026-06-22 — 🏛️ Claude: **Preflight Fase 5 RESUELTO 🟢 — Ready para construir.**
  Contrastado contra el código real. Hueco de alcance resuelto (decisión 🧑: **Fase 5 incluye la
  generación de los pools ocultos** — `visible_bank_service` hardcodea `banco_visible`). Contradicciones
  fijadas: `final_distribution` mapea a `level` (N1/N2/N3); timer (`expires_at = inicio + config`) ≠
  cota de duración (`sum(estimated_minutes)±%`), exigir `estimated_minutes>0`; intento en transacción
  + una sola sesión `en_curso`. Dominio por **último intento** (60/40, ≥80% y final ≥80%), función
  nueva sin tocar el `progress_service` legacy. Sin migraciones esperadas. Tarjeta en
  `backlog/3-construccion/`; construye 🔨 Antigravity (`feat/guias-fase5-evaluaciones`).
- 2026-06-22 — 🏛️ Claude: **Fase 4 AUDITADA Y CERRADA 🟢 — merge de PR #82 a `main`.**
  Auditor distinto al builder (Codex). Propiedad crítica intacta (sin `eval`/`exec`/`parse_expr`/
  `sympify(string)`; whitelist AST; inyección bien cubierta). Hallazgo Medium de DoS corregido por
  excepción (Claude builder, por decisión del 🧑): apilamiento de exponentes `(...**n)**m` evadía
  `MAX_EXPONENT_ABS` y explotaba en `cancel` (~296 MB + cuelgue confirmado); fix con
  `MAX_TOTAL_DEGREE=32` + `_degree_upper_bound` que corta sobre el AST antes del paso caro (<0,04 s).
  **494 tests OK**, sin migraciones, `check --deploy` exit 0. `audit:aprobado` aplicado.
- 2026-06-22 — 🧩 Codex: **Fase 4 CONSTRUIDA — PR #82 esperando auditor distinto 🟡.**
  Parser AST→SymPy seguro, respuestas numéricas/algebraicas, panel editorial y práctica mixta
  completados. **493 tests OK local y CI Linux completo verde** (incluido timeout `SIGALRM`);
  pip-audit, deploy-check, migraciones, Ruff y pre-commit verdes. El único check rojo es el gate
  organizativo que exige revisión de otra IA. Auto-merge deshabilitado; label
  `seguridad:requiere-claude` aplicado.
- 2026-06-22 — 🧩 Codex: **Preflight Fase 4 — LISTO PARA CONSTRUIR 🟢.**
  Se resolvieron las contradicciones del handoff: la práctica visible no persiste `text_answer`;
  parser AST→SymPy nodo a nodo sin `parse_expr`/`sympify(string)`; tolerancia absoluta; gramática,
  límites y timeout concretos; edición/publicación por tipo; práctica mixta y adaptación
  retrocompatible del reproductor. SymPy 1.14.0 queda como dependencia nueva. Tarjeta movida a
  `backlog/3-construccion/`.
- 2026-06-22 — 🏛️ Claude: **Fix dificultad acentuada — 🟢 mergeado a `main`** (`fix/dificultad-acentos`).
  Detectado en QA local: con API key real, la generación de guías de F2 fallaba la validación porque
  la IA devuelve dificultades **con acento** (`"básica"`) y el modelo usa claves **sin acento**
  (`basica/.../desafio`); además F1 perdía silenciosamente la dificultad a "intermedia". Se agregó
  `Question.normalize_difficulty()` y se canonizó en prompts/mocks/validación/plantilla
  (`item_extraction`, `learning_guide`, `visible_bank`, `item_review`, `_item_row.html`). +3 tests.
  **472 tests OK**, sin migración. Verificado en navegador (badge "Básica" correcto).
- 2026-06-22 — 🏛️ Claude + 🔨 Antigravity + 🧩 Codex: **Guías interactivas — Fases 2 y 3 CERRADAS 🟢
  y mergeadas a `main`** (squash-merge, F2+F3 juntas; F3 se construyó sobre F2 sin mergear).
  **F2** (guía ProfeOnline original + anti-copia): generación IA, motor de originalidad determinista
  (n-gramas de 10 palabras + blocklist + tope anti-DoS), publicación manual bloqueada con
  **revalidación en caliente por hash**, versionado con `archivada` y guía única pública por tema.
  Cierre legal de 🏛️ Claude (`seguridad:requiere-claude`) ✅. **F3** (banco visible + estudio):
  página pública de la guía (KaTeX, imprimible), banco agrupado por ítem/dificultad, práctica
  por ítem/mixta **sin peso académico**, panel editorial con cuotas/déficit/generación, y
  **aislamiento del banco legacy con `scope=""`**. Construyó Antigravity; Codex auditó/corrigió ambas;
  🏛️ Claude verificó en corrida limpia y cerró. **Barrera: 469 tests OK** + `check --deploy` 0 errores
  + sin migraciones pendientes. Migraciones aplicadas: `0034` (F1), `0035` (F2). Tarjetas en
  `backlog/6-finalizados/`. **Pendiente P3 (no bloqueante): QA visual móvil 320/360/390. Siguiente: F4.**
- 2026-06-22 — 🧩 Codex: **Guías interactivas — Fase 3 APROBADA TÉCNICAMENTE 🟢.**
  Se corrigieron publicación incompleta/automática, borrado físico, edición en caliente de preguntas
  publicadas, revalidación del submit, cruces entre temas, cuotas concurrentes, UI editorial ausente,
  render del esquema real de Fase 2, CSP y N+1. **469 tests OK** en 324,059 s; 13 tests específicos,
  104 regresiones afectadas, deploy-check, migraciones y pre-commit verdes. Tarjeta movida a
  `backlog/5-cierre/`; queda revisión final y merge por 🏛️ Claude.
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 3 (banco visible + experiencia de estudio) — LISTO PARA AUDITORÍA 🟡**
  (rama `feat/guias-fase3-banco-visible`). Se completó la implementación de la Fase 3 del epic. Aislamiento legacy (scope="") en selectors de disponibilidad, quiz y evaluación final. Servicio `visible_bank_service.py` con generación atómica por déficit (borrador + publicada) y selector round-robin mixto. Panel editorial HTMX en `item_extraction` (cuota editable inline y generación con indicador de carga). Revisión ampliada en `question_review` para `banco_visible` con sección editorial separada, sincronización de `canonical_answer` en alternativas y validación/envío/acciones masivas con rechazo estricto (HTTP 400). Detalle de guía público (/guias/<slug>/) para alumnos con logo, Katex y CSS de impresión. Práctica no académica fullscreen con guardado de sesión (filtros/orden/IDs) y calificación al vuelo libre de escrituras en BD. 10 tests de integración específicos y pre-commit hooks verdes. Tarjeta movida a `backlog/4-auditoria/`.
- 2026-06-22 — 🧩 Codex: **Preflight Fase 3 — LISTO PARA CONSTRUIR 🟢.**
  Handoff refinado contra el código real: servicio propio para generar preguntas
  `scope="banco_visible"` en borrador reutilizando candidatos IA, panel por ítem/recurso,
  aislamiento obligatorio `scope=""` del quiz legacy, práctica no académica sin `QuizAttempt`,
  query anti-N+1, integración tema/recurso, reproductor fullscreen, CSP, KaTeX y CSS print.
- 2026-06-22 — 🧩 Codex: **Guías interactivas — Fase 2 APROBADA TÉCNICAMENTE 🟢.**
  Auditoría con correcciones de versionado, autorización/bloqueo de fuentes, contrato JSON estricto,
  flujo HTMX, selección OpenAI/Gemini, hash canónico y concurrencia. **456 tests OK**, deploy-check,
  migraciones, pre-commit y diff-check verdes. Tarjeta movida a `backlog/5-cierre/`; queda auditoría
  legal final y merge por 🏛️ Claude (`seguridad:requiere-claude`).
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 2 (guía ProfeOnline original + originalidad) — LISTO PARA AUDITORÍA 🟡**
  (rama `feat/guias-fase2-guia-original`, `seguridad:requiere-claude`). Se completó la implementación
  de la Fase 2 del epic. Lógica aditiva con campos de originalidad en `LearningGuide` (migración `0035`),
  servicio de generación con IA (grounded en ítems aprobados del tema y fuentes privadas, anti-injection),
  motor de originalidad determinista sin truncamiento silencioso (n-gramas de 10 palabras y blocklist de
  marcas), control de concurrencia y revalidación en caliente mediante transacciones atómicas y
  bloqueos select_for_update (para Topic y guías ordenadas), restricción unique_active_published_guide_per_topic,
  panel HTMX CSP-safe (sin JS inline), y 17 tests unitarios focalizados. Barrera completa
  verificada (449 tests Django OK, check --deploy OK, makemigrations --check OK, pre-commit OK).
  Tarjeta movida a `backlog/4-auditoria/`.
- 2026-06-22 — 🏛️ Claude + 🔨 Antigravity + 🧩 Codex: **Guías interactivas — Fase 1 CERRADA 🟢**
  (squash-merge a `main`, commit `6ccf403`). Panel solo-admin `/publicar/items/`: la IA propone
  ítems de aprendizaje desde una guía privada (`QuizGuide`) calibrando dificultad al nivel educativo,
  y el profesor los edita/fusiona/aprueba/archiva. Todo **detrás del flag
  `Topic.structured_bank_enabled`** (banco legacy intacto). Antigravity construyó; Codex rechazó por
  5 P1 + 5 P2; ante la falta de correcciones del builder, 🏛️ Claude (por decisión del 🧑) corrigió
  **todos** los hallazgos (flag server-side, fusión mismo-tema, CSP→JS externo con nonce,
  `detected_exercise_count` con migración aditiva `0034`, validación de guía, N+1, dedupe IA, choices,
  `_sanitize_key`) y cerró. **432 tests OK** + barrera completa verde. Tarjeta en
  `backlog/6-finalizados/`. **Próximo: Fase 2 (guía ProfeOnline original + anti-copia,
  `seguridad:requiere-claude`).**
- 2026-06-22 — 🧩 Codex: **Fase 1 de guías interactivas — GATE RECHAZADO 🔴.**
  Suite completa **425 tests OK**, `check --deploy` sin errores, sin migraciones y pre-commit verde;
  pero quedaron P1: flag por tema no aplicado, fusión cruzada entre temas, JS inline bloqueado por
  CSP, `detected_exercise_count` descartado y guía no validada contra el tema. Tarjeta con hallazgos
  devuelta mediante `git mv` a `backlog/3-construccion/` para corrección por 🔨 Antigravity.
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 1 (extracción y aprobación de ítems) — LISTO PARA AUDITORÍA 🟡**
  (rama `feat/guias-fase1-extraccion-items`). Se implementó el servicio de extracción curricular IA `item_extraction_service.py` (calibra la dificultad por nivel pedagógico y soporta LaTeX) y el panel HTMX in-app `publicar/items/` (edición inline, aprobación/archivado, vinculación de recursos y fusión segura de ítems). Todo 100% aditivo y detrás del flag de tema. Suite completa con 425 tests OK (10 nuevos para esta fase). Tarjeta movida de `2-arquitectura/` a `4-auditoria/`.
- 2026-06-21 — 🏛️ Claude + 🧩 Codex + 🧑: **Rediseño de recurso + progreso académico — CERRADO 🟢**
  (rama `feat/recurso-progreso-academico`). Vista de recurso rediseñada (título primero, metadatos
  compactos, descripción con Ver más/menos, columna legible, sin barra "Comprendido") + bloque único
  "Practica y evalúa tu aprendizaje" con pestañas por nivel. **Progreso calculado desde intentos
  reales**: promedio de los últimos 3 por modo, ponderado 30/70, estados Preparado/Aprobado; motor
  `progress_service` + selectores sin N+1. Perfil ampliado con panel por tema/recurso. "Comprendido"
  retirado de la UI (endpoint+modelo conservados); agregados de tema usan progreso ponderado.
  🧩 Codex corrigió disponibilidad por modo, cobertura real del perfil y pestañas móviles.
  **Sin migraciones. 391 tests OK + QA 320/360/390 px. PR #75 squash-mergeado**
  en `main` (`3d847a6`, 2026-06-21). Tarjeta en `backlog/6-finalizados/`.
- 2026-06-21 — 🏛️ Claude + 🧑: **Reproductor de preguntas a pantalla completa — CERRADO 🟢** (commit
  `faacd8c`, merge a `main`). Panel interno fullscreen (móvil + PC): una pregunta a la vez con
  `Anterior`/`Siguiente`, pantalla de revisión respondida/pendiente previa al envío y resultados a
  pantalla completa con corrección. Aplica a Preparación, Evaluación por nivel y evaluación final del
  tema. Overlay global `#quiz-player-root` + `static/js/quiz-player.js` (CSP-safe), reusa las vistas
  HTMX; `quiz_submit` ordena resultados por orden de presentación. **Sin migraciones ni endpoints
  nuevos. Suite completa 370 OK** + QA visual (escritorio y móvil 360px). Tarjeta en
  `backlog/6-finalizados/`.
- 2026-06-21 — 🏛️ Claude + 🧑: **Agente local de subida `upload-batch/v1`** (commit `79836ad`).
  `scripts/process_upload_batch.py` sube cada video como no listado, obtiene la transcripción
  desde la IP local, registra el ítem en ProfeOnline y espera la validación antes de hacerlo
  público (revierte a no listado si la confirmación server-side falla). Cierra el **paso 2** del
  pipeline único de publicación: el cliente Node `profeonline-uploader` se reemplaza por este
  agente Python local. Incluye `cleanup_borradores` (limpia borradores residuales, dry-run por
  defecto, respeta ítems en vuelo) + tests del agente (4 OK). Sin migraciones.
- 2026-06-21 — 🧩 Codex + 🧑: **Taxonomía, cobertura y Lenguaje Algebraico actualizados en producción.**
  Asignaciones vigentes: Electromagnetismo → Física; Física Escolar → Física +
  Medio/Preuniversitario; Matemática Media/Preuniversitaria → Matemáticas. El resumen del banco usa
  Área→Nivel→Asignatura→Tema→Recurso y orden Escolar→Medio/Preuniversitario→Universitario.
  Lenguaje Algebraico quedó con 1.530 preguntas (90 en cada uno de 17 recursos), cobertura 17/17 y
  orden manual `1.x→2.x→3.x→4.01→4.01a→4.02→4.03→4.04`.
- 2026-06-20 — 🏛️ Claude + 🧑: **Nivel educativo por asignatura (rama `feat/nivel-por-asignatura`).**
  Nuevo campo `Subject.education_level` (migración 0031) que los temas/recursos sin nivel propio
  heredan vía `Resource.get_education_level()`; cableado en generación inline, estudio, pipeline y
  `generate_pending_questions`. Comando `set_subject_level --subject … --level … [--apply]` (dry-run
  por defecto). Aplicado en producción: **Física Escolar → Medio/Preuniversitario**. Tests
  focalizados verdes.
- 2026-06-20 — 🏛️ Claude + 🧑: **Rediseño de dos paneles del banco (rama `feat/rediseno-resumen-banco`).**
  (1) Resumen `/publicar/preguntas/resumen/` → acordeón
  Área→Nivel→Asignatura→Tema→Recurso con fracciones
  `auditados/total` por categoría editorial, preguntas por nivel y semáforo (verde/amarillo/rojo <20%).
  (2) `question_review` → config de evaluación full-width arriba + generador IA por nivel/modo con
  cantidad y descripción; Gemini ahora ve las preguntas existentes para no repetir; "copiando documento"
  deshabilitado. Sin migraciones. Tests focalizados verdes. Detalle en
  `reportes-sesion/2026-06-20-rediseno-paneles-banco.md`. QA visual y despliegue completados.
- 2026-06-18 — 🏛️ Claude: **Cierre de Fase 5 (auditoría final).** Auditados como no destructivos el
  generador local aditivo (`scratch/generate_math_questions.py`: sin `.delete()`, dedup por
  `existing_texts`) y el importador transaccional (`import_questions_json` dentro de `transaction.atomic`).
  Tarjeta **"Estudio de banco de preguntas"** archivada (`4-auditoria` → `6-finalizados`); `4-auditoria/`
  queda vacía (solo `.gitkeep`). Barrera re-verificada local: **331 tests OK**; `check --deploy` solo con
  warnings de dev-settings (sin errores).
- 2026-06-16 — 🏛️ Claude + 🧑 Usuario: **Banco de preguntas con generación IA CERRADO 🟢** (6 PRs:
  #62 banco+generación grounded, #63 fix key-leak + backoff 429, #64 transcript guardado en el recurso,
  #65 `backfill_transcripts`, #66 dos modos video/documento + UI de guías, #67 filtro `--subject`).
  289 tests. **Aprendizaje:** YouTube bloquea el scraping masivo de transcripts por IP → se bajan a
  cuentagotas desde el PC y se guardan. Detalle y pendientes en `reportes-sesion/2026-06-16.md`.
- 2026-06-05 — 🏛️🔨🧩 **"Estudio de publicación (Fase 1)" CERRADO 🟢.** Página staff (`/publicar/estudio/`) que
  arma una **orden de lote** (`profeonline.upload-batch/v1`): selecciona varios videos (solo por nombre, no sube
  contenido), Área/Asignatura/Tema/Módulo (con creación inline), playlist (enlace o crear nueva) e indicación libre;
  Codex sube a YouTube y publica tal cual. Codex auditó (P2/P3 menores), QA del 🧑 detectó un bug al crear tema inline
  (`resource_ordering_method`) que Claude corrigió + test. Mergeado a `main` (squash). Tarjeta en `6-finalizados/`.
  **Sin migraciones.** Pendiente aparte: fix del seed `Matemática` (singular) y la Fase 2 (cola/agente).
- 2026-06-04 — 🏛️ Claude + 🧑 Usuario: **"Estudio de publicación" SIMPLIFICADO (revisión pre-merge).** Tras la QA,
  Octavio pidió algo más simple: lote de videos (por nombre) + Área/Asignatura/Tema/Módulo + playlist + indicación
  libre; Codex hace título/descripción/miniatura/subida tal cual. Se quita copy/duplicados/miniatura/privacidad y se
  agrega selección múltiple de archivos. Tarjeta `4-auditoria` → `3-construccion` para recorte por 🔨 Antigravity.
  Contrato pasa a `upload-batch/v1`.
- 2026-06-04 — 🧩 Codex + 🏛️ Claude: **Preflight de "Estudio de publicación (Fase 1)" OK** (sin objeciones).
  3 refinamientos integrados al handoff: inline de asignatura setea `Subject.area`; inline de módulo setea
  `subject` (+topic/levels) y `module_slug` es solo organizativo; mantener firma de `build_resource_copy`
  (wrapper compatible, tolera `video_url` vacío). JSON server-side. **Listo para Antigravity.**
- 2026-06-04 — 🏛️ Claude: **Handoff "Estudio de publicación (Fase 1)" mergeado a `main` (PR #54).**
- 2026-06-04 — 🏛️ Claude + 🧑 Usuario: **Handoff "Estudio de publicación (Fase 1)" Ready.** Idea creada y
  avanzada `1-por-iniciar` → `2-arquitectura`. Planificación 🧑+🤖 refinada por 🧩 Codex (8 acotaciones
  integradas) y verificada contra el código (URL real `/api/recursos/crear-video/`, webhook sin
  `area_slug`/`module_slug`, `Level` M2M). Acotado a la web que genera el JSON; Fase 2 (cola/agente) aparte.
- 2026-06-03 — 🏛️🔨 **Pulido técnico a11y/SEO CERRADO 🟢 (PR #46).** Antigravity construyó (focus-trap
  drawer, skip-link, reduced-motion, JSON-LD Person/LocalBusiness, tokens); Claude auditó (2ª IA) y
  corrigió una regresión (`--secondary-hover` borrado del `:root`). Tarjeta en `6-finalizados/`.
- 2026-06-03 — 🏛️🧩🔨 **Handoff PWA refinado y Ready.** Claude fusionó el plan de Antigravity + Plan v2
  de Codex y corrigió 4 supuestos contra el código (color teal, apple-touch PNG, precache sin hashing,
  start_url no medible). Decisiones 🧑: theme `#0f766e`, QA iOS opcional. Tarjeta en `2-arquitectura/`.
- 2026-06-03 — 🏛️🔨 **a11y + pulido móvil CERRADOS 🟢 (PR #42, #43).** Contraste AA de WhatsApp,
  drawer móvil lateral, WhatsApp flotante, contacto (Concepción, sin mail), detalle de recurso reordenado.
- 2026-06-03 — 🏛️🔨 **Rediseño del Home CERRADO 🟢.** Antigravity construyó (Hero reenfocado, perfil
  real de Octavio Chamblas, "Cómo funciona" 2 pasos, destacados condensados); Claude auditó como 2ª IA
  y corrigió (bug CSS `:active`, CSS muerto de testimonios, imagen huérfana). Barrera verde. Prueba
  social diferida por falta de testimonios reales (tarjeta nueva).
- 2026-06-03 — 🏛️ Claude + 🧑 Usuario: **Handoff de Home redactado y Ready.** Decisiones: placeholders
  + contenido hardcodeado (sin modelos/admin). Tarjeta movida `1-por-iniciar` → `2-arquitectura`.
- 2026-06-03 — 🏛️🔨🧩 **Verificación de email mergeada y CERRADA 🟢 (PR #38).** Antigravity construyó,
  Codex auditó (P1 duplicados, P2 anti-enumeración, P3 usuarios sin email), Antigravity corrigió, Claude
  cerró (sensible). 202 tests. `mandatory` + Google exento; migración no bloquea a usuarios actuales.
- 2026-06-03 — 🏛️🔨🧩 **M5 Analítica interna mergeada y CERRADA 🟢 (PR #36).** Antigravity construyó,
  Codex auditó y curó privacidad, Claude cerró como 3ª IA (superficie sensible). Suite 191 tests. Matriz M5 → 🟢.
- 2026-06-02 — 🧩 Codex: **cura privacidad M5 en PR #36** — metadata por allowlist de evento,
  `path` sin querystrings, JS sin `href`/texto/`file_url` sensible y regresiones de analitica. Lock liberado.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **rumbo post-P0 definido.** C1/C2 **aceptados** como riesgo;
  sprint de valor visible (Analytics → Home → QA a11y). Handoff de **Analytics interno** redactado en `2-arquitectura`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **rotación de credenciales de prod** (la URL quedó expuesta en
  chat). Causó un 500 breve (web cacheaba la `DATABASE_URL` vieja); recuperado con redeploy. Staging
  se desincronizó por error y se revirtió. Procedimiento + lecciones en `runbook-backups.md §5`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **A1 → 🟢 staging operativo** en Railway (`Web-staging` +
  `Postgres-Staging` aislada, 200 en `/` y `/admin/`). 2 hallazgos resueltos (`DJANGO_USE_X_FORWARDED_PROTO`,
  `collectstatic`/Custom Start Command) → `runbook-staging.md §8`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **C2 → backup real de prod + restore drill verificados**
  (`pg_dump` 18.4; runbook §4.B). Riesgo 🟡 (falta automatizar).
- 2026-06-02 — 🔨 Antigravity + 🏛️ Claude: **Router mergeado (PR #29)** — workflow mecánico de
  ruteo/labels (sin `contents: write`, sin secretos, no mergea). Revisado por Claude (`seguridad:requiere-claude`).
- 2026-06-02 — 🔨 Antigravity + 🏛️ Claude: **A1 mergeado (PR #30)** — `check_environment` + runbook
  staging. Riesgo A1 queda 🟡 hasta que el 🧑 Usuario cree el servicio staging + DB propia en Railway.
- 2026-06-02 — 🔨 Antigravity + 🏛️ Claude: **C2 mergeado (PR #28)** — `backup_db`/`restore_db` con
  guardas anti-prod + runbook. Riesgo C2 queda 🟡 hasta backups automáticos del proveedor.
- 2026-06-02 — 🔨 Antigravity + 🏛️ Claude: **C1b mergeado (PR #27)** — `seed_content` idempotente.
- 2026-06-02 — 🏛️ Claude: **C3 cerrado en 🟢** — código en `main` (PR #26) + `REDIS_URL` en Railway (PR #31).
- 2026-06-02 — 🏛️🔨🧩 **C1 mergeado (PR #24)** por el flujo completo: Antigravity construyó,
  Codex auditó (detectó fuera-de-alcance + `build.sh` + docs), Claude cerró. Lock liberado.
- 2026-06-02 — 🏛️ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 — 🏛️ Claude: automatización del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 — 🏛️ Claude: reestructuración de la documentación (PR #19).
