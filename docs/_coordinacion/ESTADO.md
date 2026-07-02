# ðŸŸ¢ ESTADO VIVO â€” CoordinaciÃ³n de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al dÃ­a.
> ðŸ”’ Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
<!-- Ejemplo: | ðŸ”¨ Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | ðŸ”´ trabajando | -->

## En curso ahora
- **Editor manual desde cada recurso — CONSTRUIDO (2026-07-01, rama `codex/editor-manual-recursos`):**
  Modal inline accesible para editar todo `NodeContent`, con listas visuales reordenables, CSRF, validación,
  control de concurrencia y protección de importaciones mediante `manual_override` + `--force-manual`.
  36 tests focalizados, `check --deploy`, migraciones y QA real escritorio/móvil, OK. La suite global excedió
  dos veces el límite local (2 y 5 min) sin emitir fallos; queda para CI/auditoría.
- **Auditoría de `explicacion` (formal+didáctico) MAT.ALG B0301–B0309 — COMPLETA 🟢 (2026-07-01, rama `content/mat-alg-b0309`):**
  Auditados los 365 recursos de los 9 bloques verificando "Definición formal" + "Desarrollo didáctico". Corregidos
  215 recursos con viñeta duplicada al final de `procedimiento` (artefacto de generación), 2 recursos de B0309 con
  `explicacion` corrompida (`repr()` de Python serializado en vez de texto), y 3 con la definición formal rota
  (fragmentos sueltos). Re-auditoría: 0 defectos restantes. `load_node_content` (840 actualizados), `check` OK,
  HTTP 200 en los 5 casos más afectados y **suite completa 501 tests OK (1 skip), sin regresiones**.
  **Hallazgo aparte sin corregir:** 6 YAML huérfanos `mat-alg-operaciones-fracciones-*.yaml` sin nodo en BD
  (`semantic_id no encontrado`) — pendiente de investigar si son duplicados o recursos por crear.
- **Auditoría y reconstrucción MAT.ALG B0301–B0308 — COMPLETA 🟢 (2026-07-01, rama `codex/refine-mat-alg-b0301-b0308`):**
  Se recuperaron 115 YAML truncados, se redactaron 17 recursos ausentes y se normalizaron los 300 recursos
  con definiciÃ³n formal antes del desarrollo didÃ¡ctico, 2 ejemplos abiertos, 2 SÃ­/No y 5 V/F. Se eliminaron
  placeholders y duplicados exactos. Los 350 ejercicios placeholder de B0308 tandas 3â€“7 fueron reemplazados
  conservando sus `stable_id`. Base local: 300/300 contenidos; 35/35 recursos reconstruidos con 10 ejercicios.
  `check`, 47 tests focalizados y QA en navegador de una ficha por bloque, OK.
- **PoblaciÃ³n MAT.GEO B0401 â€” ÃNGULOS CONSTRUIDO ðŸŸ¡ (2026-06-30, rama `content/mat-num-b0205`):**
  Bloque `04.01` completado con `53/53` recursos y `530` ejercicios publicados (`10` por recurso).
  Se generaron `53` YAML + `11` JSONL con contenido contextualizado por recurso; auditorÃ­a local:
  `53` objetivos Ãºnicos, `51` introducciones Ãºnicas, `53` resÃºmenes Ãºnicos y `530` prompts Ãºnicos.
  `load_node_content` y `load_exercise_bank` OK, `python manage.py check` OK, sin migraciones nuevas,
  `git diff --check` OK y 28 tests focalizados (`test_knowledge_f2` + `test_node_bank`) en verde.
  La tarjeta `poblar-contenido-mat-geo.md` se mantiene en `2-arquitectura/` porque el handoff completo
  aÃºn incluye `B0402â€“B0413`.
- **PoblaciÃ³n MAT.NUM B0203+B0204 â€” CONTENIDO ORGÃNICO ðŸŸ¡ (2026-06-29, rama `content/mat-num-b0203`):**
  B0203 revisado otra vez: objetivos, ejemplos y V/F ahora usan el caso y el control matemÃ¡tico propio
  de cada recurso. B0204 construido completo: `93/93` contenidos + `930` ejercicios. AuditorÃ­a conjunta:
  `167` objetivos, `501` pasos, `668` tÃ­tulos de ejemplos/VF y `1.670` prompts Ãºnicos; importadores sin
  invÃ¡lidos, cobertura 10 ejercicios por recurso, `check` y 28 tests focalizados OK.
  Se mantuvo la tarjeta
  `poblar-contenido-mat-num-b0203-b0206.md` en `2-arquitectura/` porque el scope original del
  handoff incluye tambiÃ©n `B0205â€“B0206`.
- **PoblaciÃ³n MAT.FUND â€” CONSTRUIDA ðŸŸ¡ (2026-06-28, rama `content/mat-fund`):**
  106/106 recursos con `NodeContent`, 106 recursos con al menos 10 ejercicios cada uno,
  `load_node_content` OK, `load_exercise_bank` OK (`invÃ¡lidos: 0`), `check` OK y
  `python manage.py test` OK (587 tests, 1 skip). Tarjeta movida a `backlog/4-auditoria/`.
- **PoblaciÃ³n MAT.NUM B0201/B0202 â€” CERRADA ðŸŸ¢ (2026-06-28, squash-merge main `4b99118`):**
  56 recursos con contenido publicado (21 B0201 + 35 B0202). 610 ejercicios en banco.
  Claude coordinÃ³ cierre: corrigiÃ³ 4 P1 Codex (LaTeX, errores_frecuentes, Tipo B, estado).
  Tarjeta en `backlog/6-finalizados/`. 5 handoffs de ejes pendientes en `2-arquitectura/`.
  **Pendiente operativo:** ejecutar `load_node_content` + `load_exercise_bank` en producciÃ³n.
- **Plataforma de Conocimiento â€” ENTEROS_CONJUNTO + UI + pauta de contenido ðŸŸ¢ (2026-06-28):**
  Todo el contenido ENTEROS_CONJUNTO desplegado en `main`. Campo `introduccion` aÃ±adido al modelo
  (migraciÃ³n `0042`) + 15 introducciones didÃ¡cticas (nivel ~10 aÃ±os) cargadas en los YAMLs.
  SecciÃ³n renombrada "Ejemplos Verdadero/Falso" con accordeÃ³n nativo. Pauta de contenido
  en `docs/conocimiento/pauta-contenido.md`. Los 15 resÃºmenes quedaron versionados en los YAML
  para evitar que `load_node_content` los borre al recargar.
  **Pendiente operativo:** tras desplegar el cambio, ejecutar `python manage.py load_node_content`
  en producciÃ³n (el arranque de Railway no carga contenido automÃ¡ticamente).
