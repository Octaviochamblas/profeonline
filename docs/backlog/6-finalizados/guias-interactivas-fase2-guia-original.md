# Guías interactivas — Fase 2: guía ProfeOnline original + originalidad

- **Estado:** 🟢 CERRADA (2026-06-22) — gate técnico de Codex + cierre legal de Claude; barrera completa verde; mergeada a `main`.
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · pedagogía · legal
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase2-guia-original`) → 🧩 Codex (audita) → 🏛️ Claude (cierre, **revisa originalidad**)

> **Alcance: SOLO generación del borrador + validación de originalidad + publicación manual.**
> Sin banco visible/estudio (Fase 3), sin parser (Fase 4), sin evaluaciones (Fase 5). Núcleo
> legalmente sensible: la validación anti-copia es el corazón de esta fase.

## Objetivo (una frase)
A partir de los **ítems aprobados** de un tema (`ExerciseItem.status="aprobado"`) y de la(s) guía(s)
privada(s) de origen (`QuizGuide.content_text`), la IA genera el **borrador de una guía ProfeOnline
original** (no copia), se **valida su originalidad** (anti-copia) y el profesor la **publica
manualmente**.

## Antes de empezar
- `git pull` (Fase 0 #81, parser #80 y Fase 1 ya en `main`).
- Detrás del flag `Topic.structured_bank_enabled` (igual que Fase 1); temas apagados intactos.
- **Nada se publica automáticamente.**

## Fuentes a leer
- `apps/content/models/learning_guide.py` — modelo destino YA EXISTE: `topic`, `title`, `slug` (auto),
  `structured_content` (JSONField), `resources` (M2M), `private_sources` (M2M a `QuizGuide`),
  `visibility` (`interna`/`publica`), `status` (`borrador`/`publicada`).
- `apps/content/models/exercise_item.py` — entrada: ítems con `status="aprobado"`; FK `learning_guide`
  para enlazar los ítems usados.
- `apps/content/services/ai_generation_service.py` — reusar `_call_gemini_api`/`_call_openai_api`,
  `_loads_ai_json`, `_sanitize_key`, `_post_json_with_retry`, selección de llave. KaTeX ya integrado.
- `apps/content/views/item_review.py` (Fase 1) — patrón de panel `is_admin` + helpers de flag
  (`_get_enabled_topic`), JS externo con nonce, mensajes saneados. **Replicar ese patrón.**
- `templates/pages/item_extraction.html` + parciales (estilo `studio-*`/`bg-glass`).

## Alcance de construcción

### 1) Servicio de generación — `apps/content/services/learning_guide_service.py`
- `generate_guide_draft(topic, private_guides, api_key=None) -> dict`:
  - Reúne ítems `aprobado` del tema + `content_text` de las guías privadas.
  - Prompt (`_build_guide_prompt`, LaTeX en raw strings) que pide JSON `structured_content` con:
    introducción/resumen, fórmulas (KaTeX `$...$`/`$$...$$`), ejemplos resueltos, ejercicios por
    ítem y dificultad, desafíos y solucionario.
  - **Instrucción anti-copia explícita:** reproducir cobertura/estructura pedagógica, **nunca** copiar
    texto, imágenes, logos ni nombres institucionales del original.
  - Parsea con `_loads_ai_json`; saneo con `_sanitize_key`. Mock determinista sin llave/en tests.
  - **No persiste**; devuelve el dict.

### 2) Servicio de originalidad — `apps/content/services/originality_service.py`
- `check_originality(structured_content, private_guides) -> dict` → `{"passed": bool, "issues": [...]}`:
  - Aplana el texto del borrador y lo compara contra `content_text` de cada guía privada.
  - **Fragmentos extensos copiados:** coincidencia de secuencias/n-gramas largos por encima de un
    **umbral configurable** (decisión del 🧑 — p. ej. ≥ N palabras consecutivas idénticas, normalizando
    espacios/mayúsculas). Reporta el extracto + la fuente.
  - **Marcas/nombres institucionales ajenos:** lista configurable (colegios/editoriales) + heurística
    de nombres propios presentes en el borrador.
  - Puro Python, determinista, sin red → 100% testeable.
  - ⚠️ Documenta el umbral elegido; 🏛️ Claude lo revisa en el cierre.

### 3) Panel admin propio (HTMX, `is_admin`) — `apps/content/views/learning_guide_review.py`
- Elegir tema (habilitado) → ver ítems aprobados → "Generar borrador con IA".
- Mostrar el borrador (render KaTeX en `htmx:afterSwap`), permitir **editarlo**.
- "Validar originalidad" → corre `check_originality`, muestra hallazgos; si hay issues **bloquea la
  publicación**.
- "Publicar" (manual): `status="publicada"`, `visibility="publica"` SOLO si la validación pasó; si no,
  queda `borrador`/`interna`. Enlaza los `ExerciseItem` usados vía su FK `learning_guide`.
- JS solo en archivo externo con nonce + `?v=N`; nada inline.

### 4) URLs y plantillas
- Rutas bajo `publicar/guias-profeonline/...` (generar, validar, publicar, editar) en `publish_urls.py`.
- Enlace en el menú staff de `templates/base.html`.
- `templates/pages/learning_guide_review.html` + parciales. CSS nuevo → cache-buster `?v=N`.

## Criterios de aceptación
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check` (el modelo ya existe; si hace
  falta una migración, **aditiva**).
