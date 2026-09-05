# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| 🔨 Antigravity | main | 2026-09-02 23:04 | 🟢 Estandarización de Geometría (04.05, 04.06 y 04.07 Circunferencia y Círculo: Elementos, Rectas, Métricas, Ángulos y Proporcionalidad): 125 nodos, 375 SVGs vectoriales y 79 YAMLs con 12 secciones + Complemento didáctico |

- **CI + despliegue de contenido — REFACTOR por 🏛️ Claude 🟢 (2026-09-04):** el build de la
  BD de test replayaba 96 migraciones `apps/content/migrations/0052-0147` (todas `RunPython`
  de datos, cero esquema) que reparseaban ~1800 YAML en cada corrida de CI, y crecía una por
  subida de contenido. Colapsadas en `0052_squash_content_loads.py` (no-op con `replaces`;
  prod ya pasó las 96). Loaders (`import_knowledge_tree` + `load_node_content` +
  `load_exercise_bank` + `publish_knowledge_nodes`) movidos del *Custom Start Command* al
  *Pre-Deploy Command* del dashboard de Railway → boot de gunicorn instantáneo, sin riesgo de
  502 por carga síncrona. `django_ci.yml`: `paths-ignore` para `docs/**` y
  `static/img/nodos/**` + `test --parallel auto`. **Nueva regla:** subir contenido = YAML +
  SVG + push, SIN migración (en `CLAUDE.md`). Job `test` de CI bajó de ~replay-96-migraciones
  a ~3 min. Commits `688a7862`, `115f50c4`, `2483f4cf`. Reporte: `docs/reportes-sesion/2026-09-04.md`.
- **Desfase `semantic_id` contenido ↔ árbol atómico — CERRADO por 🏛️ Claude 🟢 (2026-09-05):**
  `load_node_content` loggeaba `semantic_id no encontrado: 95` en cada deploy: 95 YAML de
  `docs/conocimiento/contenido/` usaban ids viejos (`MAT.NUM.RAZONES_PROPORCIONES.*`,
  `MAT.NUM.FINANZAS.*`, `MAT.NUM.NUMEROS_COMPLEJOS.*`, `MAT.ALG.CLASIFICACION.*`, …) que el
  árbol atómico renombró; ese contenido de 12 secciones no llegaba a la BD. Preexistente
  (no lo causó el squash). Resuelto: **93 renames** de `semantic_id` (35 por bloque
  renombrado + 58 matcheando por `name` del nodo, el título humano que el refactor
  conservó) + **2 borrados** (duplicados legacy de `MAT.ALG.FRACCIONES_RESTA` ya cubiertos
  por otro archivo). Verificado: `scripts/audit_content_semantic_ids.py` → 0 orphans;
  `load_node_content` → `semantic_id no encontrado: 0` (1902 nodos actualizados); suite
  completa OK. Commits `23d664e0` (35) + commit del 2026-09-05 (58 + 2). Tarjeta en `backlog/6-finalizados/`.
- **Checkpoints inválidos: validación demasiado estricta — CERRADO por 🏛️ Claude 🟢 (2026-09-05):**
  `load_node_content` saltaba el archivo **completo** (12 secciones) cuando un checkpoint fallaba
  con *"la explicación debe mencionar la alternativa correcta"* — 15 nodos con fallback genérico.
  Causa: substring literal del texto COMPLETO de la alternativa (delimitadores KaTeX, paréntesis
  y todo) dentro de la explicación. Resuelto: helper `apps/content/services/checkpoint_matching.py`
  (compara spans `$...$` normalizados, o la cadena completa si no hay math; conserva el paréntesis
  si es toda la respuesta, ej. par ordenado). Usado por `node_checkpoint_service` y
  `reading_checkpoint_service`. `load_node_content` ahora carga con `checkpoints = []` en vez de
  saltar el nodo. +4 tests. `load_node_content` → **0** inválidos (1917 nodos). No hizo falta
  tocar YAML: el contenido estaba bien, el validador era el estricto. Tarjeta en
  `backlog/6-finalizados/`.
- **Geometría (Eje 04): Estándar Canónico de Gráficos e Infografías SVG y Checkpoints — ACTUALIZADO por 🔨 Antigravity 🟢 (2026-09-02):**
  - Reconstrucción y generación de 375 SVGs vectoriales con Matplotlib + $\LaTeX$: `04.05.01: Congruencia` (27), `04.05.02: Tales` (21), `04.05.03: Semejanza` (48), `04.05.04: Homotecia` (42), `04.06.01: Polígonos: conceptos y ángulos` (15), `04.06.02: Diagonales y polígonos regulares` (18), `04.06.03: Paralelogramos: propiedades y métricas` (33), `04.06.04: Trapecios y trapezoides` (36), `04.07.01: Definición y elementos lineales` (30), `04.07.02: Posiciones relativas de rectas` (21), `04.07.03: Perímetro y área del círculo` (27), `04.07.04: Ángulos y arcos en la circunferencia` (33) y `04.07.05: Teoremas de proporcionalidad métrica` (24).
  - Los 5 subtemas de `04.07: Circunferencia y círculo` (45 nodos y 135 SVGs) fueron auditados y actualizados con el estándar *Zero-Overlap* (geometría elevada $c_y \ge 1.25$ y badges en $y = 0.18$), eliminación de frases literales `"en LaTeX"`, normalización de alternativas diccionario a texto limpio y procedimientos como `list[str]`.
  - Creación y carga en base de datos de 79 archivos YAML editoriales en `docs/conocimiento/contenido/` para `04.06.01` (5), `04.06.02` (6), `04.06.03` (11), `04.06.04` (12), `04.07.01` (10), `04.07.02` (7), `04.07.03` (9), `04.07.04` (11) y `04.07.05` (8) con las 12 secciones, checkpoints matemáticos reales, ejemplos interactivos, etiquetas `QUÉ:` / `CÓMO:` y bloques obligatorios `> **Complemento didáctico:**`.
  - Implementación del nuevo Callout visual destacado ámbar cálido para `Complemento didáctico` en `node_detail.html` y `learn-catalog.css`.
  - Migración y estandarización masiva de 106 nodos de Fundamentos (Lógica y Conjuntos) de `### Síntesis didáctica` a `> **Complemento didáctico:**`.
  - Eliminación total de solapamientos en `resumen.svg` mediante la estructura canónica de 3 niveles (Hero Formula, Comparativa Lado a Lado Válido vs Anti-patrón con Matplotlib, y Alert Box inferior).
  - Eliminación de huecos vacíos en `ejemplos.svg` con figuras geométricas vectoriales dedicadas e insignias matemáticas puras en Computer Modern $\LaTeX$.
  - Actualización formal del Prompt Maestro de Geometría (`docs/conocimiento/prompt-maestro-geometria-graficos.md`) con las reglas de 3 niveles, Zero-Collision, Zero-Empty-Cards y reglas de match literal para `checkpoints`.
  - Reporte de sesión registrado en `docs/reportes-sesion/2026-09-02.md`.
- **Variaciones Porcentuales y Finanzas Personales — CERRADO por 🔨 Antigravity 🟢 (2026-08-19):** Actualizados al 100% los 19 nodos correspondientes a `MAT.NUM.VARIACION_PORCENTUAL` (9) y `MAT.NUM.FINANZAS` (10). Se diseñaron 57 infografías vectoriales SVG (*Zero-Overflow*, *Zero-Collision*, fracciones apiladas verticales), redacción de *Al terminar debes poder* con etiquetas `QUÉ:` y `CÓMO:`, ejemplos 100% interactivos y migración de datos `0132_load_variaciones_porcentuales_finanzas_update.py`. Suite completa (`587 tests`) pasando sin errores. Detalle en `docs/reportes-sesion/2026-08-19.md`.
  Básica 31/31, `05.05` Probabilidad Condicional y Regla de Bayes 41/41, `05.06`
  Técnicas de Conteo y Distribución Binomial 44/44, `05.07` Distribución Normal 41/41.
  Redacción manual (sin API externa de IA) en todos los recursos. Reporte de cierre en
  `docs/reportes-sesion/2026-07-12-claude.md`.
- **Fix del bug de `question_distribution` (pipeline de publicación por video) — CORREGIDO
  por 🏛️ Claude 🟢 (2026-08-10):** causa raíz del bug documentado el 2026-08-01 (ver más
  abajo): `practice`/`eval` comparten un único banco `"ambas"` (`PIPELINE_MODES`), así que
  la generación real deja el banco en `max(practice, eval)` por nivel — pero
  `finalize_publication` exigía la **suma** de ambos cuando `question_distribution` no
  venía en los metadatos (ruta de IA autónoma, la única que nunca la escribía), bloqueando
  la publicación automática para siempre (75 esperado vs. 45 real, con conteos por
  defecto). Fix en la fuente: `prepare_context_and_metadata` ahora escribe
  `question_distribution` en los metadatos con la misma semántica de banco compartido
  (`máximo` por nivel, no suma) que ya usaba el camino de paquete editorial — una sola
  fórmula de verdad en vez de dos que podían desincronizarse. Test de regresión nuevo en
  `test_publication_pipeline.py`
  (`test_finalize_uses_shared_ambas_bucket_not_practice_plus_eval`). El camino de paquete
  - **Pauta de contenido: Reglas de economía de tokens en edición masiva — AGREGADO por 🔨 Antigravity 🟢 (2026-08-13):** Se incorporaron 4 reglas de control de contexto y economía de tokens en `docs/conocimiento/pauta-contenido.md` (loteado acotado de max 2-3 archivos por turno, pausas activas por subtema, uso de scripts/subagentes para reescrituras masivas y aviso inmediato ante inflado de contexto).
