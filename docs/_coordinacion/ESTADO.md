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
- **Biblioteca de Conocimiento — Esqueleto YAML completo al 100% 🟢 (2026-07-04):** auditoría
  completa (script que compara todos los `id:` hoja de `docs/conocimiento/*.yaml` contra
  `semantic_id` en `docs/conocimiento/contenido/*.yaml`) detectó 7 recursos huecos sobre 1911
  definidos: `MAT.FUND.PROPIEDADES_CONJUNTOS.IDEMPOTENCIA_INTERSECCION` (hueco aislado en
  Fundamentos) y 6 recursos del bloque `MAT.GEO.AREAS_TRIANGULOS` (04.04.03) que había quedado a
  medias (`FORMULA_HERON`, `HERON_APLICACION`, `FORMULA_DOS_LADOS_ANGULO`, `TRIANGULOS_IGUAL_BASE`,
  `AREA_REGIONES_COMPUESTAS`, `AREA_COORDENADAS`). Rama `content/cerrar-huecos-fund-geo`, 70
  ejercicios nuevos. **601 tests OK (1 skip)**. Con esto, **los 1911 recursos del árbol completo
  (Fundamentos, Números, Álgebra, Geometría, Probabilidad, Estadística) tienen contenido
  publicado.** **Siguiente:** pasar a F4–F5 (medición/evaluación) sobre todo lo construido, o
  iterar sobre calidad/profundidad del contenido ya existente.
- **Biblioteca de Conocimiento — Estadística Descriptiva (bloque 05.02–05.03 y 05.07) POBLADA
  Y MERGEADA 🟢 (2026-07-04):** rama `content/estadistica-descriptiva` completa, 68 recursos
  nuevos y 680 ejercicios (680 + previos). Bloques cerrados en esta sesión: `RECOLECCION_BASE`,
  `VARIABLES_TIPOS`, `TABLAS_NO_AGRUPADAS`, `DATOS_AGRUPADOS`, `GRAFICOS_BASE`, `GRAFICOS_CONTINUOS`,
  `REPRESENTACIONES_AVANZADAS`, `INTERPRETACION_CRITICA` (estadistica-descriptiva.yaml, completo);
  `MEDIA_PROMEDIO`, `MODA_ANALISIS`, `MEDIANA_ANALISIS`, `MTC_PROPIEDADES` (estadistica-tendencia-central.yaml,
  completo); `PERCENTILES`, `CUARTILES`, `DIAGRAMA_CAJA`, `DISPERSION_BASE`, `DISPERSION_COMPARATIVA`
  (estadistica-posicion-dispersion.yaml, completo); `NORMAL_BASE`, `NORMAL_ESTANDAR`, `NORMAL_CALCULO`,
  `NORMAL_APLICACIONES` (estadistica-normal.yaml, completo). **601 tests OK (1 skip)** antes del
  merge. Squash-merge a `main`. **Siguiente:** decidir próximo eje a poblar (quedan 01-03 del
  esqueleto YAML original) o pasar a F4–F5 de medición/evaluación.
- **Biblioteca de Conocimiento — Ejes 04 (Geometría) y 05 (Probabilidad y Estadística) POBLADOS
  Y MERGEADOS 🟢 (2026-07-03):** contenido completo cargado en `main` para ambas ramas.
  **Geometría (PR #155):** 482 recursos publicados (bloques 04.01–04.13 completos: círculo,
  espacio/cuerpos, cartesiano/vectores, isometrías, trigonometría, analítica ampliada). Merge con
  `--admin` por límite de 300 archivos en `gh pr diff` (tooling, no de contenido; `test (3.12)`
  había pasado limpio). **Probabilidad (PR #156):** 116 recursos publicados (bloques 05.04–05.06
  completos: probabilidad básica, condicional/Bayes, conteo/binomial), 1160 ejercicios nuevos.
  Cada recurso con objetivo/introducción/resumen/explicación/procedimiento/4 ejemplos/3 errores +
  banco de 10 ejercicios + SVG propio. **601 tests OK** en `main` tras ambos merges.
  Cierra el trabajo de población de contenido iniciado con el esqueleto YAML (2026-06-25).
  **Siguiente:** definir próximo eje/bloque a poblar, o pasar a F4–F5 (medición/evaluación).