- [ ] Generación con mock → `structured_content` con todas las secciones; cero red en tests.
- [ ] Originalidad detecta fragmento extenso copiado y marca institucional; deja pasar texto original.
- [ ] Publicación **bloqueada** si la validación falla; permitida si pasa; borrador no visible como pública.
- [ ] Flag por tema gobierna panel y mutaciones; banco legacy intacto.
- [ ] Solo `is_admin`; `_sanitize_key` en errores; CSP intacta.

## No-objetivos
- Banco visible / estudio del alumno (Fase 3), parser (Fase 4), evaluaciones (Fase 5), PDF (Fase 6).
- Publicar nada automáticamente.

## Riesgos / decisiones abiertas
- **Originalidad (legal):** riesgo central. Decisión del 🧑: **umbral anti-copia** y lista de marcas.
  Rollback: publicación manual + flag desactiva el tema.
- **Costo IA:** generar a cuentagotas (un borrador por tema por disparo).

## Auditoría y correcciones 🧩 Codex — 2026-06-22

**Gate técnico:** aprobado; sin P0/P1 abiertos. Requiere cierre legal final de 🏛️ Claude.

### Hallazgos corregidos

- **P1 — versionado roto:** una guía publicada no permitía crear reemplazo y, al reemplazarla,
  la versión anterior volvía a `borrador`, quedando expuesta a sobrescritura. Se agregó estado
  `archivada`; el panel permite generar un borrador de reemplazo y las versiones sustituidas quedan
  internas e inmutables.
- **P1 — fuentes desactualizadas/no autorizadas:** validación y publicación ahora vuelven a exigir
  fuentes persistidas, activas y vinculadas al tema/asignatura/recurso. Las filas de `QuizGuide` se
  bloquean durante validación/publicación para evitar carreras.
- **P1 — contrato JSON permisivo:** ahora exige introducción/resumen, cobertura de todos los ítems
  aprobados, IDs globalmente únicos, tipos y textos obligatorios, ejercicios con solución y
  solucionario completo sin duplicados.
- **P1 — flujo HTMX incorrecto:** guardar devolvía el panel completo dentro del contenedor de
  contenido y cancelar reabría el editor. Se corrigieron targets, retarget de errores y cancelación.
- **P2 — proveedor IA:** con solo `OPENAI_API_KEY`, la clave se reenviaba como `api_key` genérica y
  terminaba tratándose como Gemini. Se preservó la selección real del proveedor y se añadió regresión.
- **P2 — auditoría:** hash JSON canónico compacto, fuentes ordenadas y timestamps UTC; coincidencias
  de marcas con límites de palabra y n-gramas sin unir artificialmente campos JSON.
- **P2 — concurrencia/evidencia:** generación bloquea el tema al persistir; edición bloquea la guía;
  la publicación actualiza informe, fecha y hash de la revalidación en caliente.
- **P2 — errores:** respuestas HTML dinámicas escapan mensajes operativos y la generación no expone
  detalles internos del proveedor.

### Barrera real

- `.venv\Scripts\python.exe manage.py test apps.content.tests.test_learning_guide` →
  **24 tests OK**.
- `.venv\Scripts\python.exe manage.py test` → **456 tests OK** en 773.853 s.
- `.venv\Scripts\python.exe manage.py check --deploy` → exit 0; solo 7 warnings conocidos de
  settings locales.
- `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` →
  **No changes detected**.
- `.venv\Scripts\pre-commit.exe run --all-files` → todos los hooks **Passed**.
- `git diff --check` → sin errores.

## Cierre legal 🏛️ Claude — 2026-06-22

Revisé el núcleo sensible (originalidad + publicación) exigido por `seguridad:requiere-claude` y lo apruebo:

- **Motor de originalidad determinista** (`originality_service.py`): normaliza (quita LaTeX, acentos
  y puntuación; minúsculas; colapsa espacios), detecta **n-gramas de 10 palabras** copiados y marcas
  institucionales con límite de palabra; **tope de 150k caracteres** (anti-DoS) que **lanza** error
  en vez de truncar en silencio. Sin red, determinista.
- **Publicación realmente bloqueada:** `publish_learning_guide_view` revalida **en caliente** por
  hash de auditoría (detecta cambios del borrador o de las fuentes desde la última validación),
  reejecuta `check_originality`, revalida el esquema y **reautoriza las fuentes privadas**; si algo
  falla, no publica. **Nada se publica automáticamente.**
- **Versionado seguro:** una sola guía publicada por tema (constraint parcial); al reemplazar, la
  anterior pasa a `archivada`/`interna` (inmutable), sin perder historial.
- **Concurrencia:** `select_for_update` sobre tema + guías + fuentes en orden estable.
- **Sin exposición prematura al alumno** (ningún view de alumno referencia `LearningGuide`; eso es
  Fase 3).

**Decisión del 🧑 (no bloqueante):** el **umbral anti-copia** quedó en **10 palabras** consecutivas
(parámetro `threshold` en `check_originality`) y la **blocklist de marcas** en
`BLOCKLIST_MARCAS`. Ambos son ajustables; si quieres otro umbral o más instituciones, se cambian sin
rediseño.

**Barrera reverificada por 🏛️ Claude** (`.venv`): `check --deploy` exit 0 (7 warnings locales) ·
`makemigrations --check` sin cambios · `pre-commit` Passed · `git diff --check` sin errores ·
`manage.py test` (suite completa) — resultado anotado en el reporte de sesión.