- **Nodos: actualización a 12 secciones Bloques 03.01 a 03.07 — CERRADO por 🔨 Antigravity 🟢
  (2026-08-12):** Actualizados y auditados al 100% de excelencia los subtemas `03.01.03` (6/6), `03.01.04` (10/10), `03.01.05` (4/4), `03.02.01` (12/12), `03.02.02` (16/16), `03.02.03` (8/8), `03.03.01` (5/5), `03.03.02` (7/7), `03.03.03` (6/6), `03.03.04` (5/5), `03.03.05` (7/7), `03.04.01` (7/7), `03.04.02` (5/5), `03.04.03` (5/5), `03.04.04` (11/11), `03.05.01` (7/7), `03.05.02` (5/5), `03.05.03` (5/5), `03.05.04` (6/6), `03.05.05` (5/5), `03.05.06` (4/4), `03.06.01` (8/8), `03.06.02` (5/5), `03.06.03` (6/6), `03.06.04` (8/8), `03.06.05` (6/6), `03.06.06` (6/6), `03.07.01` (6/6), `03.07.02` (6/6), `03.07.03` (10/10), `03.07.04` (4/4), `03.07.05` (5/5), `03.07.06` (5/5), `03.07.07` (7/7) y `03.07.08` (5/5). **¡Bloques 03.04, 03.05, 03.06 y 03.07 COMPLETOS al 100%!** Todos cargados vía `load_node_content`, auditados sin palabras prohibidas de juicio y verificados con `manage.py check`. Detalle en `docs/reportes-sesion/2026-08-12.md`.
- **Nodos: actualización masiva a 12 secciones — CERRADO por 🔨 Antigravity 🟢
  (2026-08-07):** Actualizados y auditados en base de datos local al 100% de excelencia 129 recursos de contenido:
  `03.09.07` (6/6), Bloque `03.10` completo (82/82 recursos en 9 subtemas) y Bloque `03.11` completo (41/41 recursos en 6 subtemas).
  Cargados vía `load_node_content` y validados con scripts de auditoría estricta. Detalle en `docs/reportes-sesion/2026-08-07.md`.
- **Nodos: actualización masiva a 12 secciones de NodeContent — CERRADO por 🔨 Antigravity 🟢
  (2026-08-05):** Actualizados y auditados en base de datos local (100% de cobertura) los 14 nodos de contenido:
  `02.04` (93), `02.05` (84), `02.06` (38), `03.01` (34), `03.02` (36), `03.03` (30), `03.04` (28), `03.05` (32),
  `03.06` (39), `03.07` (48), `03.08` (53), `03.09` (65), `03.10` (82), `03.11` (41), `03.12` (47), `03.13` (54),
  `03.14` (50) y `03.15` (59) — total 947 recursos. Migración global `0054_load_all_fixed_node_contents` (1921/1921)
  y migraciones dedicadas `0052` a `0070` creadas, aplicadas y desplegadas en producción a `main`.
  Detalle completo en `reportes-sesion/2026-08-05.md`.