- **Explorador visual de `/aprender/` — CONSTRUIDO (2026-07-02, rama `codex/redisenar-explorador-aprender`):**
  Tarjetas clickeables en grid 2→1 columnas, hero de marca, breadcrumb horizontal compacto y estados accesibles
  de hover/foco/movimiento reducido. 11 tests focalizados, `check`, migraciones y QA navegador, OK.
- **Plataforma de Conocimiento — ENTEROS_CONJUNTO + UI + pauta de contenido 🟢 (2026-06-28):**
  Todo el contenido ENTEROS_CONJUNTO desplegado en `main`. Campo `introduccion` añadido al modelo
  (migración `0042`) + 15 introducciones didácticas (nivel ~10 años) cargadas en los YAMLs.
  Sección renombrada "Ejemplos Verdadero/Falso" con accordeón nativo. Pauta de contenido
  en `docs/conocimiento/pauta-contenido.md`.
  **Pendiente operativo:** `python manage.py generate_node_summaries --all` (cuota Gemini se restablece a medianoche Pacífico).
- **Plataforma de Conocimiento — F1–F3 + F6 CERRADAS 🟢 (2026-06-27, PR #102):**
  Squash-merge de `feat/grafo-conocimiento-f1` a `main`. Incluye: `KnowledgeNode`/`NodePrerequisite`,
  `NodeContent`/`NodeMedia`, app `learn`, `ItemGroup`/`NodeExercise` (**autopublicado inmediato** —
  `load_exercise_bank` siempre publica; flags `legal_review`/`rewrite_required` son metadata no
  bloqueante), UI rediseñada (`node_detail.html`: breadcrumb plegable, objetivo card, ejemplos
  interactivos V/F/Sí-No, errores como preguntas conceptuales, banco con tarjetas), ejercicios de
  clasificación (formato `matching`), filtro `to_json`. Contenido piloto: 14 NodeContent + ejercicios
  para ENTEROS_CONJUNTO. Tarjetas en `6-finalizados/`.
- **Plataforma de Conocimiento — F6 (prerrequisitos, subconjunto estructural) CONSTRUIDO 🟡 (2026-06-27):**
  Parte que **no depende del estado del alumno** (F5 diferida): comando `load_prerequisites`
  (YAML→`NodePrerequisite`, **valida aciclicidad** con `graphlib`, aborta sin escribir si hay ciclo,
  idempotente) + sección **"Antes de empezar"** informativa en la página del nodo (enlaces a
  prerrequisitos publicados, nunca bloquea) + DAG piloto `num-enteros.yaml` (operatoria←conjunto,
  verificado en navegador) + timestamps en `NodeContent` (migración `0040`). 13 tests nuevos.
  **Diferido a F5:** estado por alumno (✓/!) y "siguiente recomendado". Tarjeta F6 en `4-auditoria/`.
  **Siguiente: poblar banco/contenido (pipeline) · F4–F5 (medición) cuando se decida.**
- **Plataforma de Conocimiento — F1 y F2 CONSTRUIDOS 🟡 (2026-06-26):**
  🏛️ Claude diseñó arquitectura 6 capas + tarjetas F1–F6. **F1** (rama `feat/grafo-conocimiento-f1`):
  `KnowledgeNode`/`NodePrerequisite`, `import_knowledge_tree` idempotente (2208 nodos), migración
  `0037`, 8 tests. **F2 construido en la misma rama:** `NodeContent` (O2O con hoja,
  objetivo/explicación/procedimiento/ejemplos) + `NodeMedia` (video_youtube/file/external,
  video_kind), migración `0038`, app `apps/learn/` con 6 rutas jerárquicas
  `/aprender/<asig>/<eje>/<bloque>/<tema>/<recurso>/`, 3 templates (home/list/detail), KaTeX hereda
  de `base.html`, comando `load_node_content` idempotente, admin inlines. YAML ejemplo:
  `docs/conocimiento/contenido/mat-num-enteros-conjunto-naturales.yaml`. **554/554 tests verde.**
  Tarjetas F1 y F2 en `4-auditoria/`. **F3 construido (2026-06-27).**
- **Guías interactivas - Fase 7 (gate + piloto) - EN AUDITORÍA 🟡 (2026-06-23):**
  🏛️ Claude hizo preflight + construcción (rama `feat/guias-fase7-gate-piloto`). Decisión del 🧑:
  **coexistencia** (no se retira/clasifica el legacy). Nuevo `Topic.structured_bank_staging`
  (migración aditiva `0036`) + propiedad `structured_bank_editable` para preparar el tema con el flag
  apagado; guards admin → `editable`, vistas de alumno siguen en `enabled`. Gate solo-lectura
  (`activation_gate_service`) que reusa los ensambladores reales; activación admin que **solo enciende
  el flag si el gate pasa**; rollback = apagar. 9 tests F7. `check --deploy` exit 0,
  `makemigrations --check` sin cambios. **Gate exige auditoría de IA distinta al builder (🧩 Codex)**;
  `seguridad:requiere-claude`, auto-merge off. Es la **última fase** del épico.
- **Guías interactivas - Fase 6 (PDF) - CERRADA 🟢 (2026-06-23):**
  🧩 Codex reconstruyó la impresión nativa contra el markup real: portada A4, tema claro, KaTeX negro,
  saltos de página y solucionario final consolidado. Botón "Descargar PDF", **sin JS ni librerías
  nuevas** (CSP intacta). 🏛️ Claude auditó como IA distinta: verificó la decisión de print nativo, el
  fix de especificidad (`!important` vence color inline), portada con a11y correcta y solucionario
  único — **sin errores**. **CI Linux verde (511 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#84** a `main` (`22d3d7d`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 7 (migración
  legacy + gate + piloto) — última del épico.**
- **Guías interactivas - Fase 5 - CERRADA 🟢 (2026-06-23):**
  🧩 Codex construyó pools ocultos editoriales, ensamblado por cuotas + distribución 20/50/30,
  no-repetición, sesiones transaccionales con timer server-side, corrección idempotente y dominio
  estructurado 60/40 aislado del progreso legacy (9 hallazgos propios corregidos). 🏛️ Claude auditó
  como IA distinta: verificó timers server-side, intentos transaccionales por-recurso, aislamiento por
  scope+flag, reuso del parser de Fase 4, protección de historial (409) y gating de cobertura — **sin
  errores que corregir**. **CI Linux verde (510 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#83** a `main` (`5063113`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 6 (PDF).**
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

- 🔨 **Plataforma de Conocimiento — Fases F4–F5 (medición, diferidas por D4)** (handoffs en
  `2-arquitectura/kb-f4…kb-f5`). F1, F2, **F3 y F6 (estructural) construidos** (rama
  `feat/grafo-conocimiento-f1`). Quedan, como migraciones **aditivas** cuando se decida medir:
  **F4** evaluación formal (reusa `answer_grading_service`/`evaluation_assembly_service` + generadores
  de D3 para ítems no vistos), **F5** estado (`StudentNodeState`) — que además habilita las partes con
  estado de F6 (✓/! y "siguiente recomendado"). Foco actual: **poblar banco/contenido** (pipeline
  NotebookLM→JSONL→`load_exercise_bank`).

- 📚 **Biblioteca de Conocimiento Estructurada** — `1-por-iniciar/biblioteca-conocimiento-estructurada.md`
  (PR #89). Estructura universal por conceptos, partiendo por **Matemática preuniversitaria**. 4 capas por
  recurso (teórico / banco estructurado / práctica aleatoria / evaluación), 6 ejes de clasificación de
  ejercicios, mapa de cobertura acordeón. Plan **F0–F6 con gates del 🧑**. **Bloqueado por:** el 🧑 debe
  entregar los **índices** de sus libros de matemática para arrancar la Fase 1 (esqueleto en
  `docs/conocimiento/matematica.yaml`).
- 🔨 **Guías interactivas — Fases 4–7** (epic `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`).
  Fases 1–3 ✅. Handoffs de arquitectura redactados en `2-arquitectura/`:
  **F4** parser respuesta directa en `3-construccion/` (🟢 Ready tras preflight,
  `seguridad:requiere-claude`),
  **F5** evaluaciones nivel/final ✅ (cerrada, PR #83), **F6** PDF ✅ (cerrada, PR #84 — print nativo),
  **F7** gate + piloto (🟡 construida por Claude, en `4-auditoria/`, esperando audit de Codex —
  **última fase**),
  **F7** migración legacy + gate + piloto (🟡). Construir **en orden**, una fase por rama, cada una con preflight de Codex.
- 🔨 **PWA básica** — `backlog/2-arquitectura/pwa-progressive-web-app.md`. Ready para Codex (preflight)
  → Antigravity (rama `feat/pwa-basica`). Manifest + SW conservador + offline + iconos; sin tocar CSP.
- ✅ **Estudio de banco de preguntas — CERRADO 🟢 y ARCHIVADO (2026-06-18).** Construido y desplegado
  (PRs #62–#67): generación IA, config por recurso, edición y runtime. Tarjeta movida a
  `6-finalizados/estudio-banco-preguntas.md`. (F4 multimodal sigue bloqueada por storage externo —
  fuera de alcance por ahora.)

## Últimas entregas
- 2026-06-28 — 🏛️ Claude + 🧑: **UI accordeón + introducción didáctica + pauta de contenido.**
  Campo `introduccion` en `NodeContent` (migración `0042`) + 15 textos nivel ~10 años en YAMLs.
  Sección "Ejemplos Verdadero/Falso" renombrada. Fix acordeón KaTeX (wrap con `<span>` para
  que `justify-content: space-between` no explote los spans de math). Pauta de autoría
  `docs/conocimiento/pauta-contenido.md` (YAML + JSONL + gamificación + checklist).
- 2026-06-27 (tarde) — 🏛️ Claude + 🧑: **Contenido ENTEROS_CONJUNTO estandarizado + banco GEN.**
  15 YAMLs con 4 ejemplos Sí/No + 5 errores_frecuentes + estado publicado. 150 ejercicios nuevos
  en 3 archivos JSONL (`-banco-gen-1/2/3.jsonl`): 3 CONC + 1 REC + 3 PROC + 3 PAES por recurso.
  Fixes `generate_node_summaries`: encoding Windows, Gemini multi-part parsing, rate-limit resilience.
  Resúmenes pendientes de regenerar (cuota Gemini agotada).
- 2026-06-27 — 🏛️ Claude + 🧑: **F1–F3 + F6 CERRADAS — PR #102 squash-merge a `main` (rama `feat/grafo-conocimiento-f1`).**
  UI rediseñada: breadcrumb plegable, objetivo card, ejemplos interactivos (V/F/Sí-No), errores como
  preguntas conceptuales, banco con tarjetas+sombra. Ejercicios de clasificación (formato `matching`).
  Política **autopublicado inmediato** en `load_exercise_bank`. Contenido: 14 NodeContent + ejercicios
  ENTEROS_CONJUNTO + clasificación. Tests actualizados. Tarjetas en `6-finalizados/`.
- 2026-06-27 — 🏛️ Claude + 🧑: **F3 — estructura pedagógica por ítems (`ItemGroup` + `NodeExercise` + pipeline JSONL) — rama `feat/grafo-conocimiento-f1`.**
  Decisiones **D2/D3/D4** ratificadas en la arquitectura (§8). Modelos nuevos **aditivos** anclados a
  `KnowledgeNode` (Sistema A intacto): `ItemGroup` (7 grupos estándar) + `NodeExercise` (banco único,
  `kind=item|template` para generadores futuros), migración `0039`, admin, comando idempotente
  `load_exercise_bank` (JSONL NotebookLM→Claude; **nunca autopublica**; no degrada publicaciones
  manuales), sección "Practica por ítems" (acordeón + toggle solución + KaTeX), prompts en
  `docs/conocimiento/pipeline/`. Piloto Naturales (4 ejercicios) verificado en navegador. 20 tests
  nuevos. Tarjeta F3 → `4-auditoria/`.
- 2026-06-27 — 🏛️ Claude: **F6 (estructural) — prerrequisitos DAG + "Antes de empezar" — misma rama.**
  Comando `load_prerequisites` (YAML→`NodePrerequisite`, valida aciclicidad con `graphlib`, aborta sin
  escribir si hay ciclo, idempotente), sección informativa "Antes de empezar" en la página
  (`_prereqs.html`, enlaces a prerrequisitos publicados, nunca bloquea), DAG piloto `num-enteros.yaml`,
  timestamps en `NodeContent` (mig. `0040`). 13 tests. Estado por alumno (✓/!) y "siguiente
  recomendado" diferidos a F5. Verificado en navegador. Tarjeta F6 a `4-auditoria/`.
- 2026-06-26 — 🏛️ Claude + 🧑: **F2 construido — `NodeContent`/`NodeMedia` + app `learn` + `/aprender/` — rama `feat/grafo-conocimiento-f1`.**
  Modelos con migración `0038`, app `apps/learn/` con 6 rutas jerárquicas, 3 templates (home/list/detail),
  KaTeX por herencia de `base.html`, comando `load_node_content` idempotente (actualiza `NodeMedia` si
  YAML incluye clave `media:`), admin inlines, YAML ejemplo piloto. 22 tests nuevos. **554/554 verde.**
  Tarjeta F2 movida a `4-auditoria/`.
- 2026-06-26 — 🏛️ Claude + 🧑: **Arquitectura de plataforma (6 capas) + F1 construido — rama `feat/grafo-conocimiento-f1`.**
  Rediseño en 6 capas (banco≠evaluación; estado solo-rendimiento; asignatura como nodo raíz para
  Física/Química a futuro). Tarjetas F1–F6. **F1 construido y verde:** `KnowledgeNode`/`NodePrerequisite`,
  `import_knowledge_tree` idempotente (2208 nodos importados, 13 legacy omitidos), admin, migración `0037`,
  8 tests. Detalle en `reportes-sesion/2026-06-26.md`. **Siguiente: F2 (contenido + páginas, piloto Números Enteros).**
- 2026-06-25 — 🏛️ Claude + 🧑: **Biblioteca de Conocimiento — esqueleto YAML completo (ejes 01–05) — PR #99 abierto.**
  Eje 05 PROBABILIDAD Y ESTADÍSTICA (7 bloques 05.01–05.07), Eje 02 ampliado (02.06 Sucesiones),
  Eje 03 completado (03.11–03.15), Eje 04 ampliado (04.12–04.13). Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Total: ~700 recursos en 37 bloques, 5 ejes.
- 2026-06-25 — 🏛️ Claude + 🧑: **Eje 04 GEOMETRÍA completo — PR #98 en auto-merge.**
  11 bloques YAML atómicos (04.01–04.11), ~382 recursos, 55 temas. Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Conflict `TRIANGULOS_NOTABLES` resuelto
  con sufijo `_METRICA` en 04.04. Prompts para eje 05 PROBABILIDAD Y ESTADÍSTICA entregados.
- 2026-06-23 (tarde) — 🏛️ Claude + 🧑: **Bugfixes operativos de guías + proyecto nuevo.**
  (1) **PR #87** `gunicorn --timeout 120` + truncar guía en extracción de ítems: arregla el
  `SystemExit: 1` (worker abortado a los 30 s en la llamada síncrona a Gemini; detectado por Sentry
  `PYTHON-DJANGO-K`). **⚠️ El Custom Start Command de Railway sobrescribe los archivos del repo →
  el 🧑 debe agregar `--timeout 120 --workers 3` en el dashboard.** (2) **PR #88** N+1 en
  `/asignaturas/` (30→3 queries; `SubjectListView` con `select_related`/`prefetch_related` + agrupado
  en memoria). (3) Diagnóstico de lentitud del sitio: **no era el código** sino **1 worker de gunicorn**
  saturado por los clics de extracción que colgaban el worker → recomendado `WEB_CONCURRENCY=3`.
  (4) **PR #89** tarjeta de backlog del proyecto **Biblioteca de Conocimiento Estructurada**.
  Tracing de Sentry activado temporal (`SENTRY_TRACES_SAMPLE_RATE=1.0`, **revertir a 0**).
- 2026-06-23 — 🏛️ Claude: **Re-auditoría profunda del épico (F1–F7) + correcciones 🟢.**
  Doc en `docs/auditorias/2026-06-23-auditoria-epico-guias-interactivas.md`. F1–F6 sólidas. 5 hallazgos
  en F7 (Media/Baja, sin afectar datos), todos corregidos: `merge_items`/`edit_practice_quota` no
  funcionaban en staging (guard `enabled`→`editable`); un tema legacy no podía entrar a staging desde
  la UI (selector propio con todos los temas activos); `redirect` no importado en `item_review.py`
  (bug latente, NameError en ruta no-HTMX); gate contaba banco visible sin filtrar por la guía pública.
  13 tests F7 (de 9). Sin migraciones. Rama `fix/guias-fase7-auditoria`.
- 2026-06-23 — 🏛️ Claude: **Fase 7 (gate + piloto) PREFLIGHT + CONSTRUIDA 🟡 — esperando auditor distinto.**
  Modelo de coexistencia (no se toca el legacy). `Topic.structured_bank_staging` (mig. aditiva `0036`)
  + `structured_bank_editable` para preparar con el flag apagado; gate solo-lectura que reusa los
  ensambladores; activación admin gobernada por el gate + rollback. 9 tests F7. Rama
  `feat/guias-fase7-gate-piloto`; `seguridad:requiere-claude`. Audita 🧩 Codex (IA distinta al builder).
- 2026-06-23 — 🏛️ Claude: **Fase 6 (PDF) AUDITADA Y CERRADA 🟢 — merge de PR #84 a `main`.**
  Auditor distinto al builder (Codex). Fase solo-front: verificado print nativo (sin JS/deps nuevas,
  CSP intacta), el fix del bug de texto invisible (`!important` vence color inline), portada solo-print
  con a11y correcta, solucionario único consolidado y saltos de página. Test fija la decisión
  (`assertNotContains("html2pdf")`). CI Linux verde (511 OK, 1 skip), sin migraciones. **Sin errores.**
- 2026-06-23 — 🏛️ Claude: **Preflight Fase 6 (PDF) RESUELTO 🟢 — Ready para 🔨 Antigravity.**
  Decisión del 🧑: **print nativo** (`window.print()` + `@media print`), NO html2pdf.js (riesgo
  `unsafe-eval`/CSP, rasterización del tema oscuro, ~1 MB JS). Realidad encontrada: el
  `learning-guide-print.css` está **obsoleto** (apunta a clases inexistentes), `header{display:none}`
  **oculta logo+título** (no hay portada) y las clases Bootstrap/inline dejan **texto invisible** en
  papel. Alcance afinado: reescribir el print CSS contra el markup real, portada solo-print, forzar
  texto negro, resolver doble solucionario, relabelar botón. **Sin migraciones** (front).
  Tarjeta en `backlog/3-construccion/`; rama `feat/guias-fase6-pdf`.
- 2026-06-23 — 🏛️ Claude: **Fase 5 AUDITADA Y CERRADA 🟢 — merge de PR #83 a `main`.**
  Auditor distinto al builder (Codex). Verificadas las invariantes sensibles: timers 100% server-side,
  consumo de intento transaccional y **por-recurso** (no global), aislamiento `scope+flag`, reuso del
  parser seguro de Fase 4, **protección de historial** (409 al editar preguntas ya usadas; pools solo se
  archivan), ownership/CSRF, guards anti-DoS del ensamblador y gating de cobertura. Los 9 hallazgos del
  self-audit de Codex están corregidos; **no encontré P0/P1 nuevos**. CI Linux verde (510 OK, 1 skip),
  sin migraciones. `audit:aprobado` aplicado.
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