- **Plataforma de Conocimiento â€” F1â€“F3 + F6 CERRADAS ðŸŸ¢ (2026-06-27, PR #102):**
  Squash-merge de `feat/grafo-conocimiento-f1` a `main`. Incluye: `KnowledgeNode`/`NodePrerequisite`,
  `NodeContent`/`NodeMedia`, app `learn`, `ItemGroup`/`NodeExercise` (**autopublicado inmediato** â€”
  `load_exercise_bank` siempre publica; flags `legal_review`/`rewrite_required` son metadata no
  bloqueante), UI rediseÃ±ada (`node_detail.html`: breadcrumb plegable, objetivo card, ejemplos
  interactivos V/F/SÃ­-No, errores como preguntas conceptuales, banco con tarjetas), ejercicios de
  clasificaciÃ³n (formato `matching`), filtro `to_json`. Contenido piloto: 14 NodeContent + ejercicios
  para ENTEROS_CONJUNTO. Tarjetas en `6-finalizados/`.
- **Plataforma de Conocimiento â€” F6 (prerrequisitos, subconjunto estructural) CONSTRUIDO ðŸŸ¡ (2026-06-27):**
  Parte que **no depende del estado del alumno** (F5 diferida): comando `load_prerequisites`
  (YAMLâ†’`NodePrerequisite`, **valida aciclicidad** con `graphlib`, aborta sin escribir si hay ciclo,
  idempotente) + secciÃ³n **"Antes de empezar"** informativa en la pÃ¡gina del nodo (enlaces a
  prerrequisitos publicados, nunca bloquea) + DAG piloto `num-enteros.yaml` (operatoriaâ†conjunto,
  verificado en navegador) + timestamps en `NodeContent` (migraciÃ³n `0040`). 13 tests nuevos.
  **Diferido a F5:** estado por alumno (âœ“/!) y "siguiente recomendado". Tarjeta F6 en `4-auditoria/`.
  **Siguiente: poblar banco/contenido (pipeline) Â· F4â€“F5 (mediciÃ³n) cuando se decida.**
- **Plataforma de Conocimiento â€” F1 y F2 CONSTRUIDOS ðŸŸ¡ (2026-06-26):**
  ðŸ›ï¸ Claude diseÃ±Ã³ arquitectura 6 capas + tarjetas F1â€“F6. **F1** (rama `feat/grafo-conocimiento-f1`):
  `KnowledgeNode`/`NodePrerequisite`, `import_knowledge_tree` idempotente (2208 nodos), migraciÃ³n
  `0037`, 8 tests. **F2 construido en la misma rama:** `NodeContent` (O2O con hoja,
  objetivo/explicaciÃ³n/procedimiento/ejemplos) + `NodeMedia` (video_youtube/file/external,
  video_kind), migraciÃ³n `0038`, app `apps/learn/` con 6 rutas jerÃ¡rquicas
  `/aprender/<asig>/<eje>/<bloque>/<tema>/<recurso>/`, 3 templates (home/list/detail), KaTeX hereda
  de `base.html`, comando `load_node_content` idempotente, admin inlines. YAML ejemplo:
  `docs/conocimiento/contenido/mat-num-enteros-conjunto-naturales.yaml`. **554/554 tests verde.**
  Tarjetas F1 y F2 en `4-auditoria/`. **F3 construido (2026-06-27).**
- **GuÃ­as interactivas - Fase 7 (gate + piloto) - EN AUDITORÃA ðŸŸ¡ (2026-06-23):**
  ðŸ›ï¸ Claude hizo preflight + construcciÃ³n (rama `feat/guias-fase7-gate-piloto`). DecisiÃ³n del ðŸ§‘:
  **coexistencia** (no se retira/clasifica el legacy). Nuevo `Topic.structured_bank_staging`
  (migraciÃ³n aditiva `0036`) + propiedad `structured_bank_editable` para preparar el tema con el flag
  apagado; guards admin â†’ `editable`, vistas de alumno siguen en `enabled`. Gate solo-lectura
  (`activation_gate_service`) que reusa los ensambladores reales; activaciÃ³n admin que **solo enciende
  el flag si el gate pasa**; rollback = apagar. 9 tests F7. `check --deploy` exit 0,
  `makemigrations --check` sin cambios. **Gate exige auditorÃ­a de IA distinta al builder (ðŸ§© Codex)**;
  `seguridad:requiere-claude`, auto-merge off. Es la **Ãºltima fase** del Ã©pico.
- **GuÃ­as interactivas - Fase 6 (PDF) - CERRADA ðŸŸ¢ (2026-06-23):**
  ðŸ§© Codex reconstruyÃ³ la impresiÃ³n nativa contra el markup real: portada A4, tema claro, KaTeX negro,
  saltos de pÃ¡gina y solucionario final consolidado. BotÃ³n "Descargar PDF", **sin JS ni librerÃ­as
  nuevas** (CSP intacta). ðŸ›ï¸ Claude auditÃ³ como IA distinta: verificÃ³ la decisiÃ³n de print nativo, el
  fix de especificidad (`!important` vence color inline), portada con a11y correcta y solucionario
  Ãºnico â€” **sin errores**. **CI Linux verde (511 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#84** a `main` (`22d3d7d`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 7 (migraciÃ³n
  legacy + gate + piloto) â€” Ãºltima del Ã©pico.**
- **GuÃ­as interactivas - Fase 5 - CERRADA ðŸŸ¢ (2026-06-23):**
  ðŸ§© Codex construyÃ³ pools ocultos editoriales, ensamblado por cuotas + distribuciÃ³n 20/50/30,
  no-repeticiÃ³n, sesiones transaccionales con timer server-side, correcciÃ³n idempotente y dominio
  estructurado 60/40 aislado del progreso legacy (9 hallazgos propios corregidos). ðŸ›ï¸ Claude auditÃ³
  como IA distinta: verificÃ³ timers server-side, intentos transaccionales por-recurso, aislamiento por
  scope+flag, reuso del parser de Fase 4, protecciÃ³n de historial (409) y gating de cobertura â€” **sin
  errores que corregir**. **CI Linux verde (510 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#83** a `main` (`5063113`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 6 (PDF).**
- **GuÃ­as interactivas - Fase 4 - CERRADA ðŸŸ¢ (2026-06-22):**
  ðŸ§© Codex construyÃ³ el parser seguro ASTâ†’SymPy; ðŸ›ï¸ Claude auditÃ³ como IA distinta, encontrÃ³ y
  corrigiÃ³ **1 hallazgo Medium de DoS** (apilamiento de exponentes que evadÃ­a el tope por-exponente y
  explotaba en `cancel`: nuevo `MAX_TOTAL_DEGREE`/`_degree_upper_bound` que corta sobre el AST antes
  del paso caro, +1 test) y cerrÃ³. **494 tests OK** (1 skip local `SIGALRM`), sin migraciones,
  `check --deploy` exit 0. Squash-merge de PR **#82** a `main`. Tarjeta en `backlog/6-finalizados/`.
  **Nota a futuro:** el timeout depende de `SIGALRM`+main thread (ok con gunicorn `sync`); documentar
  si se migra a `gthread`/`gevent`. **Siguiente: Fase 5 (evaluaciones nivel/final).**
- **GuÃ­as interactivas - Fase 3 - APROBADA TÃ‰CNICAMENTE ðŸŸ¢ (2026-06-22):**
  ðŸ§© Codex auditÃ³ y corrigiÃ³ generaciÃ³n/publicaciÃ³n manual, aislamiento y revalidaciÃ³n del runtime,
  panel editorial, esquema real de la guÃ­a, CSP, borrado lÃ³gico y N+1. **469 tests OK**; tarjeta en
  `backlog/5-cierre/` para auditorÃ­a final y merge de ðŸ›ï¸ Claude.
- **Pendientes de KaTeX cerrados â€” ðŸŸ¢ (2026-06-22):**
  (#2 parser) `_loads_ai_json` endurece el parseo de Gemini/OpenAI/pipeline ante cercas markdown
  y prosa (sin reparar barras a ciegas); **validado EN VIVO** con Gemini real generando Ã¡lgebra en
  `$...$` y parseando bien. 5 tests nuevos. Rama `fix/parser-json-latex` (PR pendiente).
  (#1 banco existente) **DecisiÃ³n del ðŸ§‘: dejar las ~1.500 preguntas en prosa como estÃ¡n** â€”
  solo el contenido nuevo sale con notaciÃ³n; se conserva la revisiÃ³n humana (v2). RegeneraciÃ³n por
  recurso queda disponible a pedido.
- **KaTeX â€” render de fÃ³rmulas matemÃ¡ticas en TODO el sitio â€” CERRADO ðŸŸ¢ (2026-06-21):**
  KaTeX 0.16.11 **self-host** (`static/vendor/katex/`, sin CDN, CSP intacta) + `katex-init.js`
  (nonce) que renderiza `document.body` al cargar y cada `htmx:afterSwap` â†’ cubre preguntas,
  alternativas, explicaciones, recursos y el reproductor fullscreen. Delimitadores `$...$`/`$$...$$`
  (y `\(\)`/`\[\]`). **GeneraciÃ³n IA conectada:** el prompt compartido (`_build_prompt`) ahora
  ordena LaTeX y reestructura los niveles pedagÃ³gicos (N1 conceptual / N2 procedimental / N3
  transferencia, con distractores por nivel) y refuerza el pipeline (documento canÃ³nico + auditor
  saben de LaTeX). **403 tests OK** + QA visual
  (potencia/fracciÃ³n/raÃ­z/integral/matriz). Tarjeta en `backlog/6-finalizados/`.
  **Pendiente aparte:** migrar/regenerar el banco existente y verificar el parser JSON ante el
  escape `\\` de la IA en la primera generaciÃ³n real.
- **RediseÃ±o compacto de temas â€” CERRADO ðŸŸ¢ (PR #77, 2026-06-21):**
  progreso global corregido, indicadores por nivel, cabecera/tarjetas mÃ³viles condensadas y
  limpieza v1 de tÃ­tulos con migraciÃ³n `0032`. **398 tests OK** y QA 320/360/390 px.
  Tarjeta en `backlog/6-finalizados/`.
- **Pipeline Ãºnico de publicaciÃ³n educativa â€” BACKEND MERGEADO ðŸŸ¢ (PR #72, 2026-06-19):**
  transcripciÃ³n como fuente â†’ documento canÃ³nico, metadatos, guÃ­a y preguntas con segunda auditorÃ­a;
  publicaciÃ³n en dos fases. ðŸ§© Codex construyÃ³; ðŸ›ï¸ Claude auditÃ³ y corrigiÃ³ (`SET_NULL` en guÃ­a
  canÃ³nica, +tests; **suite 348 OK**). **Agente Python excluido** (duplica el uploader Node
  `profeonline-uploader`): el flujo de subida se implementÃ³ como **agente Python local**
  (`scripts/process_upload_batch.py`, commit `79836ad`, 2026-06-21) â€” paso 2 âœ…. Concurrencia
  (`select_for_update`) diferida. Tarjeta en `backlog/6-finalizados/`.
- **Limpieza fÃ­sica + auditorÃ­a global â€” CERRADA POR CODEX ðŸŸ¢ (2026-06-19):**
  respaldo de 1.351 archivadas, borrado fÃ­sico sin historial afectado y auditorÃ­a de las 2.476
  activas. Resultado: 0 archivadas, 0 duplicados textuales, 43 grupos estructurales para revisiÃ³n,
  0 alternativas huÃ©rfanas y producciÃ³n 200. Tarjeta en `backlog/5-cierre/`.
- **Diversidad del banco de racionales â€” APLICADA EN PRODUCCIÃ“N ðŸŸ¢ (2026-06-19):**
  1.351 repeticiones archivadas, 55 representantes antiguas conservadas y 1.440 preguntas nuevas
  publicadas en 16 recursos. VerificaciÃ³n: 1.495 publicadas, 1.351 archivadas, 0 alternativas
  invÃ¡lidas; respaldo JSON local de las 1.406 preguntas originales.
- **Rama consolidada `codex/admin-options-menu` â€” CERRADA ðŸŸ¢ (2026-06-18):**
  menÃº staff, plantilla allauth, robustez IA, importador JSON y generador local aditivo auditados.
  Hallazgo P0 de migraciÃ³n destructiva corregido; 331 tests y barrera CI local verdes.
- **AnalÃ­tica del banco â€” CERRADO ðŸŸ¢ (2026-06-18):** cobertura, resultados, efectividad por pregunta
  y tasa ponderada filtrable por alumno o grupo ad hoc, agregada por tema/recurso/pregunta. ðŸ§© Codex
  construyÃ³, ðŸ›ï¸ Claude auditÃ³ (fix de GET invÃ¡lido + 3 tests de regresiÃ³n) y cerrÃ³. **PR #69
  squash-mergeado**; suite completa verde, sin migraciones. Tarjeta en `backlog/6-finalizados/`.
- **GuÃ­as desde Google Drive â€” PR #68 mergeado (2026-06-18):** importar guÃ­as desde una carpeta
  de Drive (service account, navegaciÃ³n de subcarpetas), selector jerÃ¡rquico de vÃ­nculos, soporte `.docx`
  (`python-docx`) y **publicar preguntas de inmediato por defecto**. Validado e2e contra carpeta real;
  suite completa verde, sin migraciones. Tarjeta en `backlog/3-construccion/guias-desde-drive.md`.
  **Pendiente operativo:** el ðŸ§‘ carga `GOOGLE_SERVICE_ACCOUNT_JSON` + `GUIDES_DRIVE_FOLDER_ID`
  en Railway Â· publicar los borradores que ya estÃ¡n en prod (loops viejos).
- **Banco de preguntas con generaciÃ³n IA â€” CERRADO ðŸŸ¢ y desplegado (2026-06-16):** 6 PRs (#62â€“#67).
  GeneraciÃ³n grounded en transcript de YouTube + guÃ­as de estilo; **2 modos** (ðŸŽ¬ video / ðŸ“„ documento)
  con UI (pÃ¡gina de guÃ­as + botones por recurso + selector en el estudio); comando `backfill_transcripts`;
  fix de seguridad de la API key + backoff 429. **289 tests.** Detalle en `reportes-sesion/2026-06-16.md`.
  **Pendiente operativo del ðŸ§‘:** poblar matemÃ¡tica escolar (loops desde el PC) y **rotar la contraseÃ±a
  del Postgres** (quedÃ³ expuesta en una captura).
- **M5 (AnalÃ­tica) y VerificaciÃ³n de email CERRADAS ðŸŸ¢ (2026-06-03):** mergeadas vÃ­a **PR #36** y **PR #38**
  (Antigravity construyÃ³, Codex auditÃ³, Claude cerrÃ³). AnalÃ­tica interna + verificaciÃ³n obligatoria de email.
- **Sprint de producto:** **Home âœ… â†’ a11y/pulido âœ… â†’ pulido tÃ©cnico âœ… â†’ PWA (handoff Ready)**; KaTeX condicional.
  **6 PRs cerrados hoy ðŸŸ¢:** #41 (rediseÃ±o Home), #42 (contraste AA), #43 (pulido mÃ³vil),
  #44/#45 (handoffs docs), **#46 (pulido tÃ©cnico a11y/SEO).** ConstruyÃ³ Antigravity/Claude; Claude cerrÃ³.
- **PWA (handoff Ready):** plan de Antigravity + Plan v2 de Codex, **refinado y corregido por Claude**
  (theme teal `#0f766e`, precache solo offline+iconos, apple-touch PNG). En `backlog/2-arquitectura/`.
  **Pendiente:** preflight de Codex + construcciÃ³n de Antigravity (`feat/pwa-basica`).
- **Matriz P0/clave:** C1 âšª aceptado Â· C2 âšª aceptado Â· C3 ðŸŸ¢ Â· A1 ðŸŸ¢ Â· **M5 ðŸŸ¢**.
- **Infra viva:** prod `www.profeonline.cl` ðŸŸ¢ 200 Â· staging `web-staging-production-0dfc.up.railway.app` ðŸŸ¢ 200.

## Bloqueos / esperando

- **QA a11y manual (teclado + NVDA)** ðŸ”´ requiere al ðŸ§‘ en Windows â€” tarjeta en `1-por-iniciar/`.
- **Mejoras de conversiÃ³n** (testimonios, FAQ, precios, "sobre mÃ­", formulario, gancho) ðŸ”´ bloqueadas
  by contenido/decisiÃ³n del ðŸ§‘ â€” `1-por-iniciar/mejoras-conversion-contenido.md` (+ testimonios).
- **C1/C2** âšª aceptados (no son bloqueo; reconsiderar al entrar datos reales).

## Handoffs abiertos (Ready para construir)

- ðŸ”¨ **Plataforma de Conocimiento â€” Fases F4â€“F5 (mediciÃ³n, diferidas por D4)** (handoffs en
  `2-arquitectura/kb-f4â€¦kb-f5`). F1, F2, **F3 y F6 (estructural) construidos** (rama
  `feat/grafo-conocimiento-f1`). Quedan, como migraciones **aditivas** cuando se decida medir:
  **F4** evaluaciÃ³n formal (reusa `answer_grading_service`/`evaluation_assembly_service` + generadores
  de D3 para Ã­tems no vistos), **F5** estado (`StudentNodeState`) â€” que ademÃ¡s habilita las partes con
  estado de F6 (âœ“/! y "siguiente recomendado"). Foco actual: **poblar banco/contenido** (pipeline
  NotebookLMâ†’JSONLâ†’`load_exercise_bank`).

- ðŸ“š **Biblioteca de Conocimiento Estructurada** â€” `1-por-iniciar/biblioteca-conocimiento-estructurada.md`
  (PR #89). Estructura universal por conceptos, partiendo por **MatemÃ¡tica preuniversitaria**. 4 capas por
  recurso (teÃ³rico / banco estructurado / prÃ¡ctica aleatoria / evaluaciÃ³n), 6 ejes de clasificaciÃ³n de
  ejercicios, mapa de cobertura acordeÃ³n. Plan **F0â€“F6 con gates del ðŸ§‘**. **Bloqueado por:** el ðŸ§‘ debe
  entregar los **Ã­ndices** de sus libros de matemÃ¡tica para arrancar la Fase 1 (esqueleto en
  `docs/conocimiento/matematica.yaml`).
- ðŸ”¨ **GuÃ­as interactivas â€” Fases 4â€“7** (epic `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`).
  Fases 1â€“3 âœ…. Handoffs de arquitectura redactados en `2-arquitectura/`:
  **F4** parser respuesta directa en `3-construccion/` (ðŸŸ¢ Ready tras preflight,
  `seguridad:requiere-claude`),
  **F5** evaluaciones nivel/final âœ… (cerrada, PR #83), **F6** PDF âœ… (cerrada, PR #84 â€” print nativo),
  **F7** gate + piloto (ðŸŸ¡ construida por Claude, en `4-auditoria/`, esperando audit de Codex â€”
  **Ãºltima fase**),
  **F7** migraciÃ³n legacy + gate + piloto (ðŸŸ¡). Construir **en orden**, una fase por rama, cada una con preflight de Codex.
- ðŸ”¨ **PoblaciÃ³n de contenido â€” MAT completa (1.891 recursos pendientes):**
  Handoffs autÃ³nomos en `backlog/2-arquitectura/` â€” uno por eje/grupo:
  - `poblar-contenido-mat-num-b0201-b0202.md` â€” 56r (21 B0201 + 35 B0202), rama `content/mat-num-b0201-b0202`
  - `poblar-contenido-mat-num-b0203-b0206.md` â€” 289r (B0203 Racionales + B0204 Reales + B0205 Razones + B0206 Sucesiones), rama `content/mat-num-b0203-b0206`
  - `poblar-contenido-mat-fund.md` â€” 106r (B0101 LÃ³gica + B0102 Conjuntos), rama `content/mat-fund`
  - `poblar-contenido-mat-est.md` â€” 260r (B0501â€“B0507 EstadÃ­stica+Probabilidad), rama `content/mat-est`
  - `poblar-contenido-mat-alg.md` â€” 698r (B0301â€“B0315 Ãlgebra y Funciones), rama `content/mat-alg`
  - `poblar-contenido-mat-geo.md` â€” 482r (B0401â€“B0413 GeometrÃ­a), rama `content/mat-geo`
  Todos listos para Antigravity. El proceso: query de pendientes â†’ YAML â†’ JSONL â†’ `load_node_content` â†’ `load_exercise_bank` â†’ commit por tanda.
- ðŸ”¨ **PWA bÃ¡sica** â€” `backlog/2-arquitectura/pwa-progressive-web-app.md`. Ready para Codex (preflight)
  â†’ Antigravity (rama `feat/pwa-basica`). Manifest + SW conservador + offline + iconos; sin tocar CSP.
- âœ… **Estudio de banco de preguntas â€” CERRADO ðŸŸ¢ y ARCHIVADO (2026-06-18).** Construido y desplegado
  (PRs #62â€“#67): generaciÃ³n IA, config por recurso, ediciÃ³n y runtime. Tarjeta movida a
  `6-finalizados/estudio-banco-preguntas.md`. (F4 multimodal sigue bloqueada por storage externo â€”
  fuera de alcance por ahora.)

## Ãšltimas entregas
- 2026-06-28 â€” ðŸ›ï¸ Claude: **Handoff autÃ³nomo de poblaciÃ³n de contenido MAT.NUM B0201+B0202.**
  Creado `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` â€” listo para
  ejecuciÃ³n por Antigravity (o cualquier IA). Cubre 56 recursos pendientes: 21 de B0201
  (ENTEROS_OPERATORIA) + 35 de B0202 (divisibilidad/primos/MCM/MCD). Tanda 1 de B0202 ya
  cargada en BD (5 recursos DIVISIBILIDAD + 50 ejercicios). El handoff incluye: tablas de
  recursos por tanda, reglas de formato YAML/JSONL, abreviaciones `stable_id`, comandos de
  carga y verificaciÃ³n, criterios de aceptaciÃ³n y lista de no-tocar.
- 2026-06-28 â€” ðŸ›ï¸ Claude: **Tanda 1 B0202 generada y cargada en BD (5 recursos + 50 ejercicios).**
  Archivos YAML: `mat-num-divisibilidad-{multiplo-concepto,divisor-concepto,division-exacta,
  obtencion-multiplos,obtencion-divisores}.yaml`. JSONL: `mat-num-teoria-numeros-banco-gen-1.jsonl`.
  Corregido error en OMULT-GEN-PAES-2 (correct_answer 15â†’14). Cargado con `load_node_content`
  (5 created) + `load_exercise_bank` (50 ejercicios). Estrategia documentada en
  `docs/conocimiento/estrategia-poblacion.md`.
- 2026-06-28 â€” ðŸ›ï¸ Claude: **Estructura de recurso documentada como estÃ¡ndar.**
  AÃ±adida secciÃ³n `## 0. Estructura completa de la pÃ¡gina de recurso` a
  `docs/conocimiento/pauta-contenido.md`: las 11 secciones de la pÃ¡gina `/aprender/<slug>/`
  descritas con fuente de datos (modelo/campo), formato, reglas de presencia, propÃ³sito
  pedagÃ³gico y diagramas ASCII de cada tipo de ejemplo/ejercicio. Es el estÃ¡ndar de referencia
  para cualquier contenido nuevo.
- 2026-06-28 â€” ðŸ§© Codex: **resÃºmenes de ENTEROS_CONJUNTO versionados en YAML.**
  Diagnosticado el borrado al recargar contenido: los YAML omitÃ­an `resumen` y el loader escribÃ­a
  una cadena vacÃ­a. Los 15 recursos ahora incluyen resumen; pauta actualizada a 9 campos
  obligatorios. ValidaciÃ³n local: 15/15 con resumen, tests focalizados 4/4 OK.
- 2026-06-28 â€” ðŸ›ï¸ Claude + ðŸ§‘: **UI accordeÃ³n + introducciÃ³n didÃ¡ctica + pauta de contenido.**
  Campo `introduccion` en `NodeContent` (migraciÃ³n `0042`) + 15 textos nivel ~10 aÃ±os en YAMLs.
  SecciÃ³n "Ejemplos Verdadero/Falso" renombrada. Fix acordeÃ³n KaTeX (wrap con `<span>` para
  que `justify-content: space-between` no explote los spans de math). Pauta de autorÃ­a
  `docs/conocimiento/pauta-contenido.md` (YAML + JSONL + gamificaciÃ³n + checklist).
- 2026-06-27 (tarde) â€” ðŸ›ï¸ Claude + ðŸ§‘: **Contenido ENTEROS_CONJUNTO estandarizado + banco GEN.**
  15 YAMLs con 4 ejemplos SÃ­/No + 5 errores_frecuentes + estado publicado. 150 ejercicios nuevos
  en 3 archivos JSONL (`-banco-gen-1/2/3.jsonl`): 3 CONC + 1 REC + 3 PROC + 3 PAES por recurso.
  Fixes `generate_node_summaries`: encoding Windows, Gemini multi-part parsing, rate-limit resilience.
  ResÃºmenes pendientes de regenerar (cuota Gemini agotada).
- 2026-06-27 â€” ðŸ›ï¸ Claude + ðŸ§‘: **F1â€“F3 + F6 CERRADAS â€” PR #102 squash-merge a `main` (rama `feat/grafo-conocimiento-f1`).**
  UI rediseÃ±ada: breadcrumb plegable, objetivo card, ejemplos interactivos (V/F/SÃ­-No), errores como
  preguntas conceptuales, banco con tarjetas+sombra. Ejercicios de clasificaciÃ³n (formato `matching`).
  PolÃ­tica **autopublicado inmediato** en `load_exercise_bank`. Contenido: 14 NodeContent + ejercicios
  ENTEROS_CONJUNTO + clasificaciÃ³n. Tests actualizados. Tarjetas en `6-finalizados/`.
- 2026-06-27 â€” ðŸ›ï¸ Claude + ðŸ§‘: **F3 â€” estructura pedagÃ³gica por Ã­tems (`ItemGroup` + `NodeExercise` + pipeline JSONL) â€” rama `feat/grafo-conocimiento-f1`.**
  Decisiones **D2/D3/D4** ratificadas en la arquitectura (Â§8). Modelos nuevos **aditivos** anclados a
  `KnowledgeNode` (Sistema A intacto): `ItemGroup` (7 grupos estÃ¡ndar) + `NodeExercise` (banco Ãºnico,
  `kind=item|template` para generadores futuros), migraciÃ³n `0039`, admin, comando idempotente
  `load_exercise_bank` (JSONL NotebookLMâ†’Claude; **nunca autopublica**; no degrada publicaciones
  manuales), secciÃ³n "Practica por Ã­tems" (acordeÃ³n + toggle soluciÃ³n + KaTeX), prompts en
  `docs/conocimiento/pipeline/`. Piloto Naturales (4 ejercicios) verificado en navegador. 20 tests
  nuevos. Tarjeta F3 â†’ `4-auditoria/`.
- 2026-06-27 â€” ðŸ›ï¸ Claude: **F6 (estructural) â€” prerrequisitos DAG + "Antes de empezar" â€” misma rama.**
  Comando `load_prerequisites` (YAMLâ†’`NodePrerequisite`, valida aciclicidad con `graphlib`, aborta sin
  escribir si hay ciclo, idempotente), secciÃ³n informativa "Antes de empezar" en la pÃ¡gina
  (`_prereqs.html`, enlaces a prerrequisitos publicados, nunca bloquea), DAG piloto `num-enteros.yaml`,
  timestamps en `NodeContent` (mig. `0040`). 13 tests. Estado por alumno (âœ“/!) y "siguiente
  recomendado" diferidos a F5. Verificado en navegador. Tarjeta F6 a `4-auditoria/`.
- 2026-06-26 â€” ðŸ›ï¸ Claude + ðŸ§‘: **F2 construido â€” `NodeContent`/`NodeMedia` + app `learn` + `/aprender/` â€” rama `feat/grafo-conocimiento-f1`.**
  Modelos con migraciÃ³n `0038`, app `apps/learn/` con 6 rutas jerÃ¡rquicas, 3 templates (home/list/detail),
  KaTeX por herencia de `base.html`, comando `load_node_content` idempotente (actualiza `NodeMedia` si
  YAML incluye clave `media:`), admin inlines, YAML ejemplo piloto. 22 tests nuevos. **554/554 verde.**
  Tarjeta F2 movida a `4-auditoria/`.
- 2026-06-26 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Arquitectura de plataforma (6 capas) + F1 construido â€” rama `feat/grafo-conocimiento-f1`.**
  RediseÃ±o en 6 capas (bancoâ‰ evaluaciÃ³n; estado solo-rendimiento; asignatura como nodo raÃ­z para
  FÃ­sica/QuÃ­mica a futuro). Tarjetas F1â€“F6. **F1 construido y verde:** `KnowledgeNode`/`NodePrerequisite`,
  `import_knowledge_tree` idempotente (2208 nodos importados, 13 legacy omitidos), admin, migraciÃ³n `0037`,
  8 tests. Detalle en `reportes-sesion/2026-06-26.md`. **Siguiente: F2 (contenido + pÃ¡ginas, piloto NÃºmeros Enteros).**
- 2026-06-25 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Biblioteca de Conocimiento â€” esqueleto YAML completo (ejes 01â€“05) â€” PR #99 abierto.**
  Eje 05 PROBABILIDAD Y ESTADÃSTICA (7 bloques 05.01â€“05.07), Eje 02 ampliado (02.06 Sucesiones),
  Eje 03 completado (03.11â€“03.15), Eje 04 ampliado (04.12â€“04.13). Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Total: ~700 recursos en 37 bloques, 5 ejes.
- 2026-06-25 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Eje 04 GEOMETRÃA completo â€” PR #98 en auto-merge.**
  11 bloques YAML atÃ³micos (04.01â€“04.11), ~382 recursos, 55 temas. Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Conflict `TRIANGULOS_NOTABLES` resuelto
  con sufijo `_METRICA` en 04.04. Prompts para eje 05 PROBABILIDAD Y ESTADÃSTICA entregados.
- 2026-06-23 (tarde) â€” ðŸ›ï¸ Claude + ðŸ§‘: **Bugfixes operativos de guÃ­as + proyecto nuevo.**
  (1) **PR #87** `gunicorn --timeout 120` + truncar guÃ­a en extracciÃ³n de Ã­tems: arregla el
  `SystemExit: 1` (worker abortado a los 30 s en la llamada sÃ­ncrona a Gemini; detectado por Sentry
  `PYTHON-DJANGO-K`). **âš ï¸ El Custom Start Command de Railway sobrescribe los archivos del repo â†’
  el ðŸ§‘ debe agregar `--timeout 120 --workers 3` en el dashboard.** (2) **PR #88** N+1 en
  `/asignaturas/` (30â†’3 queries; `SubjectListView` con `select_related`/`prefetch_related` + agrupado
  en memoria). (3) DiagnÃ³stico de lentitud del sitio: **no era el cÃ³digo** sino **1 worker de gunicorn**
  saturado por los clics de extracciÃ³n que colgaban el worker â†’ recomendado `WEB_CONCURRENCY=3`.
  (4) **PR #89** tarjeta de backlog del proyecto **Biblioteca de Conocimiento Estructurada**.
  Tracing de Sentry activado temporal (`SENTRY_TRACES_SAMPLE_RATE=1.0`, **revertir a 0**).
- 2026-06-23 â€” ðŸ›ï¸ Claude: **Re-auditorÃ­a profunda del Ã©pico (F1â€“F7) + correcciones ðŸŸ¢.**
  Doc en `docs/auditorias/2026-06-23-auditoria-epico-guias-interactivas.md`. F1â€“F6 sÃ³lidas. 5 hallazgos
  en F7 (Media/Baja, sin afectar datos), todos corregidos: `merge_items`/`edit_practice_quota` no
  funcionaban en staging (guard `enabled`â†’`editable`); un tema legacy no podÃ­a entrar a staging desde
  la UI (selector propio con todos los temas activos); `redirect` no importado en `item_review.py`
  (bug latente, NameError en ruta no-HTMX); gate contaba banco visible sin filtrar por la guÃ­a pÃºblica.
  13 tests F7 (de 9). Sin migraciones. Rama `fix/guias-fase7-auditoria`.
- 2026-06-23 â€” ðŸ›ï¸ Claude: **Fase 7 (gate + piloto) PREFLIGHT + CONSTRUIDA ðŸŸ¡ â€” esperando auditor distinto.**
  Modelo de coexistencia (no se toca el legacy). `Topic.structured_bank_staging` (mig. aditiva `0036`)
  + `structured_bank_editable` para preparar con el flag apagado; gate solo-lectura que reusa los
  ensambladores; activaciÃ³n admin gobernada por el gate + rollback. 9 tests F7. Rama
  `feat/guias-fase7-gate-piloto`; `seguridad:requiere-claude`. Audita ðŸ§© Codex (IA distinta al builder).
- 2026-06-23 â€” ðŸ›ï¸ Claude: **Fase 6 (PDF) AUDITADA Y CERRADA ðŸŸ¢ â€” merge de PR #84 a `main`.**
  Auditor distinto al builder (Codex). Fase solo-front: verificado print nativo (sin JS/deps nuevas,
  CSP intacta), el fix del bug de texto invisible (`!important` vence color inline), portada solo-print
  con a11y correcta, solucionario Ãºnico consolidado y saltos de pÃ¡gina. Test fija la decisiÃ³n
  (`assertNotContains("html2pdf")`). CI Linux verde (511 OK, 1 skip), sin migraciones. **Sin errores.**
- 2026-06-23 â€” ðŸ›ï¸ Claude: **Preflight Fase 6 (PDF) RESUELTO ðŸŸ¢ â€” Ready para ðŸ”¨ Antigravity.**
  DecisiÃ³n del ðŸ§‘: **print nativo** (`window.print()` + `@media print`), NO html2pdf.js (riesgo
  `unsafe-eval`/CSP, rasterizaciÃ³n del tema oscuro, ~1 MB JS). Realidad encontrada: el
  `learning-guide-print.css` estÃ¡ **obsoleto** (apunta a clases inexistentes), `header{display:none}`
  **oculta logo+tÃ­tulo** (no hay portada) y las clases Bootstrap/inline dejan **texto invisible** en
  papel. Alcance afinado: reescribir el print CSS contra el markup real, portada solo-print, forzar
  texto negro, resolver doble solucionario, relabelar botÃ³n. **Sin migraciones** (front).
  Tarjeta en `backlog/3-construccion/`; rama `feat/guias-fase6-pdf`.
- 2026-06-23 â€” ðŸ›ï¸ Claude: **Fase 5 AUDITADA Y CERRADA ðŸŸ¢ â€” merge de PR #83 a `main`.**
  Auditor distinto al builder (Codex). Verificadas las invariantes sensibles: timers 100% server-side,
  consumo de intento transaccional y **por-recurso** (no global), aislamiento `scope+flag`, reuso del
  parser seguro de Fase 4, **protecciÃ³n de historial** (409 al editar preguntas ya usadas; pools solo se
  archivan), ownership/CSRF, guards anti-DoS del ensamblador y gating de cobertura. Los 9 hallazgos del
  self-audit de Codex estÃ¡n corregidos; **no encontrÃ© P0/P1 nuevos**. CI Linux verde (510 OK, 1 skip),
  sin migraciones. `audit:aprobado` aplicado.
- 2026-06-22 â€” ðŸ›ï¸ Claude: **Preflight Fase 5 RESUELTO ðŸŸ¢ â€” Ready para construir.**
  Contrastado contra el cÃ³digo real. Hueco de alcance resuelto (decisiÃ³n ðŸ§‘: **Fase 5 incluye la
  generaciÃ³n de los pools ocultos** â€” `visible_bank_service` hardcodea `banco_visible`). Contradicciones
  fijadas: `final_distribution` mapea a `level` (N1/N2/N3); timer (`expires_at = inicio + config`) â‰ 
  cota de duraciÃ³n (`sum(estimated_minutes)Â±%`), exigir `estimated_minutes>0`; intento en transacciÃ³n
  + una sola sesiÃ³n `en_curso`. Dominio por **Ãºltimo intento** (60/40, â‰¥80% y final â‰¥80%), funciÃ³n
  nueva sin tocar el `progress_service` legacy. Sin migraciones esperadas. Tarjeta en
  `backlog/3-construccion/`; construye ðŸ”¨ Antigravity (`feat/guias-fase5-evaluaciones`).
- 2026-06-22 â€” ðŸ›ï¸ Claude: **Fase 4 AUDITADA Y CERRADA ðŸŸ¢ â€” merge de PR #82 a `main`.**
  Auditor distinto al builder (Codex). Propiedad crÃ­tica intacta (sin `eval`/`exec`/`parse_expr`/
  `sympify(string)`; whitelist AST; inyecciÃ³n bien cubierta). Hallazgo Medium de DoS corregido por
  excepciÃ³n (Claude builder, por decisiÃ³n del ðŸ§‘): apilamiento de exponentes `(...**n)**m` evadÃ­a
  `MAX_EXPONENT_ABS` y explotaba en `cancel` (~296 MB + cuelgue confirmado); fix con
  `MAX_TOTAL_DEGREE=32` + `_degree_upper_bound` que corta sobre el AST antes del paso caro (<0,04 s).
  **494 tests OK**, sin migraciones, `check --deploy` exit 0. `audit:aprobado` aplicado.
- 2026-06-22 â€” ðŸ§© Codex: **Fase 4 CONSTRUIDA â€” PR #82 esperando auditor distinto ðŸŸ¡.**
  Parser ASTâ†’SymPy seguro, respuestas numÃ©ricas/algebraicas, panel editorial y prÃ¡ctica mixta
  completados. **493 tests OK local y CI Linux completo verde** (incluido timeout `SIGALRM`);
  pip-audit, deploy-check, migraciones, Ruff y pre-commit verdes. El Ãºnico check rojo es el gate
  organizativo que exige revisiÃ³n de otra IA. Auto-merge deshabilitado; label
  `seguridad:requiere-claude` aplicado.
- 2026-06-22 â€” ðŸ§© Codex: **Preflight Fase 4 â€” LISTO PARA CONSTRUIR ðŸŸ¢.**
  Se resolvieron las contradicciones del handoff: la prÃ¡ctica visible no persiste `text_answer`;
  parser ASTâ†’SymPy nodo a nodo sin `parse_expr`/`sympify(string)`; tolerancia absoluta; gramÃ¡tica,
  lÃ­mites y timeout concretos; ediciÃ³n/publicaciÃ³n por tipo; prÃ¡ctica mixta y adaptaciÃ³n
  retrocompatible del reproductor. SymPy 1.14.0 queda como dependencia nueva. Tarjeta movida a
  `backlog/3-construccion/`.
- 2026-06-22 â€” ðŸ›ï¸ Claude: **Fix dificultad acentuada â€” ðŸŸ¢ mergeado a `main`** (`fix/dificultad-acentos`).
  Detectado en QA local: con API key real, la generaciÃ³n de guÃ­as de F2 fallaba la validaciÃ³n porque
  la IA devuelve dificultades **con acento** (`"bÃ¡sica"`) y el modelo usa claves **sin acento**
  (`basica/.../desafio`); ademÃ¡s F1 perdÃ­a silenciosamente la dificultad a "intermedia". Se agregÃ³
  `Question.normalize_difficulty()` y se canonizÃ³ en prompts/mocks/validaciÃ³n/plantilla
  (`item_extraction`, `learning_guide`, `visible_bank`, `item_review`, `_item_row.html`). +3 tests.
  **472 tests OK**, sin migraciÃ³n. Verificado en navegador (badge "BÃ¡sica" correcto).
- 2026-06-22 â€” ðŸ›ï¸ Claude + ðŸ”¨ Antigravity + ðŸ§© Codex: **GuÃ­as interactivas â€” Fases 2 y 3 CERRADAS ðŸŸ¢
  y mergeadas a `main`** (squash-merge, F2+F3 juntas; F3 se construyÃ³ sobre F2 sin mergear).
  **F2** (guÃ­a ProfeOnline original + anti-copia): generaciÃ³n IA, motor de originalidad determinista
  (n-gramas de 10 palabras + blocklist + tope anti-DoS), publicaciÃ³n manual bloqueada con
  **revalidaciÃ³n en caliente por hash**, versionado con `archivada` y guÃ­a Ãºnica pÃºblica por tema.
  Cierre legal de ðŸ›ï¸ Claude (`seguridad:requiere-claude`) âœ…. **F3** (banco visible + estudio):
  pÃ¡gina pÃºblica de la guÃ­a (KaTeX, imprimible), banco agrupado por Ã­tem/dificultad, prÃ¡ctica
  por Ã­tem/mixta **sin peso acadÃ©mico**, panel editorial con cuotas/dÃ©ficit/generaciÃ³n, y
  **aislamiento del banco legacy con `scope=""`**. ConstruyÃ³ Antigravity; Codex auditÃ³/corrigiÃ³ ambas;
  ðŸ›ï¸ Claude verificÃ³ en corrida limpia y cerrÃ³. **Barrera: 469 tests OK** + `check --deploy` 0 errores
  + sin migraciones pendientes. Migraciones aplicadas: `0034` (F1), `0035` (F2). Tarjetas en
  `backlog/6-finalizados/`. **Pendiente P3 (no bloqueante): QA visual mÃ³vil 320/360/390. Siguiente: F4.**
- 2026-06-22 â€” ðŸ§© Codex: **GuÃ­as interactivas â€” Fase 3 APROBADA TÃ‰CNICAMENTE ðŸŸ¢.**
  Se corrigieron publicaciÃ³n incompleta/automÃ¡tica, borrado fÃ­sico, ediciÃ³n en caliente de preguntas
  publicadas, revalidaciÃ³n del submit, cruces entre temas, cuotas concurrentes, UI editorial ausente,
  render del esquema real de Fase 2, CSP y N+1. **469 tests OK** en 324,059 s; 13 tests especÃ­ficos,
  104 regresiones afectadas, deploy-check, migraciones y pre-commit verdes. Tarjeta movida a
  `backlog/5-cierre/`; queda revisiÃ³n final y merge por ðŸ›ï¸ Claude.
- 2026-06-22 â€” ðŸ”¨ Antigravity: **GuÃ­as interactivas â€” Fase 3 (banco visible + experiencia de estudio) â€” LISTO PARA AUDITORÃA ðŸŸ¡**
  (rama `feat/guias-fase3-banco-visible`). Se completÃ³ la implementaciÃ³n de la Fase 3 del epic. Aislamiento legacy (scope="") en selectors de disponibilidad, quiz y evaluaciÃ³n final. Servicio `visible_bank_service.py` con generaciÃ³n atÃ³mica por dÃ©ficit (borrador + publicada) y selector round-robin mixto. Panel editorial HTMX en `item_extraction` (cuota editable inline y generaciÃ³n con indicador de carga). RevisiÃ³n ampliada en `question_review` para `banco_visible` con secciÃ³n editorial separada, sincronizaciÃ³n de `canonical_answer` en alternativas y validaciÃ³n/envÃ­o/acciones masivas con rechazo estricto (HTTP 400). Detalle de guÃ­a pÃºblico (/guias/<slug>/) para alumnos con logo, Katex y CSS de impresiÃ³n. PrÃ¡ctica no acadÃ©mica fullscreen con guardado de sesiÃ³n (filtros/orden/IDs) y calificaciÃ³n al vuelo libre de escrituras en BD. 10 tests de integraciÃ³n especÃ­ficos y pre-commit hooks verdes. Tarjeta movida a `backlog/4-auditoria/`.
- 2026-06-22 â€” ðŸ§© Codex: **Preflight Fase 3 â€” LISTO PARA CONSTRUIR ðŸŸ¢.**
  Handoff refinado contra el cÃ³digo real: servicio propio para generar preguntas
  `scope="banco_visible"` en borrador reutilizando candidatos IA, panel por Ã­tem/recurso,
  aislamiento obligatorio `scope=""` del quiz legacy, prÃ¡ctica no acadÃ©mica sin `QuizAttempt`,
  query anti-N+1, integraciÃ³n tema/recurso, reproductor fullscreen, CSP, KaTeX y CSS print.
- 2026-06-22 â€” ðŸ§© Codex: **GuÃ­as interactivas â€” Fase 2 APROBADA TÃ‰CNICAMENTE ðŸŸ¢.**
  AuditorÃ­a con correcciones de versionado, autorizaciÃ³n/bloqueo de fuentes, contrato JSON estricto,
  flujo HTMX, selecciÃ³n OpenAI/Gemini, hash canÃ³nico y concurrencia. **456 tests OK**, deploy-check,
  migraciones, pre-commit y diff-check verdes. Tarjeta movida a `backlog/5-cierre/`; queda auditorÃ­a
  legal final y merge por ðŸ›ï¸ Claude (`seguridad:requiere-claude`).
- 2026-06-22 â€” ðŸ”¨ Antigravity: **GuÃ­as interactivas â€” Fase 2 (guÃ­a ProfeOnline original + originalidad) â€” LISTO PARA AUDITORÃA ðŸŸ¡**
  (rama `feat/guias-fase2-guia-original`, `seguridad:requiere-claude`). Se completÃ³ la implementaciÃ³n
  de la Fase 2 del epic. LÃ³gica aditiva con campos de originalidad en `LearningGuide` (migraciÃ³n `0035`),
  servicio de generaciÃ³n con IA (grounded en Ã­tems aprobados del tema y fuentes privadas, anti-injection),
  motor de originalidad determinista sin truncamiento silencioso (n-gramas de 10 palabras y blocklist de
  marcas), control de concurrencia y revalidaciÃ³n en caliente mediante transacciones atÃ³micas y
  bloqueos select_for_update (para Topic y guÃ­as ordenadas), restricciÃ³n unique_active_published_guide_per_topic,
  panel HTMX CSP-safe (sin JS inline), y 17 tests unitarios focalizados. Barrera completa
  verificada (449 tests Django OK, check --deploy OK, makemigrations --check OK, pre-commit OK).
  Tarjeta movida a `backlog/4-auditoria/`.
- 2026-06-22 â€” ðŸ›ï¸ Claude + ðŸ”¨ Antigravity + ðŸ§© Codex: **GuÃ­as interactivas â€” Fase 1 CERRADA ðŸŸ¢**
  (squash-merge a `main`, commit `6ccf403`). Panel solo-admin `/publicar/items/`: la IA propone
  Ã­tems de aprendizaje desde una guÃ­a privada (`QuizGuide`) calibrando dificultad al nivel educativo,
  y el profesor los edita/fusiona/aprueba/archiva. Todo **detrÃ¡s del flag
  `Topic.structured_bank_enabled`** (banco legacy intacto). Antigravity construyÃ³; Codex rechazÃ³ por
  5 P1 + 5 P2; ante la falta de correcciones del builder, ðŸ›ï¸ Claude (por decisiÃ³n del ðŸ§‘) corrigiÃ³
  **todos** los hallazgos (flag server-side, fusiÃ³n mismo-tema, CSPâ†’JS externo con nonce,
  `detected_exercise_count` con migraciÃ³n aditiva `0034`, validaciÃ³n de guÃ­a, N+1, dedupe IA, choices,
  `_sanitize_key`) y cerrÃ³. **432 tests OK** + barrera completa verde. Tarjeta en
  `backlog/6-finalizados/`. **PrÃ³ximo: Fase 2 (guÃ­a ProfeOnline original + anti-copia,
  `seguridad:requiere-claude`).**
- 2026-06-22 â€” ðŸ§© Codex: **Fase 1 de guÃ­as interactivas â€” GATE RECHAZADO ðŸ”´.**
  Suite completa **425 tests OK**, `check --deploy` sin errores, sin migraciones y pre-commit verde;
  pero quedaron P1: flag por tema no aplicado, fusiÃ³n cruzada entre temas, JS inline bloqueado por
  CSP, `detected_exercise_count` descartado y guÃ­a no validada contra el tema. Tarjeta con hallazgos
  devuelta mediante `git mv` a `backlog/3-construccion/` para correcciÃ³n por ðŸ”¨ Antigravity.
- 2026-06-22 â€” ðŸ”¨ Antigravity: **GuÃ­as interactivas â€” Fase 1 (extracciÃ³n y aprobaciÃ³n de Ã­tems) â€” LISTO PARA AUDITORÃA ðŸŸ¡**
  (rama `feat/guias-fase1-extraccion-items`). Se implementÃ³ el servicio de extracciÃ³n curricular IA `item_extraction_service.py` (calibra la dificultad por nivel pedagÃ³gico y soporta LaTeX) y el panel HTMX in-app `publicar/items/` (ediciÃ³n inline, aprobaciÃ³n/archivado, vinculaciÃ³n de recursos y fusiÃ³n segura de Ã­tems). Todo 100% aditivo y detrÃ¡s del flag de tema. Suite completa con 425 tests OK (10 nuevos para esta fase). Tarjeta movida de `2-arquitectura/` a `4-auditoria/`.
- 2026-06-21 â€” ðŸ›ï¸ Claude + ðŸ§© Codex + ðŸ§‘: **RediseÃ±o de recurso + progreso acadÃ©mico â€” CERRADO ðŸŸ¢**
  (rama `feat/recurso-progreso-academico`). Vista de recurso rediseÃ±ada (tÃ­tulo primero, metadatos
  compactos, descripciÃ³n con Ver mÃ¡s/menos, columna legible, sin barra "Comprendido") + bloque Ãºnico
  "Practica y evalÃºa tu aprendizaje" con pestaÃ±as por nivel. **Progreso calculado desde intentos
  reales**: promedio de los Ãºltimos 3 por modo, ponderado 30/70, estados Preparado/Aprobado; motor
  `progress_service` + selectores sin N+1. Perfil ampliado con panel por tema/recurso. "Comprendido"
  retirado de la UI (endpoint+modelo conservados); agregados de tema usan progreso ponderado.
  ðŸ§© Codex corrigiÃ³ disponibilidad por modo, cobertura real del perfil y pestaÃ±as mÃ³viles.
  **Sin migraciones. 391 tests OK + QA 320/360/390 px. PR #75 squash-mergeado**
  en `main` (`3d847a6`, 2026-06-21). Tarjeta en `backlog/6-finalizados/`.
- 2026-06-21 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Reproductor de preguntas a pantalla completa â€” CERRADO ðŸŸ¢** (commit
  `faacd8c`, merge a `main`). Panel interno fullscreen (mÃ³vil + PC): una pregunta a la vez con
  `Anterior`/`Siguiente`, pantalla de revisiÃ³n respondida/pendiente previa al envÃ­o y resultados a
  pantalla completa con correcciÃ³n. Aplica a PreparaciÃ³n, EvaluaciÃ³n por nivel y evaluaciÃ³n final del
  tema. Overlay global `#quiz-player-root` + `static/js/quiz-player.js` (CSP-safe), reusa las vistas
  HTMX; `quiz_submit` ordena resultados por orden de presentaciÃ³n. **Sin migraciones ni endpoints
  nuevos. Suite completa 370 OK** + QA visual (escritorio y mÃ³vil 360px). Tarjeta en
  `backlog/6-finalizados/`.
- 2026-06-21 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Agente local de subida `upload-batch/v1`** (commit `79836ad`).
  `scripts/process_upload_batch.py` sube cada video como no listado, obtiene la transcripciÃ³n
  desde la IP local, registra el Ã­tem en ProfeOnline y espera la validaciÃ³n antes de hacerlo
  pÃºblico (revierte a no listado si la confirmaciÃ³n server-side falla). Cierra el **paso 2** del
  pipeline Ãºnico de publicaciÃ³n: el cliente Node `profeonline-uploader` se reemplaza por este
  agente Python local. Incluye `cleanup_borradores` (limpia borradores residuales, dry-run por
  defecto, respeta Ã­tems en vuelo) + tests del agente (4 OK). Sin migraciones.
- 2026-06-21 â€” ðŸ§© Codex + ðŸ§‘: **TaxonomÃ­a, cobertura y Lenguaje Algebraico actualizados en producciÃ³n.**
  Asignaciones vigentes: Electromagnetismo â†’ FÃ­sica; FÃ­sica Escolar â†’ FÃ­sica +
  Medio/Preuniversitario; MatemÃ¡tica Media/Preuniversitaria â†’ MatemÃ¡ticas. El resumen del banco usa
  Ãreaâ†’Nivelâ†’Asignaturaâ†’Temaâ†’Recurso y orden Escolarâ†’Medio/Preuniversitarioâ†’Universitario.
  Lenguaje Algebraico quedÃ³ con 1.530 preguntas (90 en cada uno de 17 recursos), cobertura 17/17 y
  orden manual `1.xâ†’2.xâ†’3.xâ†’4.01â†’4.01aâ†’4.02â†’4.03â†’4.04`.
- 2026-06-20 â€” ðŸ›ï¸ Claude + ðŸ§‘: **Nivel educativo por asignatura (rama `feat/nivel-por-asignatura`).**
  Nuevo campo `Subject.education_level` (migraciÃ³n 0031) que los temas/recursos sin nivel propio
  heredan vÃ­a `Resource.get_education_level()`; cableado en generaciÃ³n inline, estudio, pipeline y
  `generate_pending_questions`. Comando `set_subject_level --subject â€¦ --level â€¦ [--apply]` (dry-run
  por defecto). Aplicado en producciÃ³n: **FÃ­sica Escolar â†’ Medio/Preuniversitario**. Tests
  focalizados verdes.
- 2026-06-20 â€” ðŸ›ï¸ Claude + ðŸ§‘: **RediseÃ±o de dos paneles del banco (rama `feat/rediseno-resumen-banco`).**
  (1) Resumen `/publicar/preguntas/resumen/` â†’ acordeÃ³n
  Ãreaâ†’Nivelâ†’Asignaturaâ†’Temaâ†’Recurso con fracciones
  `auditados/total` por categorÃ­a editorial, preguntas por nivel y semÃ¡foro (verde/amarillo/rojo <20%).
  (2) `question_review` â†’ config de evaluaciÃ³n full-width arriba + generador IA por nivel/modo con
  cantidad y descripciÃ³n; Gemini ahora ve las preguntas existentes para no repetir; "copiando documento"
  deshabilitado. Sin migraciones. Tests focalizados verdes. Detalle en
  `reportes-sesion/2026-06-20-rediseno-paneles-banco.md`. QA visual y despliegue completados.
- 2026-06-18 â€” ðŸ›ï¸ Claude: **Cierre de Fase 5 (auditorÃ­a final).** Auditados como no destructivos el
  generador local aditivo (`scratch/generate_math_questions.py`: sin `.delete()`, dedup por
  `existing_texts`) y el importador transaccional (`import_questions_json` dentro de `transaction.atomic`).
  Tarjeta **"Estudio de banco de preguntas"** archivada (`4-auditoria` â†’ `6-finalizados`); `4-auditoria/`
  queda vacÃ­a (solo `.gitkeep`). Barrera re-verificada local: **331 tests OK**; `check --deploy` solo con
  warnings de dev-settings (sin errores).
- 2026-06-16 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **Banco de preguntas con generaciÃ³n IA CERRADO ðŸŸ¢** (6 PRs:
  #62 banco+generaciÃ³n grounded, #63 fix key-leak + backoff 429, #64 transcript guardado en el recurso,
  #65 `backfill_transcripts`, #66 dos modos video/documento + UI de guÃ­as, #67 filtro `--subject`).
  289 tests. **Aprendizaje:** YouTube bloquea el scraping masivo de transcripts por IP â†’ se bajan a
  cuentagotas desde el PC y se guardan. Detalle y pendientes en `reportes-sesion/2026-06-16.md`.
- 2026-06-05 â€” ðŸ›ï¸ðŸ”¨ðŸ§© **"Estudio de publicaciÃ³n (Fase 1)" CERRADO ðŸŸ¢.** PÃ¡gina staff (`/publicar/estudio/`) que
  arma una **orden de lote** (`profeonline.upload-batch/v1`): selecciona varios videos (solo por nombre, no sube
  contenido), Ãrea/Asignatura/Tema/MÃ³dulo (con creaciÃ³n inline), playlist (enlace o crear nueva) e indicaciÃ³n libre;
  Codex sube a YouTube y publica tal cual. Codex auditÃ³ (P2/P3 menores), QA del ðŸ§‘ detectÃ³ un bug al crear tema inline
  (`resource_ordering_method`) que Claude corrigiÃ³ + test. Mergeado a `main` (squash). Tarjeta en `6-finalizados/`.
  **Sin migraciones.** Pendiente aparte: fix del seed `MatemÃ¡tica` (singular) y la Fase 2 (cola/agente).
- 2026-06-04 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **"Estudio de publicaciÃ³n" SIMPLIFICADO (revisiÃ³n pre-merge).** Tras la QA,
  Octavio pidiÃ³ algo mÃ¡s simple: lote de videos (por nombre) + Ãrea/Asignatura/Tema/MÃ³dulo + playlist + indicaciÃ³n
  libre; Codex hace tÃ­tulo/descripciÃ³n/miniatura/subida tal cual. Se quita copy/duplicados/miniatura/privacidad y se
  agrega selecciÃ³n mÃºltiple de archivos. Tarjeta `4-auditoria` â†’ `3-construccion` para recorte por ðŸ”¨ Antigravity.
  Contrato pasa a `upload-batch/v1`.
- 2026-06-04 â€” ðŸ§© Codex + ðŸ›ï¸ Claude: **Preflight de "Estudio de publicaciÃ³n (Fase 1)" OK** (sin objeciones).
  3 refinamientos integrados al handoff: inline de asignatura setea `Subject.area`; inline de mÃ³dulo setea
  `subject` (+topic/levels) y `module_slug` es solo organizativo; mantener firma de `build_resource_copy`
  (wrapper compatible, tolera `video_url` vacÃ­o). JSON server-side. **Listo para Antigravity.**
- 2026-06-04 â€” ðŸ›ï¸ Claude: **Handoff "Estudio de publicaciÃ³n (Fase 1)" mergeado a `main` (PR #54).**
- 2026-06-04 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **Handoff "Estudio de publicaciÃ³n (Fase 1)" Ready.** Idea creada y
  avanzada `1-por-iniciar` â†’ `2-arquitectura`. PlanificaciÃ³n ðŸ§‘+ðŸ¤– refinada por ðŸ§© Codex (8 acotaciones
  integradas) y verificada contra el cÃ³digo (URL real `/api/recursos/crear-video/`, webhook sin
  `area_slug`/`module_slug`, `Level` M2M). Acotado a la web que genera el JSON; Fase 2 (cola/agente) aparte.
- 2026-06-03 â€” ðŸ›ï¸ðŸ”¨ **Pulido tÃ©cnico a11y/SEO CERRADO ðŸŸ¢ (PR #46).** Antigravity construyÃ³ (focus-trap
  drawer, skip-link, reduced-motion, JSON-LD Person/LocalBusiness, tokens); Claude auditÃ³ (2Âª IA) y
  corrigiÃ³ una regresiÃ³n (`--secondary-hover` borrado del `:root`). Tarjeta en `6-finalizados/`.
- 2026-06-03 â€” ðŸ›ï¸ðŸ§©ðŸ”¨ **Handoff PWA refinado y Ready.** Claude fusionÃ³ el plan de Antigravity + Plan v2
  de Codex y corrigiÃ³ 4 supuestos contra el cÃ³digo (color teal, apple-touch PNG, precache sin hashing,
  start_url no medible). Decisiones ðŸ§‘: theme `#0f766e`, QA iOS opcional. Tarjeta en `2-arquitectura/`.
- 2026-06-03 â€” ðŸ›ï¸ðŸ”¨ **a11y + pulido mÃ³vil CERRADOS ðŸŸ¢ (PR #42, #43).** Contraste AA de WhatsApp,
  drawer mÃ³vil lateral, WhatsApp flotante, contacto (ConcepciÃ³n, sin mail), detalle de recurso reordenado.
- 2026-06-03 â€” ðŸ›ï¸ðŸ”¨ **RediseÃ±o del Home CERRADO ðŸŸ¢.** Antigravity construyÃ³ (Hero reenfocado, perfil
  real de Octavio Chamblas, "CÃ³mo funciona" 2 pasos, destacados condensados); Claude auditÃ³ como 2Âª IA
  y corrigiÃ³ (bug CSS `:active`, CSS muerto de testimonios, imagen huÃ©rfana). Barrera verde. Prueba
  social diferida por falta de testimonios reales (tarjeta nueva).
- 2026-06-03 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **Handoff de Home redactado y Ready.** Decisiones: placeholders
  + contenido hardcodeado (sin modelos/admin). Tarjeta movida `1-por-iniciar` â†’ `2-arquitectura`.
- 2026-06-03 â€” ðŸ›ï¸ðŸ”¨ðŸ§© **VerificaciÃ³n de email mergeada y CERRADA ðŸŸ¢ (PR #38).** Antigravity construyÃ³,
  Codex auditÃ³ (P1 duplicados, P2 anti-enumeraciÃ³n, P3 usuarios sin email), Antigravity corrigiÃ³, Claude
  cerrÃ³ (sensible). 202 tests. `mandatory` + Google exento; migraciÃ³n no bloquea a usuarios actuales.
- 2026-06-03 â€” ðŸ›ï¸ðŸ”¨ðŸ§© **M5 AnalÃ­tica interna mergeada y CERRADA ðŸŸ¢ (PR #36).** Antigravity construyÃ³,
  Codex auditÃ³ y curÃ³ privacidad, Claude cerrÃ³ como 3Âª IA (superficie sensible). Suite 191 tests. Matriz M5 â†’ ðŸŸ¢.
- 2026-06-02 â€” ðŸ§© Codex: **cura privacidad M5 en PR #36** â€” metadata por allowlist de evento,
  `path` sin querystrings, JS sin `href`/texto/`file_url` sensible y regresiones de analitica. Lock liberado.
- 2026-06-02 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **rumbo post-P0 definido.** C1/C2 **aceptados** como riesgo;
  sprint de valor visible (Analytics â†’ Home â†’ QA a11y). Handoff de **Analytics interno** redactado en `2-arquitectura`.
- 2026-06-02 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **rotaciÃ³n de credenciales de prod** (la URL quedÃ³ expuesta en
  chat). CausÃ³ un 500 breve (web cacheaba la `DATABASE_URL` vieja); recuperado con redeploy. Staging
  se desincronizÃ³ por error y se revirtiÃ³. Procedimiento + lecciones en `runbook-backups.md Â§5`.
- 2026-06-02 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **A1 â†’ ðŸŸ¢ staging operativo** en Railway (`Web-staging` +
  `Postgres-Staging` aislada, 200 en `/` y `/admin/`). 2 hallazgos resueltos (`DJANGO_USE_X_FORWARDED_PROTO`,
  `collectstatic`/Custom Start Command) â†’ `runbook-staging.md Â§8`.
- 2026-06-02 â€” ðŸ›ï¸ Claude + ðŸ§‘ Usuario: **C2 â†’ backup real de prod + restore drill verificados**
  (`pg_dump` 18.4; runbook Â§4.B). Riesgo ðŸŸ¡ (falta automatizar).
- 2026-06-02 â€” ðŸ”¨ Antigravity + ðŸ›ï¸ Claude: **Router mergeado (PR #29)** â€” workflow mecÃ¡nico de
  ruteo/labels (sin `contents: write`, sin secretos, no mergea). Revisado por Claude (`seguridad:requiere-claude`).
- 2026-06-02 â€” ðŸ”¨ Antigravity + ðŸ›ï¸ Claude: **A1 mergeado (PR #30)** â€” `check_environment` + runbook
  staging. Riesgo A1 queda ðŸŸ¡ hasta que el ðŸ§‘ Usuario cree el servicio staging + DB propia en Railway.
- 2026-06-02 â€” ðŸ”¨ Antigravity + ðŸ›ï¸ Claude: **C2 mergeado (PR #28)** â€” `backup_db`/`restore_db` con
  guardas anti-prod + runbook. Riesgo C2 queda ðŸŸ¡ hasta backups automÃ¡ticos del proveedor.
- 2026-06-02 â€” ðŸ”¨ Antigravity + ðŸ›ï¸ Claude: **C1b mergeado (PR #27)** â€” `seed_content` idempotente.
- 2026-06-02 â€” ðŸ›ï¸ Claude: **C3 cerrado en ðŸŸ¢** â€” cÃ³digo en `main` (PR #26) + `REDIS_URL` en Railway (PR #31).
- 2026-06-02 â€” ðŸ›ï¸ðŸ”¨ðŸ§© **C1 mergeado (PR #24)** por el flujo completo: Antigravity construyÃ³,
  Codex auditÃ³ (detectÃ³ fuera-de-alcance + `build.sh` + docs), Claude cerrÃ³. Lock liberado.
- 2026-06-02 â€” ðŸ›ï¸ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 â€” ðŸ›ï¸ Claude: automatizaciÃ³n del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 â€” ðŸ›ï¸ Claude: reestructuraciÃ³n de la documentaciÃ³n (PR #19).
