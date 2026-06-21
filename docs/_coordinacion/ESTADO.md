# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| _libre_ | - | - | 🟢 sin lock |

<!-- Ejemplo: | 🔨 Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | 🔴 trabajando | -->

## En curso ahora

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
  por contenido/decisión del 🧑 — `1-por-iniciar/mejoras-conversion-contenido.md` (+ testimonios).
- **KaTeX** ⏸️ pendiente decisión del 🧑: ¿el contenido llevará fórmulas en notación?
- **C1/C2** ⚪ aceptados (no son bloqueo; reconsiderar al entrar datos reales).

## Handoffs abiertos (Ready para construir)

- 🔨 **PWA básica** — `backlog/2-arquitectura/pwa-progressive-web-app.md`. Ready para Codex (preflight)
  → Antigravity (rama `feat/pwa-basica`). Manifest + SW conservador + offline + iconos; sin tocar CSP.
- ✅ **Estudio de banco de preguntas — CERRADO 🟢 y ARCHIVADO (2026-06-18).** Construido y desplegado
  (PRs #62–#67): generación IA, config por recurso, edición y runtime. Tarjeta movida a
  `6-finalizados/estudio-banco-preguntas.md`. (F4 multimodal sigue bloqueada por storage externo —
  fuera de alcance por ahora.)

## Últimas entregas
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