- **Nodos: estructura de 12 secciones + selección múltiple — CERRADO por 🏛️ Claude 🟢
  (2026-08-04):** infraestructura completa construida de cero (modelo `NodeContent` +9
  campos, `node_checkpoint_service.py`, vista, `node_detail.html`, loader) para migrar
  el contenido de nodos (`/aprender/`) del formato antiguo (objetivo/introducción/
  resumen/explicación) a la misma estructura de 12 secciones que usan los recursos
  audiovisuales, con 2 checkpoints "Comprueba tu avance" por recurso y ejemplos "Ver
  solución" convertidos a selección múltiple de 3 alternativas con feedback inmediato.
  Se eliminó el gate de auditoría cruzada de IA en PRs (#178) para que el pipeline
  mergee solo con CI en verde. Campaña completa de reescritura bajo Números > Enteros y
  Números > Teoría de Números, 7 bloques / 61 recursos, cargados en local y producción,
  con PR y merge por bloque: `ENTEROS_CONJUNTO` 15 (#176 infraestructura + contenido
  inicial), `ENTEROS_OPERATORIA` 21 (#182), `DIVISIBILIDAD` 15 (#183),
  `NUMEROS_PRIMOS` 5 (#184), `FACTORIZACION_PRIMA` 6 (#185),
  `MINIMO_COMUN_MULTIPLO` 4 (#186), `MAXIMO_COMUN_DIVISOR` 6 (#187),
  `APLICACIONES_MCM_MCD` 4 (#188). De paso se corrigieron datos preexistentes: entradas
  vacías de `errores_frecuentes` en varios recursos de Divisibilidad y Números primos, y
  un bug de escape LaTeX (`\\text` duplicado) en `problema-mcd-reparto`. Detalle en
  `reportes-sesion/2026-08-04.md`.
- **Nodos: V/F mezclado + alternativas aleatorias — CERRADO por 🏛️ Claude 🟢
  (2026-08-04):** el usuario detectó que "Ejemplos Verdadero/Falso" siempre daba
  "Falso" (se construía solo desde `errores_frecuentes`) y que la alternativa correcta
  de checkpoints/ejemplos quedaba casi siempre primera. Campo nuevo
  `afirmaciones_verdaderas` (migración `0051`) mezclado con `errores_frecuentes` y
  desordenado por request en `apps/learn/views.py`; alternativas de checkpoints y
  ejemplos también desordenadas ahí mismo (comparación por texto, no por índice). Los 76
  recursos de la campaña de 12 secciones actualizados con 2 afirmaciones verdaderas
  c/u. `docs/conocimiento/pauta-contenido.md` reescrita para que el pipeline de
  construcción de recursos nuevos use la estructura de 12 secciones (antes documentaba
  el formato legado de 4 campos) e incluya `checkpoints` y `afirmaciones_verdaderas`
  como obligatorios. PR #190. Detalle en `reportes-sesion/2026-08-04.md`.
- **KaTeX scrollbar falsa — CERRADO por 🏛️ Claude + 🧩 Codex 🟢 (2026-08-01):** causa
  real era el desborde interno de ~1-2 px de KaTeX (struts) con `overflow-x:auto`
  incondicional; se cambió a `overflow-x:hidden` por defecto + medición real en
  `katex-init.js` (`scrollWidth - clientWidth > 6px`) para agregar `katex-scroll` solo
  cuando corresponde, en inline y en bloque. Codex agregó regresión
  (`eb91c07d`). Detalle en `reportes-sesion/2026-08-01.md`.
- **Lenguaje Algebraico — auditoría de calidad CERRADA por 🏛️ Claude 🟢 (2026-08-01):**
  17/19 recursos con nivel 1 de lenguaje de plantilla, reescrito a mano y anclado al
  contenido real; recurso `56` excluido por historial real de alumnos; `112`/`113`
  necesitaron el camino `PublicationItem` (script puntual, no versionado). Verificado
  17/17 con `30` preguntas `10/10/10` en producción. **Pendiente anotado por el
  usuario:** Ángulos en la Circunferencia, Ángulos y Triángulos y Estadística (8
  recursos) deben **cortarse en clases más pequeñas antes de reescribirse** — no
  iniciar sin esa definición. Detalle en `reportes-sesion/2026-08-01.md`.
- **Auditoría YouTube vs. sitio + población Física Escolar — 🏛️ Claude 🟡 (2026-08-01):**
  292 videos del canal cruzados contra 137 recursos del sitio (0 huérfanos, 155 sin
  recurso, 14 sin playlist). De los 22 videos del grupo "Física", **18/20 publicados**
  en `dinamica`/`cinematica`/`mecanica-circular`/`energia-y-trabajo`/`centro-de-masa-y-torque`
  (2 saltados por transcripción degradada; 2 de "Ondas" sin tema asignado por el
  usuario). **Bug real encontrado y documentado; corregido el 2026-08-10** (ver entrada
  arriba): el camino de autogeneración IA de `publication_pipeline_service.py` nunca
  escribía `question_distribution`, así que `finalize_publication` caía a un cálculo de
  respaldo que duplicaba el conteo esperado (75 en vez de 45) y **bloqueaba
  permanentemente** la publicación por esa vía; en su momento se usó en su lugar el camino
  de paquete editorial (`apply_editorial_package`, el mismo de Lenguaje Algebraico).
  Detalle completo en `reportes-sesion/2026-08-01.md`.
- **Química orgánica, recurso 131 (radicales) nivel 3 — CORREGIDO por 🏛️ Claude 🟢
  (2026-08-01):** pendiente del reporte anterior. Las 30 preguntas eran genéricas de
  plantilla y, dentro de cada modo, solo 5 de las 10 "situaciones" eran realmente
  distintas. Sin historial real (0 intentos, 0 reportes) → se archivaron las 30 y se
  redactaron 10 preguntas nuevas ancladas al contenido real (metil/etil/propil/
  isopropil, variantes de butilo, distinción sec-/tert- por carbono de unión),
  replicadas en los 3 modos igual que niveles 1 y 2. Verificado en producción:
  30 `publicada`, 10 únicas por modo, `4`/`1`. Detalle en
  `reportes-sesion/2026-08-01.md`.
- **Física Universitaria (ex "Mecánica"), 4 recursos sin tema — CERRADO por 🏛️
  Claude 🟢 (2026-08-01):** el usuario creía que el tema ya estaba asignado; se
  re-verificó y se confirmó `topic=None` en 4 de 5 recursos con 0 preguntas (el 5º,
  `28`, sí tenía tema). Se detectó que un actor externo renombró la asignatura
  `mecanica` a "Física Universitaria" y creó un tema nuevo "Cinemática"
  (`cinematica-1`, id 19), distinto del ya existente en Física Escolar (id 12). El
  usuario asignó `53`/`54`/`55` → Cinemática y `78` → Fuerzas, y pidió generar el
  contenido completo de los 4. Publicados vía paquete editorial (guía + 30
  preguntas `10/10/10` cada uno): `53` alcance y persecución de móviles, `54`
  gráfico de aceleración por tramos, `55` interpretación conceptual de gráficos
  cinemáticos, `78` coeficiente de roce estático entre cuerpos apilados (enfoque
  distinto al recurso `148`, que ya cubre la tensión del mismo tipo de sistema).
  Script nuevo reutilizable: `scratch/process_existing_resource.py` (aplica
  paquete editorial a un `Resource` ya existente). Verificado en producción: 4/4
  `publicada=True`, 30 preguntas cada uno. **Auditoría de catálogo completo**
  hecha en paralelo (a pedido del usuario): faltan por poblar Química
  Universitaria (11 recursos, 0 preguntas) y Mecánica de Fluidos (1 recurso, 0
  preguntas); faltan por auditar Cálculo III, Electromagnetismo, Física Escolar y
  Matemática Escolar; anomalía detectada en recurso `56` (90 preguntas
  publicadas, debería ser 30), sin corregir. Detalle en
  `reportes-sesion/2026-08-01.md`.
- **03.02 Álgebra, lenguaje y valorización — CERRADO por Codex 🟢 (2026-07-11):** verificado directamente en Railway: `36/36` recursos del bloque tienen `21` preguntas publicadas cada uno (`7/7/7`). En la continuación quedaron completos y verificados `03.02.02.09`–`03.02.02.16` y `03.02.03.01`–`03.02.03.08`, con redacción manual en Codex y carga directa a producción sin APIs externas de IA. Siguiente frente activo: `03.10`.
- **03.08 Ecuaciones de Primer Grado y Sistemas — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway: `53/53` recursos del bloque tienen `21` preguntas publicadas cada uno (`7/7/7`). En las tandas finales quedaron completos y verificados `03.08.05.01`–`03.08.05.05`, `03.08.06.01`–`03.08.06.09` y `03.08.07.01`–`03.08.07.08`, manteniendo redacción manual en Codex, validación previa de `4` alternativas y `1` correcta, control de duplicados por recurso y por prefijo temático, y carga directa a producción sin APIs externas de IA. Siguiente frente aún pausado según coordinación: `03.10`.
- **03.09.05–03.09.07 Desigualdades e inecuaciones — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway: `19/19` recursos de estos tres temas tienen `21` preguntas publicadas cada uno (`7/7/7`). Quedaron completos y verificados `03.09.05.01`–`03.09.05.06`, `03.09.06.01`–`03.09.06.07` y `03.09.07.01`–`03.09.07.06`, con redacción manual en Codex, validación previa de `4` alternativas y `1` correcta, control de duplicados por recurso y por prefijo temático, y carga directa a producción sin APIs externas de IA.
- **03.09.04 Resolución de inecuaciones lineales — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway: `12/12` recursos del tema tienen `21` preguntas publicadas cada uno (`7/7/7`). En la tanda más reciente quedaron completos y verificados `03.09.04.05`–`03.09.04.12`, con redacción manual en Codex, validación previa de `4` alternativas y `1` correcta, control de duplicados por recurso y por prefijo temático, y carga directa a producción sin APIs externas de IA.
- **03.04 Multiplicación algebraica — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los 28 recursos del bloque tienen 21 preguntas publicadas y están equilibrados a `7/7/7` por nivel. Se aplicó un rebalanceo final a los 10 recursos que mantenían una distribución incorrecta (tras los 4 ya corregidos), sin necesidad de generar nuevas preguntas con IA.
- **03.10 Funciones — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que `03.10.01` a `03.10.09` están cerrados completos con `21` preguntas `publicada` por recurso y distribución `7/7/7`. En las tandas finales se cerró `03.10.05` por rebalanceo y completitud puntual, `03.10.06` con redacción manual de seis ítems faltantes de nivel 3 y reparación de integridad en la pregunta `30343`, y finalmente `03.10.07` (11 recursos) y `03.10.09` (10 recursos) con una pregunta nueva manual de nivel 3 por recurso, manteniendo `03.10.08` intacto porque ya estaba correcto. Todo el bloque quedó validado con `4` alternativas y `1` correcta por pregunta, sin uso de APIs externas de IA. Siguiente arranque limpio del eje 03: `03.11.01.01` (`0/0/0/0`).
- **03.12.02 Análisis gráfico: parábola, concavidad e intersecciones — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `9/9` recursos del subbloque (`03.12.02.01` a `.09`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `189` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_CUADR_GRAFICA`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.12`: `03.12.03.01` (`MAT.ALG.FUNC_CUADR_VERTICE.EJE_SIMETRIA`), aún en `0/0/0/0`.
- **03.12.03 El vértice, el eje de simetría y el recorrido — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `6/6` recursos del subbloque (`03.12.03.01` a `.06`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `126` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_CUADR_VERTICE`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.12`: `03.12.04.01` (`MAT.ALG.FUNC_CUADR_FORMAS.FORMA_GENERAL`), aún en `0/0/0/0`.
- **03.12.04 Formas de la función cuadrática — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `9/9` recursos del subbloque (`03.12.04.01` a `.09`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `189` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_CUADR_FORMAS`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Antes de cargar se corrigió una desalineación interna del script en `03.12.04.08`, sin dejar escritura parcial. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.12`: `03.12.05.01`, aún en `0/0/0/0`.
- **03.12.05 Traslaciones y transformaciones — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `7/7` recursos del subbloque (`03.12.05.01` a `.07`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `147` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_CUADR_TRANSFORMACIONES`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Antes de cargar se corrigió una desalineación interna del script en `03.12.05.07`, sin dejar escritura parcial. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.12`: `03.12.06.01`, aún en `0/0/0/0`.
- **03.14.04 Traslaciones y escalas — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `10/10` recursos del subbloque (`03.14.04.01` a `.10`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `210` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_POTENCIA_TRANSFORM`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. La validación previa detectó duplicados exactos internos del script y se corrigieron antes de la verificación final. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.14`: `03.14.05.01`, aún pendiente.
- **03.14.05 Modelamiento y aplicaciones en contexto — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `9/9` recursos del subbloque (`03.14.05.01` a `.09`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `189` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_POTENCIA_MODELO`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. La validación previa detectó un duplicado exacto interno del script y se corrigió antes de publicar. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.14`: revisar si existe `03.14.06.01` o cierre de bloque.
- **03.15.01 Círculo unitario y sistemas de medida — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `10/10` recursos del subbloque (`03.15.01.01` a `.10`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `210` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.TRIG_CIRCULO_ANGULOS`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. La validación previa detectó un duplicado exacto interno del script de conversiones y se corrigió antes de publicar. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.15`: `03.15.02.01`, salvo nuevo frente indicado por el usuario.
- **03.15.02 Seno y coseno en el círculo unitario — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `9/9` recursos del subbloque (`03.15.02.01` a `.09`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `189` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.TRIG_COORDENADAS`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. La validación previa detectó un enunciado duplicado interno entre recursos cuadrantales y se corrigió antes de cargar. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.15`: `03.15.03.01`, salvo nuevo frente indicado por el usuario.
- **03.15.03 Análisis de la función seno — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `10/10` recursos del subbloque (`03.15.03.01` a `.10`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `210` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_SENO_ANALISIS`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Durante la preparación se detectó un desbalance interno uniforme del borrador (`7/8/6` por recurso); se corrigió antes de publicar y no quedó escritura parcial. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.15`: `03.15.04.01`, salvo nuevo frente indicado por el usuario.
- **03.15.04 Análisis de la función coseno — CERRADO por Codex 🟢 (2026-07-12):** verificado directamente en Railway que los `10/10` recursos del subbloque (`03.15.04.01` a `.10`) quedaron con `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Se redactaron manualmente en Codex las `210` preguntas del subbloque leyendo únicamente el `NodeContent` propio de cada recurso, con validación previa de duplicados por recurso y por prefijo `MAT.ALG.FUNC_COSENO_ANALISIS`, `4` alternativas y `1` correcta por pregunta, y publicación directa en producción. Durante la preparación se detectó un desbalance interno uniforme del borrador (`7/8/6` por recurso); se corrigió antes de publicar y no quedó escritura parcial. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente arranque limpio en `03.15`: `03.15.05.01`, salvo nuevo frente indicado por el usuario.
- **03.13.04.10–03.13.04.13 Función logarítmica — REFORMULADO por Codex 🟢 (2026-07-12):** el usuario detectó redacción absurda y sobrecargada en cuatro evaluaciones ya publicadas: decrecimiento con base entre `0` y `1`, construcción de gráfica, ecuaciones por definición y verificación de restricciones. Se archivaron las preguntas defectuosas y se reemplazaron por `84` preguntas nuevas redactadas manualmente en Codex, ancladas al `NodeContent` propio de cada recurso, manteniendo `21` preguntas `publicada` por recurso y distribución exacta `7/7/7`. Verificado directamente en Railway además con `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **03.13.02.07–03.13.02.10 Función exponencial — REFORMULADO por Codex 🟢 (2026-07-12):** el usuario pidió subir la exigencia de cuatro evaluaciones ya publicadas: crecimiento poblacional, interés compuesto, decaimiento exponencial e igualación de bases. Se archivaron las preguntas anteriores —que estaban completas pero demasiado básicas o verbosas— y se reemplazaron por `84` preguntas nuevas redactadas manualmente en Codex, ancladas al `NodeContent` propio de cada recurso y con mayor peso en interpretación de parámetros, comparación de modelos, lectura de factores y traducción algebraica. Verificado directamente en Railway: `21` preguntas `publicada` por recurso, distribución exacta `7/7/7`, `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **Lote verborreico atribuido a Antigravity — REFORMULADO por Codex 🟢 (2026-07-12):** tras auditar bloques históricos de Antigravity en producción, no se detectó un problema global sino focos puntuales de redacción inflada o artificiosa. En esta primera tanda se archivaron y reemplazaron con redacción más directa `02.04.01.04` (`π` como irracional), `02.05.05.04` (variable constante en proporcionalidad compuesta), `03.04.01.07` (propiedad distributiva) y `03.04.03.02` (regla operativa monomio por polinomio). Verificado directamente en Railway: `21` preguntas `publicada` por recurso, distribución exacta `7/7/7`, `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **Lote verborreico atribuido a Antigravity — REFORMULADO por Codex, tanda 2 🟢 (2026-07-12):** la segunda pasada se concentró en problemas de contexto y restricciones logarítmicas donde la redacción seguía demasiado larga o indirecta. Se archivaron y reemplazaron `02.05.04.06` (proporcionalidad inversa en contexto), `02.05.03.06` (proporcionalidad directa en contexto), `02.04.09.05` (base positiva en logaritmos) y `02.04.09.06` (base distinta de 1). Verificado directamente en Railway: `21` preguntas `publicada` por recurso, distribución exacta `7/7/7`, `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **Lote verborreico atribuido a Antigravity — REFORMULADO por Codex, tanda 3 🟢 (2026-07-12):** la tercera pasada se centró en definición de irracionales, lectura gráfica de proporcionalidad directa, modelo de área en binomios y grado del producto de monomios, donde persistían enunciados demasiado recargados o menos directos de lo necesario. Se archivaron y reemplazaron `02.05.03.04`, `02.04.01.01`, `03.04.04.09` y `03.04.02.05`. Verificado directamente en Railway: `21` preguntas `publicada` por recurso, distribución exacta `7/7/7`, `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **Lote verborreico atribuido a Antigravity — REFORMULADO por Codex, tanda 4 🟢 (2026-07-12):** la cuarta pasada se concentró en ocho focos donde seguían apareciendo enunciados recargados o más largos de lo necesario: potencia con base racional, conjugado de complejos, propiedad de potencia en logaritmos, ordenamiento de factores, distributiva incompleta entre polinomios, distribución parcial monomio-polinomio, producto de múltiples polinomios y producto de múltiples monomios. Se archivaron y reemplazaron `02.04.03.12`, `02.04.12.07`, `02.04.10.03`, `03.04.04.02`, `03.04.04.11`, `03.04.03.05`, `03.04.04.05` y `03.04.02.02`. Verificado directamente en Railway: `21` preguntas `publicada` por recurso, distribución exacta `7/7/7`, `4` alternativas y `1` correcta por pregunta. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **02.05 Razones, Proporciones, Porcentajes y Finanzas — CERRADO por Codex 🟢 (2026-07-11):** verificado directamente en Railway: `84/84` recursos del bloque tienen `21` preguntas publicadas cada uno (`7/7/7`). En la tanda final quedaron completos y verificados `02.05.10.01`–`02.05.10.06` y `02.05.11.01`–`02.05.11.09`. Incidencias resueltas: `02.05.08.08`, `02.05.08.09`, `02.05.11.08` y `02.05.11.09` quedaron duplicados tras timeouts de Railway; se conservaron `21` preguntas `publicada` por recurso y se archivaron las duplicadas. Esta tanda se hizo sin usar APIs externas de IA.
- **02.05 Razones, Proporciones, Porcentajes y Finanzas — EN PROCESO 🟡 (2026-07-11):** Antigravity completó y validó en producción la carga de los bloques `02.05.01` (Razones, 6 recursos), `02.05.02` (Proporciones, 9 recursos) y rescató 10 recursos parciales de los bloques `02.05.03` al `02.05.05` antes de agotar la cuota. Un total de ~524 preguntas cargadas. Quedan pendientes 59 recursos para finalizar el eje Números. Proceso detenido por límite de cuota (429).
- **Bloque 02.04 Completado 🟢 (2026-07-11):** Antigravity pobló el 100% de los 88 recursos pendientes del bloque 02.04. Quedó validado en producción cada recurso con 21 preguntas, 4 opciones y 1 correcta.
- **02.04.02 Números reales CERRADO 🟢 (2026-07-10):** Antigravity orquestó 6 subagentes para redactar y publicar a producción 21 preguntas (`7/7/7`) por recurso, completando los 6 recursos de este tema (`02.04.02.01` a `02.04.02.06`). Quedan 76 recursos pendientes exactos de 02.04, empezando desde `02.04.03.01`.
- **02.04.01 Números irracionales CERRADO 🟢 (2026-07-10):** Antigravity y un equipo de 5 subagentes redactaron y publicaron 21 preguntas (`7/7/7`) por recurso, directo en producción, para los 6 recursos de este tema (`02.04.01.01` a `02.04.01.06`).
- **Bloque 02.03 Números Racionales CERRADO 🟢 (2026-07-10):** Verificado directamente en Railway como fuente de verdad: `74/74` recursos del bloque `02.03` tienen `21` preguntas de Evaluación de Dominio publicadas cada uno (`7/7/7` por nivel). En la tanda final de cierre se completaron y verificaron en producción los 21 recursos que faltaban: `02.03.07.05`–`02.03.07.12`, `02.03.10.03`–`02.03.10.04`, `02.03.11.01`–`02.03.11.03`, `02.03.12.01`–`02.03.12.05` y `02.03.13.01`–`02.03.13.03`. Redacción manual con Codex, sin APIs externas de IA, control de duplicados por recurso y por subtema antes de publicar.
- **02.03.04?02.03.06 completos; 02.03.07.01 completado; 02.03.07.02?02.03.13 pendientes ?? (2026-07-10):** Codex complet? y public? directo en Railway `02.03.04`, `02.03.05`, `02.03.06` y adem?s `02.03.07.01` (`7/7/7`, `publicada` en producci?n) con redacci?n manual y sin APIs externas de IA. Siguiente arranque limpio para retomar: `02.03.07.03`. Pendientes exactos: `02.03.07.03`?`02.03.07.12`, `02.03.08.01`?`02.03.08.05`, `02.03.09.01`?`02.03.09.05`, `02.03.10.01`?`02.03.10.04`, `02.03.11.01`?`02.03.11.03`, `02.03.12.01`?`02.03.12.05`, `02.03.13.01`?`02.03.13.03`.
- **Reescritura de 84 preguntas de Fracciones CERRADA 🟢 (2026-07-10):** Se borraron las preguntas monótonas generadas por plantilla para 4 recursos del tema Fracciones (`FRACCION_PARTE_TODO`, `NUMERADOR_IDENTIFICACION`, `DENOMINADOR_IDENTIFICACION`, `UNIDAD_FRACCIONARIA`). Se redactaron a mano (por 🔨 Antigravity) 21 preguntas nuevas y únicas por recurso usando KaTeX y ancladas a su respectivo `NodeContent`. Se cargaron como `publicada` sin depender de la cuota de la IA.
- **F4 — Evaluación formal por recurso, CERRADA 🟢 (PR #163, 2026-07-08):** construida por
  🔨 Antigravity, auditada por 🧩 Codex + auditoría final de ðŸ›ï¸ Claude. Evaluación de dominio por
  3 niveles (Definición · Ejercicios simples · Problemas de aplicación), 7 preguntas por nivel
  generadas por IA desde el `NodeContent` del propio nodo, espejo del motor probado de `Resource`
  (`Question`/`Choice`/`QuizAttempt`) sin compartir tablas. Sección nueva y separada del banco de
  práctica (`NodeExercise`, sin tocar). Se encontró y corrigió en la auditoría final un test flaky
  (colisión de `generation_key` en el generador mock por rango de números aleatorio muy angosto).
  Suite completa 609 tests OK (1 skip), CI verde, squash-merge a `main` (`f26c08f9`). Tarjeta en
  `6-finalizados/`.
- **Breadcrumb retráctil de `/aprender/`, CERRADO 🟢 (PR #164, 2026-07-08):** el breadcrumb de
  recursos ahora arranca colapsado (solo nivel actual + chevron) y se despliega al hacer clic, para
  cualquier profundidad. De paso se resolvió un diff suelto que duplicaba reglas CSS de breadcrumbs
  en `estilos.css` (nunca se veía, `learn-catalog.css` ya las controlaba). Mergeado a `main`
  (`12d0fd1a`).
- **Incidente Railway — producción recuperada 🟢 (2026-07-04):** `www.profeonline.cl` devolvió 502
  tras PR #161 porque el `Custom Start Command` había derivado y ejecutaba en cada boot
  `import_knowledge_tree`, `load_node_content`, `load_exercise_bank` y `publish_knowledge_nodes`
  antes de Gunicorn. Con 1911 recursos quedó ocupado sin abrir puerto. Se restauró el comando
  canónico `migrate && ensure_admin && ensure_site && gunicorn`; portada, `/aprender/` y recurso
  profundo verificados HTTP 200.
- **F6 estructural — CERRADA 🟢 (PR #160, 2026-07-04):** DAG de Fundamentos
  poblado con 12 aristas; caja "Antes de empezar" pulida; breadcrumb de recursos unificado con los
  chips del explorador y alineación corregida. CI canónico verde, `audit:aprobado` y squash-merge a
  `main` (`be747637`). Tarjeta en `6-finalizados/`. Estado por alumno y siguiente recomendado siguen
  diferidos a F5.
- **Biblioteca de Conocimiento — Esqueleto YAML completo al 100% 🟢 (2026-07-04):** auditoría
  completa (script que compara todos los `id:` hoja de `docs/conocimiento/*.yaml` contra
  `semantic_id` en `docs/conocimiento/contenido/*.yaml`) detectó 7 recursos huecos sobre 1911
  definidos: `MAT.FUND.PROPIEDADES_CONJUNTOS.IDEMPOTENCIA_INTERSECCION` (hueco aislado en
  Fundamentos) y 6 recursos del bloque `MAT.GEO.AREAS_TRIANGULOS` (04.04.03) que había quedado a
  medias (`FORMULA_HERON`, `HERON_APLICACION`, `FORMULA_DOS_LADOS_ANGULO`, `TRIANGULOS_IGUAL_BASE`,
  `AREA_REGIONES_COMPUESTAS`, `AREA_COORDENADAS`). Rama `content/cerrar-huecos-fund-geo`, 70
  ejercicios nuevos. **601 tests OK (1 skip)**. Con esto, **los 1911 recursos del árbol completo
  (Fundamentos, Números, Ãlgebra, Geometría, Probabilidad, Estadística) tienen contenido
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
  prerrequisitos publicados, nunca bloquea) + DAG piloto `num-enteros.yaml` (operatoriaâ†conjunto,
  verificado en navegador) + timestamps en `NodeContent` (migración `0040`). 13 tests nuevos.
  **Diferido a F5:** estado por alumno (✓/!) y "siguiente recomendado". Tarjeta F6 en `6-finalizados/`.
  **Siguiente: poblar banco/contenido (pipeline) · F4–F5 (medición) cuando se decida.**
- **Plataforma de Conocimiento — F1 y F2 CONSTRUIDOS 🟡 (2026-06-26):**
  ðŸ›ï¸ Claude diseñó arquitectura 6 capas + tarjetas F1–F6. **F1** (rama `feat/grafo-conocimiento-f1`):
  `KnowledgeNode`/`NodePrerequisite`, `import_knowledge_tree` idempotente (2208 nodos), migración
  `0037`, 8 tests. **F2 construido en la misma rama:** `NodeContent` (O2O con hoja,
  objetivo/explicación/procedimiento/ejemplos) + `NodeMedia` (video_youtube/file/external,
  video_kind), migración `0038`, app `apps/learn/` con 6 rutas jerárquicas
  `/aprender/<asig>/<eje>/<bloque>/<tema>/<recurso>/`, 3 templates (home/list/detail), KaTeX hereda
  de `base.html`, comando `load_node_content` idempotente, admin inlines. YAML ejemplo:
  `docs/conocimiento/contenido/mat-num-enteros-conjunto-naturales.yaml`. **554/554 tests verde.**
  Tarjetas F1 y F2 en `4-auditoria/`. **F3 construido (2026-06-27).**
- **Guías interactivas - Fase 7 (gate + piloto) - EN AUDITORÃA 🟡 (2026-06-23):**
  ðŸ›ï¸ Claude hizo preflight + construcción (rama `feat/guias-fase7-gate-piloto`). Decisión del 🧑:
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
  nuevas** (CSP intacta). ðŸ›ï¸ Claude auditó como IA distinta: verificó la decisión de print nativo, el
  fix de especificidad (`!important` vence color inline), portada con a11y correcta y solucionario
  único — **sin errores**. **CI Linux verde (511 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#84** a `main` (`22d3d7d`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 7 (migración
  legacy + gate + piloto) — última del épico.**
- **Guías interactivas - Fase 5 - CERRADA 🟢 (2026-06-23):**
  🧩 Codex construyó pools ocultos editoriales, ensamblado por cuotas + distribución 20/50/30,
  no-repetición, sesiones transaccionales con timer server-side, corrección idempotente y dominio
  estructurado 60/40 aislado del progreso legacy (9 hallazgos propios corregidos). ðŸ›ï¸ Claude auditó
  como IA distinta: verificó timers server-side, intentos transaccionales por-recurso, aislamiento por
  scope+flag, reuso del parser de Fase 4, protección de historial (409) y gating de cobertura — **sin
  errores que corregir**. **CI Linux verde (510 OK, 1 skip)**, sin migraciones. Squash-merge de PR
  **#83** a `main` (`5063113`). Tarjeta en `backlog/6-finalizados/`. **Siguiente: Fase 6 (PDF).**
- **Guías interactivas - Fase 4 - CERRADA 🟢 (2026-06-22):**
  🧩 Codex construyó el parser seguro AST→SymPy; ðŸ›ï¸ Claude auditó como IA distinta, encontró y
  corrigió **1 hallazgo Medium de DoS** (apilamiento de exponentes que evadía el tope por-exponente y
  explotaba en `cancel`: nuevo `MAX_TOTAL_DEGREE`/`_degree_upper_bound` que corta sobre el AST antes
  del paso caro, +1 test) y cerró. **494 tests OK** (1 skip local `SIGALRM`), sin migraciones,
  `check --deploy` exit 0. Squash-merge de PR **#82** a `main`. Tarjeta en `backlog/6-finalizados/`.
  **Nota a futuro:** el timeout depende de `SIGALRM`+main thread (ok con gunicorn `sync`); documentar
  si se migra a `gthread`/`gevent`. **Siguiente: Fase 5 (evaluaciones nivel/final).**
- **Guías interactivas - Fase 3 - APROBADA TÉCNICAMENTE 🟢 (2026-06-22):**
  🧩 Codex auditó y corrigió generación/publicación manual, aislamiento y revalidación del runtime,
  panel editorial, esquema real de la guía, CSP, borrado lógico y N+1. **469 tests OK**; tarjeta en
  `backlog/5-cierre/` para auditoría final y merge de ðŸ›ï¸ Claude.
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
  publicación en dos fases. 🧩 Codex construyó; ðŸ›ï¸ Claude auditó y corrigió (`SET_NULL` en guía
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
  construyó, ðŸ›ï¸ Claude auditó (fix de GET inválido + 3 tests de regresión) y cerró. **PR #69
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
- 2026-06-28 — ðŸ›ï¸ Claude + 🧑: **UI accordeón + introducción didáctica + pauta de contenido.**
  Campo `introduccion` en `NodeContent` (migración `0042`) + 15 textos nivel ~10 años en YAMLs.
  Sección "Ejemplos Verdadero/Falso" renombrada. Fix acordeón KaTeX (wrap con `<span>` para
  que `justify-content: space-between` no explote los spans de math). Pauta de autoría
  `docs/conocimiento/pauta-contenido.md` (YAML + JSONL + gamificación + checklist).
- 2026-06-27 (tarde) — ðŸ›ï¸ Claude + 🧑: **Contenido ENTEROS_CONJUNTO estandarizado + banco GEN.**
  15 YAMLs con 4 ejemplos Sí/No + 5 errores_frecuentes + estado publicado. 150 ejercicios nuevos
  en 3 archivos JSONL (`-banco-gen-1/2/3.jsonl`): 3 CONC + 1 REC + 3 PROC + 3 PAES por recurso.
  Fixes `generate_node_summaries`: encoding Windows, Gemini multi-part parsing, rate-limit resilience.
  Resúmenes pendientes de regenerar (cuota Gemini agotada).
- 2026-06-27 — ðŸ›ï¸ Claude + 🧑: **F1–F3 + F6 CERRADAS — PR #102 squash-merge a `main` (rama `feat/grafo-conocimiento-f1`).**
  UI rediseñada: breadcrumb plegable, objetivo card, ejemplos interactivos (V/F/Sí-No), errores como
  preguntas conceptuales, banco con tarjetas+sombra. Ejercicios de clasificación (formato `matching`).
  Política **autopublicado inmediato** en `load_exercise_bank`. Contenido: 14 NodeContent + ejercicios
  ENTEROS_CONJUNTO + clasificación. Tests actualizados. Tarjetas en `6-finalizados/`.
- 2026-06-27 — ðŸ›ï¸ Claude + 🧑: **F3 — estructura pedagógica por ítems (`ItemGroup` + `NodeExercise` + pipeline JSONL) — rama `feat/grafo-conocimiento-f1`.**
  Decisiones **D2/D3/D4** ratificadas en la arquitectura (§8). Modelos nuevos **aditivos** anclados a
  `KnowledgeNode` (Sistema A intacto): `ItemGroup` (7 grupos estándar) + `NodeExercise` (banco único,
  `kind=item|template` para generadores futuros), migración `0039`, admin, comando idempotente
  `load_exercise_bank` (JSONL NotebookLM→Claude; **nunca autopublica**; no degrada publicaciones
  manuales), sección "Practica por ítems" (acordeón + toggle solución + KaTeX), prompts en
  `docs/conocimiento/pipeline/`. Piloto Naturales (4 ejercicios) verificado en navegador. 20 tests
  nuevos. Tarjeta F3 → `4-auditoria/`.
- 2026-06-27 — ðŸ›ï¸ Claude: **F6 (estructural) — prerrequisitos DAG + "Antes de empezar" — misma rama.**
  Comando `load_prerequisites` (YAML→`NodePrerequisite`, valida aciclicidad con `graphlib`, aborta sin
  escribir si hay ciclo, idempotente), sección informativa "Antes de empezar" en la página
  (`_prereqs.html`, enlaces a prerrequisitos publicados, nunca bloquea), DAG piloto `num-enteros.yaml`,
  timestamps en `NodeContent` (mig. `0040`). 13 tests. Estado por alumno (✓/!) y "siguiente
  recomendado" diferidos a F5. Verificado en navegador. Tarjeta F6 a `4-auditoria/`.
- 2026-06-26 — ðŸ›ï¸ Claude + 🧑: **F2 construido — `NodeContent`/`NodeMedia` + app `learn` + `/aprender/` — rama `feat/grafo-conocimiento-f1`.**
  Modelos con migración `0038`, app `apps/learn/` con 6 rutas jerárquicas, 3 templates (home/list/detail),
  KaTeX por herencia de `base.html`, comando `load_node_content` idempotente (actualiza `NodeMedia` si
  YAML incluye clave `media:`), admin inlines, YAML ejemplo piloto. 22 tests nuevos. **554/554 verde.**
  Tarjeta F2 movida a `4-auditoria/`.
- 2026-06-26 — ðŸ›ï¸ Claude + 🧑: **Arquitectura de plataforma (6 capas) + F1 construido — rama `feat/grafo-conocimiento-f1`.**
  Rediseño en 6 capas (banco≠evaluación; estado solo-rendimiento; asignatura como nodo raíz para
  Física/Química a futuro). Tarjetas F1–F6. **F1 construido y verde:** `KnowledgeNode`/`NodePrerequisite`,
  `import_knowledge_tree` idempotente (2208 nodos importados, 13 legacy omitidos), admin, migración `0037`,
  8 tests. Detalle en `reportes-sesion/2026-06-26.md`. **Siguiente: F2 (contenido + páginas, piloto Números Enteros).**
- 2026-06-25 — ðŸ›ï¸ Claude + 🧑: **Biblioteca de Conocimiento — esqueleto YAML completo (ejes 01–05) — PR #99 abierto.**
  Eje 05 PROBABILIDAD Y ESTADÃSTICA (7 bloques 05.01–05.07), Eje 02 ampliado (02.06 Sucesiones),
  Eje 03 completado (03.11–03.15), Eje 04 ampliado (04.12–04.13). Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Total: ~700 recursos en 37 bloques, 5 ejes.
- 2026-06-25 — ðŸ›ï¸ Claude + 🧑: **Eje 04 GEOMETRÃA completo — PR #98 en auto-merge.**
  11 bloques YAML atómicos (04.01–04.11), ~382 recursos, 55 temas. Flujo: NotebookLM genera,
  ChatGPT audita, Claude integra (commit por bloque). Conflict `TRIANGULOS_NOTABLES` resuelto
  con sufijo `_METRICA` en 04.04. Prompts para eje 05 PROBABILIDAD Y ESTADÃSTICA entregados.
- 2026-06-23 (tarde) — ðŸ›ï¸ Claude + 🧑: **Bugfixes operativos de guías + proyecto nuevo.**
  (1) **PR #87** `gunicorn --timeout 120` + truncar guía en extracción de ítems: arregla el
  `SystemExit: 1` (worker abortado a los 30 s en la llamada síncrona a Gemini; detectado por Sentry
  `PYTHON-DJANGO-K`). **âš ï¸ El Custom Start Command de Railway sobrescribe los archivos del repo →
  el 🧑 debe agregar `--timeout 120 --workers 3` en el dashboard.** (2) **PR #88** N+1 en
  `/asignaturas/` (30→3 queries; `SubjectListView` con `select_related`/`prefetch_related` + agrupado
  en memoria). (3) Diagnóstico de lentitud del sitio: **no era el código** sino **1 worker de gunicorn**
  saturado por los clics de extracción que colgaban el worker → recomendado `WEB_CONCURRENCY=3`.
  (4) **PR #89** tarjeta de backlog del proyecto **Biblioteca de Conocimiento Estructurada**.
  Tracing de Sentry activado temporal (`SENTRY_TRACES_SAMPLE_RATE=1.0`, **revertir a 0**).
- 2026-06-23 — ðŸ›ï¸ Claude: **Re-auditoría profunda del épico (F1–F7) + correcciones 🟢.**
  Doc en `docs/auditorias/2026-06-23-auditoria-epico-guias-interactivas.md`. F1–F6 sólidas. 5 hallazgos
  en F7 (Media/Baja, sin afectar datos), todos corregidos: `merge_items`/`edit_practice_quota` no
  funcionaban en staging (guard `enabled`→`editable`); un tema legacy no podía entrar a staging desde
  la UI (selector propio con todos los temas activos); `redirect` no importado en `item_review.py`
  (bug latente, NameError en ruta no-HTMX); gate contaba banco visible sin filtrar por la guía pública.
  13 tests F7 (de 9). Sin migraciones. Rama `fix/guias-fase7-auditoria`.
- 2026-06-23 — ðŸ›ï¸ Claude: **Fase 7 (gate + piloto) PREFLIGHT + CONSTRUIDA 🟡 — esperando auditor distinto.**
  Modelo de coexistencia (no se toca el legacy). `Topic.structured_bank_staging` (mig. aditiva `0036`)
  + `structured_bank_editable` para preparar con el flag apagado; gate solo-lectura que reusa los
  ensambladores; activación admin gobernada por el gate + rollback. 9 tests F7. Rama
  `feat/guias-fase7-gate-piloto`; `seguridad:requiere-claude`. Audita 🧩 Codex (IA distinta al builder).
- 2026-06-23 — ðŸ›ï¸ Claude: **Fase 6 (PDF) AUDITADA Y CERRADA 🟢 — merge de PR #84 a `main`.**
  Auditor distinto al builder (Codex). Fase solo-front: verificado print nativo (sin JS/deps nuevas,
  CSP intacta), el fix del bug de texto invisible (`!important` vence color inline), portada solo-print
  con a11y correcta, solucionario único consolidado y saltos de página. Test fija la decisión
  (`assertNotContains("html2pdf")`). CI Linux verde (511 OK, 1 skip), sin migraciones. **Sin errores.**
- 2026-06-23 — ðŸ›ï¸ Claude: **Preflight Fase 6 (PDF) RESUELTO 🟢 — Ready para 🔨 Antigravity.**
  Decisión del 🧑: **print nativo** (`window.print()` + `@media print`), NO html2pdf.js (riesgo
  `unsafe-eval`/CSP, rasterización del tema oscuro, ~1 MB JS). Realidad encontrada: el
  `learning-guide-print.css` está **obsoleto** (apunta a clases inexistentes), `header{display:none}`
  **oculta logo+título** (no hay portada) y las clases Bootstrap/inline dejan **texto invisible** en
  papel. Alcance afinado: reescribir el print CSS contra el markup real, portada solo-print, forzar
  texto negro, resolver doble solucionario, relabelar botón. **Sin migraciones** (front).
  Tarjeta en `backlog/3-construccion/`; rama `feat/guias-fase6-pdf`.
- 2026-06-23 — ðŸ›ï¸ Claude: **Fase 5 AUDITADA Y CERRADA 🟢 — merge de PR #83 a `main`.**
  Auditor distinto al builder (Codex). Verificadas las invariantes sensibles: timers 100% server-side,
  consumo de intento transaccional y **por-recurso** (no global), aislamiento `scope+flag`, reuso del
  parser seguro de Fase 4, **protección de historial** (409 al editar preguntas ya usadas; pools solo se
  archivan), ownership/CSRF, guards anti-DoS del ensamblador y gating de cobertura. Los 9 hallazgos del
  self-audit de Codex están corregidos; **no encontré P0/P1 nuevos**. CI Linux verde (510 OK, 1 skip),
  sin migraciones. `audit:aprobado` aplicado.
- 2026-06-22 — ðŸ›ï¸ Claude: **Preflight Fase 5 RESUELTO 🟢 — Ready para construir.**
  Contrastado contra el código real. Hueco de alcance resuelto (decisión 🧑: **Fase 5 incluye la
  generación de los pools ocultos** — `visible_bank_service` hardcodea `banco_visible`). Contradicciones
  fijadas: `final_distribution` mapea a `level` (N1/N2/N3); timer (`expires_at = inicio + config`) ≠
  cota de duración (`sum(estimated_minutes)±%`), exigir `estimated_minutes>0`; intento en transacción
  + una sola sesión `en_curso`. Dominio por **último intento** (60/40, ≥80% y final ≥80%), función
  nueva sin tocar el `progress_service` legacy. Sin migraciones esperadas. Tarjeta en
  `backlog/3-construccion/`; construye 🔨 Antigravity (`feat/guias-fase5-evaluaciones`).
- 2026-06-22 — ðŸ›ï¸ Claude: **Fase 4 AUDITADA Y CERRADA 🟢 — merge de PR #82 a `main`.**
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
- 2026-06-22 — ðŸ›ï¸ Claude: **Fix dificultad acentuada — 🟢 mergeado a `main`** (`fix/dificultad-acentos`).
  Detectado en QA local: con API key real, la generación de guías de F2 fallaba la validación porque
  la IA devuelve dificultades **con acento** (`"básica"`) y el modelo usa claves **sin acento**
  (`basica/.../desafio`); además F1 perdía silenciosamente la dificultad a "intermedia". Se agregó
  `Question.normalize_difficulty()` y se canonizó en prompts/mocks/validación/plantilla
  (`item_extraction`, `learning_guide`, `visible_bank`, `item_review`, `_item_row.html`). +3 tests.
  **472 tests OK**, sin migración. Verificado en navegador (badge "Básica" correcto).
- 2026-06-22 — ðŸ›ï¸ Claude + 🔨 Antigravity + 🧩 Codex: **Guías interactivas — Fases 2 y 3 CERRADAS 🟢
  y mergeadas a `main`** (squash-merge, F2+F3 juntas; F3 se construyó sobre F2 sin mergear).
  **F2** (guía ProfeOnline original + anti-copia): generación IA, motor de originalidad determinista
  (n-gramas de 10 palabras + blocklist + tope anti-DoS), publicación manual bloqueada con
  **revalidación en caliente por hash**, versionado con `archivada` y guía única pública por tema.
  Cierre legal de ðŸ›ï¸ Claude (`seguridad:requiere-claude`) ✅. **F3** (banco visible + estudio):
  página pública de la guía (KaTeX, imprimible), banco agrupado por ítem/dificultad, práctica
  por ítem/mixta **sin peso académico**, panel editorial con cuotas/déficit/generación, y
  **aislamiento del banco legacy con `scope=""`**. Construyó Antigravity; Codex auditó/corrigió ambas;
  ðŸ›ï¸ Claude verificó en corrida limpia y cerró. **Barrera: 469 tests OK** + `check --deploy` 0 errores
  + sin migraciones pendientes. Migraciones aplicadas: `0034` (F1), `0035` (F2). Tarjetas en
  `backlog/6-finalizados/`. **Pendiente P3 (no bloqueante): QA visual móvil 320/360/390. Siguiente: F4.**
- 2026-06-22 — 🧩 Codex: **Guías interactivas — Fase 3 APROBADA TÉCNICAMENTE 🟢.**
  Se corrigieron publicación incompleta/automática, borrado físico, edición en caliente de preguntas
  publicadas, revalidación del submit, cruces entre temas, cuotas concurrentes, UI editorial ausente,
  render del esquema real de Fase 2, CSP y N+1. **469 tests OK** en 324,059 s; 13 tests específicos,
  104 regresiones afectadas, deploy-check, migraciones y pre-commit verdes. Tarjeta movida a
  `backlog/5-cierre/`; queda revisión final y merge por ðŸ›ï¸ Claude.
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 3 (banco visible + experiencia de estudio) — LISTO PARA AUDITORÃA 🟡**
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
  legal final y merge por ðŸ›ï¸ Claude (`seguridad:requiere-claude`).
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 2 (guía ProfeOnline original + originalidad) — LISTO PARA AUDITORÃA 🟡**
  (rama `feat/guias-fase2-guia-original`, `seguridad:requiere-claude`). Se completó la implementación
  de la Fase 2 del epic. Lógica aditiva con campos de originalidad en `LearningGuide` (migración `0035`),
  servicio de generación con IA (grounded en ítems aprobados del tema y fuentes privadas, anti-injection),
  motor de originalidad determinista sin truncamiento silencioso (n-gramas de 10 palabras y blocklist de
  marcas), control de concurrencia y revalidación en caliente mediante transacciones atómicas y
  bloqueos select_for_update (para Topic y guías ordenadas), restricción unique_active_published_guide_per_topic,
  panel HTMX CSP-safe (sin JS inline), y 17 tests unitarios focalizados. Barrera completa
  verificada (449 tests Django OK, check --deploy OK, makemigrations --check OK, pre-commit OK).
  Tarjeta movida a `backlog/4-auditoria/`.
- 2026-06-22 — ðŸ›ï¸ Claude + 🔨 Antigravity + 🧩 Codex: **Guías interactivas — Fase 1 CERRADA 🟢**
  (squash-merge a `main`, commit `6ccf403`). Panel solo-admin `/publicar/items/`: la IA propone
  ítems de aprendizaje desde una guía privada (`QuizGuide`) calibrando dificultad al nivel educativo,
  y el profesor los edita/fusiona/aprueba/archiva. Todo **detrás del flag
  `Topic.structured_bank_enabled`** (banco legacy intacto). Antigravity construyó; Codex rechazó por
  5 P1 + 5 P2; ante la falta de correcciones del builder, ðŸ›ï¸ Claude (por decisión del 🧑) corrigió
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
- 2026-06-22 — 🔨 Antigravity: **Guías interactivas — Fase 1 (extracción y aprobación de ítems) — LISTO PARA AUDITORÃA 🟡**
  (rama `feat/guias-fase1-extraccion-items`). Se implementó el servicio de extracción curricular IA `item_extraction_service.py` (calibra la dificultad por nivel pedagógico y soporta LaTeX) y el panel HTMX in-app `publicar/items/` (edición inline, aprobación/archivado, vinculación de recursos y fusión segura de ítems). Todo 100% aditivo y detrás del flag de tema. Suite completa con 425 tests OK (10 nuevos para esta fase). Tarjeta movida de `2-arquitectura/` a `4-auditoria/`.
- 2026-06-21 — ðŸ›ï¸ Claude + 🧩 Codex + 🧑: **Rediseño de recurso + progreso académico — CERRADO 🟢**
  (rama `feat/recurso-progreso-academico`). Vista de recurso rediseñada (título primero, metadatos
  compactos, descripción con Ver más/menos, columna legible, sin barra "Comprendido") + bloque único
  "Practica y evalúa tu aprendizaje" con pestañas por nivel. **Progreso calculado desde intentos
  reales**: promedio de los últimos 3 por modo, ponderado 30/70, estados Preparado/Aprobado; motor
  `progress_service` + selectores sin N+1. Perfil ampliado con panel por tema/recurso. "Comprendido"
  retirado de la UI (endpoint+modelo conservados); agregados de tema usan progreso ponderado.
  🧩 Codex corrigió disponibilidad por modo, cobertura real del perfil y pestañas móviles.
  **Sin migraciones. 391 tests OK + QA 320/360/390 px. PR #75 squash-mergeado**
  en `main` (`3d847a6`, 2026-06-21). Tarjeta en `backlog/6-finalizados/`.
- 2026-06-21 — ðŸ›ï¸ Claude + 🧑: **Reproductor de preguntas a pantalla completa — CERRADO 🟢** (commit
  `faacd8c`, merge a `main`). Panel interno fullscreen (móvil + PC): una pregunta a la vez con
  `Anterior`/`Siguiente`, pantalla de revisión respondida/pendiente previa al envío y resultados a
  pantalla completa con corrección. Aplica a Preparación, Evaluación por nivel y evaluación final del
  tema. Overlay global `#quiz-player-root` + `static/js/quiz-player.js` (CSP-safe), reusa las vistas
  HTMX; `quiz_submit` ordena resultados por orden de presentación. **Sin migraciones ni endpoints
  nuevos. Suite completa 370 OK** + QA visual (escritorio y móvil 360px). Tarjeta en
  `backlog/6-finalizados/`.
- 2026-06-21 — ðŸ›ï¸ Claude + 🧑: **Agente local de subida `upload-batch/v1`** (commit `79836ad`).
  `scripts/process_upload_batch.py` sube cada video como no listado, obtiene la transcripción
  desde la IP local, registra el ítem en ProfeOnline y espera la validación antes de hacerlo
  público (revierte a no listado si la confirmación server-side falla). Cierra el **paso 2** del
  pipeline único de publicación: el cliente Node `profeonline-uploader` se reemplaza por este
  agente Python local. Incluye `cleanup_borradores` (limpia borradores residuales, dry-run por
  defecto, respeta ítems en vuelo) + tests del agente (4 OK). Sin migraciones.
- 2026-06-21 — 🧩 Codex + 🧑: **Taxonomía, cobertura y Lenguaje Algebraico actualizados en producción.**
  Asignaciones vigentes: Electromagnetismo → Física; Física Escolar → Física +
  Medio/Preuniversitario; Matemática Media/Preuniversitaria → Matemáticas. El resumen del banco usa
  Ãrea→Nivel→Asignatura→Tema→Recurso y orden Escolar→Medio/Preuniversitario→Universitario.
  Lenguaje Algebraico quedó con 1.530 preguntas (90 en cada uno de 17 recursos), cobertura 17/17 y
  orden manual `1.x→2.x→3.x→4.01→4.01a→4.02→4.03→4.04`.
- 2026-06-20 — ðŸ›ï¸ Claude + 🧑: **Nivel educativo por asignatura (rama `feat/nivel-por-asignatura`).**
  Nuevo campo `Subject.education_level` (migración 0031) que los temas/recursos sin nivel propio
  heredan vía `Resource.get_education_level()`; cableado en generación inline, estudio, pipeline y
  `generate_pending_questions`. Comando `set_subject_level --subject … --level … [--apply]` (dry-run
  por defecto). Aplicado en producción: **Física Escolar → Medio/Preuniversitario**. Tests
  focalizados verdes.
- 2026-06-20 — ðŸ›ï¸ Claude + 🧑: **Rediseño de dos paneles del banco (rama `feat/rediseno-resumen-banco`).**
  (1) Resumen `/publicar/preguntas/resumen/` → acordeón
  Ãrea→Nivel→Asignatura→Tema→Recurso con fracciones
  `auditados/total` por categoría editorial, preguntas por nivel y semáforo (verde/amarillo/rojo <20%).
  (2) `question_review` → config de evaluación full-width arriba + generador IA por nivel/modo con
  cantidad y descripción; Gemini ahora ve las preguntas existentes para no repetir; "copiando documento"
  deshabilitado. Sin migraciones. Tests focalizados verdes. Detalle en
  `reportes-sesion/2026-06-20-rediseno-paneles-banco.md`. QA visual y despliegue completados.
- 2026-06-18 — ðŸ›ï¸ Claude: **Cierre de Fase 5 (auditoría final).** Auditados como no destructivos el
  generador local aditivo (`scratch/generate_math_questions.py`: sin `.delete()`, dedup por
  `existing_texts`) y el importador transaccional (`import_questions_json` dentro de `transaction.atomic`).
  Tarjeta **"Estudio de banco de preguntas"** archivada (`4-auditoria` → `6-finalizados`); `4-auditoria/`
  queda vacía (solo `.gitkeep`). Barrera re-verificada local: **331 tests OK**; `check --deploy` solo con
  warnings de dev-settings (sin errores).
- 2026-06-16 — ðŸ›ï¸ Claude + 🧑 Usuario: **Banco de preguntas con generación IA CERRADO 🟢** (6 PRs:
  #62 banco+generación grounded, #63 fix key-leak + backoff 429, #64 transcript guardado en el recurso,
  #65 `backfill_transcripts`, #66 dos modos video/documento + UI de guías, #67 filtro `--subject`).
  289 tests. **Aprendizaje:** YouTube bloquea el scraping masivo de transcripts por IP → se bajan a
  cuentagotas desde el PC y se guardan. Detalle y pendientes en `reportes-sesion/2026-06-16.md`.
- 2026-06-05 — ðŸ›ï¸🔨🧩 **"Estudio de publicación (Fase 1)" CERRADO 🟢.** Página staff (`/publicar/estudio/`) que
  arma una **orden de lote** (`profeonline.upload-batch/v1`): selecciona varios videos (solo por nombre, no sube
  contenido), Ãrea/Asignatura/Tema/Módulo (con creación inline), playlist (enlace o crear nueva) e indicación libre;
  Codex sube a YouTube y publica tal cual. Codex auditó (P2/P3 menores), QA del 🧑 detectó un bug al crear tema inline
  (`resource_ordering_method`) que Claude corrigió + test. Mergeado a `main` (squash). Tarjeta en `6-finalizados/`.
  **Sin migraciones.** Pendiente aparte: fix del seed `Matemática` (singular) y la Fase 2 (cola/agente).
- 2026-06-04 — ðŸ›ï¸ Claude + 🧑 Usuario: **"Estudio de publicación" SIMPLIFICADO (revisión pre-merge).** Tras la QA,
  Octavio pidió algo más simple: lote de videos (por nombre) + Ãrea/Asignatura/Tema/Módulo + playlist + indicación
  libre; Codex hace título/descripción/miniatura/subida tal cual. Se quita copy/duplicados/miniatura/privacidad y se
  agrega selección múltiple de archivos. Tarjeta `4-auditoria` → `3-construccion` para recorte por 🔨 Antigravity.
  Contrato pasa a `upload-batch/v1`.
- 2026-06-04 — 🧩 Codex + ðŸ›ï¸ Claude: **Preflight de "Estudio de publicación (Fase 1)" OK** (sin objeciones).
  3 refinamientos integrados al handoff: inline de asignatura setea `Subject.area`; inline de módulo setea
  `subject` (+topic/levels) y `module_slug` es solo organizativo; mantener firma de `build_resource_copy`
  (wrapper compatible, tolera `video_url` vacío). JSON server-side. **Listo para Antigravity.**
- 2026-06-04 — ðŸ›ï¸ Claude: **Handoff "Estudio de publicación (Fase 1)" mergeado a `main` (PR #54).**
- 2026-06-04 — ðŸ›ï¸ Claude + 🧑 Usuario: **Handoff "Estudio de publicación (Fase 1)" Ready.** Idea creada y
  avanzada `1-por-iniciar` → `2-arquitectura`. Planificación 🧑+🤖 refinada por 🧩 Codex (8 acotaciones
  integradas) y verificada contra el código (URL real `/api/recursos/crear-video/`, webhook sin
  `area_slug`/`module_slug`, `Level` M2M). Acotado a la web que genera el JSON; Fase 2 (cola/agente) aparte.
- 2026-06-03 — ðŸ›ï¸🔨 **Pulido técnico a11y/SEO CERRADO 🟢 (PR #46).** Antigravity construyó (focus-trap
  drawer, skip-link, reduced-motion, JSON-LD Person/LocalBusiness, tokens); Claude auditó (2ª IA) y
  corrigió una regresión (`--secondary-hover` borrado del `:root`). Tarjeta en `6-finalizados/`.
- 2026-06-03 — ðŸ›ï¸🧩🔨 **Handoff PWA refinado y Ready.** Claude fusionó el plan de Antigravity + Plan v2
  de Codex y corrigió 4 supuestos contra el código (color teal, apple-touch PNG, precache sin hashing,
  start_url no medible). Decisiones 🧑: theme `#0f766e`, QA iOS opcional. Tarjeta en `2-arquitectura/`.
- 2026-06-03 — ðŸ›ï¸🔨 **a11y + pulido móvil CERRADOS 🟢 (PR #42, #43).** Contraste AA de WhatsApp,
  drawer móvil lateral, WhatsApp flotante, contacto (Concepción, sin mail), detalle de recurso reordenado.
- 2026-06-03 — ðŸ›ï¸🔨 **Rediseño del Home CERRADO 🟢.** Antigravity construyó (Hero reenfocado, perfil
  real de Octavio Chamblas, "Cómo funciona" 2 pasos, destacados condensados); Claude auditó como 2ª IA
  y corrigió (bug CSS `:active`, CSS muerto de testimonios, imagen huérfana). Barrera verde. Prueba
  social diferida por falta de testimonios reales (tarjeta nueva).
- 2026-06-03 — ðŸ›ï¸ Claude + 🧑 Usuario: **Handoff de Home redactado y Ready.** Decisiones: placeholders
  + contenido hardcodeado (sin modelos/admin). Tarjeta movida `1-por-iniciar` → `2-arquitectura`.
- 2026-06-03 — ðŸ›ï¸🔨🧩 **Verificación de email mergeada y CERRADA 🟢 (PR #38).** Antigravity construyó,
  Codex auditó (P1 duplicados, P2 anti-enumeración, P3 usuarios sin email), Antigravity corrigió, Claude
  cerró (sensible). 202 tests. `mandatory` + Google exento; migración no bloquea a usuarios actuales.
- 2026-06-03 — ðŸ›ï¸🔨🧩 **M5 Analítica interna mergeada y CERRADA 🟢 (PR #36).** Antigravity construyó,
  Codex auditó y curó privacidad, Claude cerró como 3ª IA (superficie sensible). Suite 191 tests. Matriz M5 → 🟢.
- 2026-06-02 — 🧩 Codex: **cura privacidad M5 en PR #36** — metadata por allowlist de evento,
  `path` sin querystrings, JS sin `href`/texto/`file_url` sensible y regresiones de analitica. Lock liberado.
- 2026-06-02 — ðŸ›ï¸ Claude + 🧑 Usuario: **rumbo post-P0 definido.** C1/C2 **aceptados** como riesgo;
  sprint de valor visible (Analytics → Home → QA a11y). Handoff de **Analytics interno** redactado en `2-arquitectura`.
- 2026-06-02 — ðŸ›ï¸ Claude + 🧑 Usuario: **rotación de credenciales de prod** (la URL quedó expuesta en
  chat). Causó un 500 breve (web cacheaba la `DATABASE_URL` vieja); recuperado con redeploy. Staging
  se desincronizó por error y se revirtió. Procedimiento + lecciones en `runbook-backups.md §5`.
- 2026-06-02 — ðŸ›ï¸ Claude + 🧑 Usuario: **A1 → 🟢 staging operativo** en Railway (`Web-staging` +
  `Postgres-Staging` aislada, 200 en `/` y `/admin/`). 2 hallazgos resueltos (`DJANGO_USE_X_FORWARDED_PROTO`,
  `collectstatic`/Custom Start Command) → `runbook-staging.md §8`.
- 2026-06-02 — ðŸ›ï¸ Claude + 🧑 Usuario: **C2 → backup real de prod + restore drill verificados**
  (`pg_dump` 18.4; runbook §4.B). Riesgo 🟡 (falta automatizar).
- 2026-06-02 — 🔨 Antigravity + ðŸ›ï¸ Claude: **Router mergeado (PR #29)** — workflow mecánico de
  ruteo/labels (sin `contents: write`, sin secretos, no mergea). Revisado por Claude (`seguridad:requiere-claude`).
- 2026-06-02 — 🔨 Antigravity + ðŸ›ï¸ Claude: **A1 mergeado (PR #30)** — `check_environment` + runbook
  staging. Riesgo A1 queda 🟡 hasta que el 🧑 Usuario cree el servicio staging + DB propia en Railway.
- 2026-06-02 — 🔨 Antigravity + ðŸ›ï¸ Claude: **C2 mergeado (PR #28)** — `backup_db`/`restore_db` con
  guardas anti-prod + runbook. Riesgo C2 queda 🟡 hasta backups automáticos del proveedor.
- 2026-06-02 — 🔨 Antigravity + ðŸ›ï¸ Claude: **C1b mergeado (PR #27)** — `seed_content` idempotente.
- 2026-06-02 — ðŸ›ï¸ Claude: **C3 cerrado en 🟢** — código en `main` (PR #26) + `REDIS_URL` en Railway (PR #31).
- 2026-06-02 — ðŸ›ï¸🔨🧩 **C1 mergeado (PR #24)** por el flujo completo: Antigravity construyó,
  Codex auditó (detectó fuera-de-alcance + `build.sh` + docs), Claude cerró. Lock liberado.
- 2026-06-02 — ðŸ›ï¸ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 — ðŸ›ï¸ Claude: automatización del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 — ðŸ›ï¸ Claude: reestructuración de la documentación (PR #19).
- **03.12 Recuperación de Función Cuadrática — CERRADO por Codex 🟢 (2026-07-12):** se auditó el bloque completo en Railway tras detectar preguntas placeholder dañadas por una intervención previa. `03.12.01.02` a `.08` y `03.12.06.01` a `.08` fueron reparados archivando las preguntas `publicada` defectuosas y reemplazándolas por redacción manual en Codex, leyendo únicamente el `NodeContent` propio de cada recurso. Verificación final directa en Railway: los `47/47` recursos de `03.12` quedaron con `21` preguntas `publicada`, distribución `7/7/7`, `4` alternativas y `1` correcta por pregunta, sin placeholders activos. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **03.15.05 Parámetros y transformaciones de funciones periódicas — CERRADO por Codex 🟢 (2026-07-12):** `03.15.05.01` a `.10` quedaron publicados en Railway con `210` preguntas nuevas (`21` por recurso, `7/7/7`), validadas por duplicados internos y por prefijo `MAT.ALG.FUNC_TRIG_PARAMETROS`. El borrador inicial tenía desbalance interno (`7/8/6` y `7/9/6`) y un cierre sobrante en el script; se corrigió antes de publicar, sin escrituras parciales. Confirmación explícita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
- **03.06.01.03 Extracción del factor común monomio — AJUSTADO por Codex 🟢 (2026-07-13):** Railway mostró que era el siguiente recurso incompleto en orden real (`21` preguntas, distribución `5/9/7`). Se leyó únicamente su `NodeContent`, se archivaron los ítems previos y se publicaron `21` preguntas nuevas redactadas manualmente en Codex, equilibradas a `7/7/7`. La validación cubrió duplicados internos y contra el prefijo `MAT.ALG.FACTOR_COMUN`; verificación independiente posterior confirmó `4` alternativas y exactamente `1` correcta por pregunta. No se usaron APIs externas de IA ni `generate_node_assessment_questions`. Siguiente recurso incompleto en orden real: `03.06.01.04` (`21`, distribución `4/10/7`).
- **03.15.06 Modelamiento trigonom?trico y extensiones ? CERRADO por Codex ?? (2026-07-13):** `03.15.06.01` a `.10` quedaron publicados en Railway con `210` preguntas nuevas (`21` por recurso, `7/7/7`), validadas por duplicados internos y por prefijo `MAT.ALG.FUNC_TRIG_MODELO`. El borrador inicial ten?a desbalance interno (`7/8/6` en la mayor?a de los recursos y dos casos con `22` ?tems); se corrigi? antes de publicar, sin escrituras parciales. Confirmaci?n expl?cita: no se usaron APIs externas de IA ni `generate_node_assessment_questions`.
