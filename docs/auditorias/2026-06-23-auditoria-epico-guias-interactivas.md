# Auditoría profunda del épico "Guías interactivas y banco por ítems" (F1–F7)

- **Fecha:** 2026-06-23 · **Auditor:** 🏛️ Claude (re-auditoría completa post-merge de F7)
- **Alcance:** F1 (ítems), F2 (guía original), F3 (banco visible), F4 (parser respuesta directa),
  F5 (evaluaciones nivel/final), F6 (PDF), F7 (gate + piloto). Todo ya mergeado a `main`.
- **Método:** lectura del código real en `main`, mapa completo del flag
  `structured_bank_enabled`/`structured_bank_editable` (alumno vs admin), revisión de los
  ensambladores, sesiones/timers, dominio, parser y la activación.

## Resultado general

Las fases F1–F6 (auditadas en su momento por varias IAs) están **sólidas**: no se encontraron
errores nuevos. Los hallazgos se concentran en **F7**, que construyó 🏛️ Claude y solo había pasado
por una auditoría. Todos son de severidad **Media/Baja** y **no afectan datos** (la activación sigue
siendo reversible y el aislamiento de alumno se mantiene).

## Hallazgos

### F7-A · Media · `merge_items` no funciona en staging
`apps/content/views/item_review.py` (`merge_items`) valida `topic.structured_bank_enabled` en vez de
`structured_bank_editable`. Al pasar el resto de los guards admin a `editable` (Fase 7), este quedó
inconsistente: **fusionar ítems durante la preparación (staging) devuelve 400**, aunque el resto del
panel sí opera. **Fix:** usar `structured_bank_editable`.

### F7-B · Media · `edit_practice_quota` no funciona en staging
Mismo patrón en `edit_practice_quota` (misma vista): valida `structured_bank_enabled`. **Editar la
cuota de práctica durante la preparación devuelve 400.** **Fix:** `structured_bank_editable`.

### F7-C · Media · No se puede poner un tema legacy en preparación desde la UI
El selector de temas de `item_extraction.html` lista **solo temas editables** (`enabled OR staging`).
Un tema legacy (enabled=False, staging=False) — el candidato natural a piloto — **no aparece en el
selector**, así que no hay forma de seleccionarlo para marcarlo en staging: la preparación no puede
ni empezar desde la interfaz (huevo-y-gallina nuevo). Las vistas backend (`set_staging`,
`activation_panel`) ya aceptan cualquier tema activo; falta exponerlo en la UI. **Fix:** selector
propio en la sección de activación que lista **todos los temas activos**, independiente del selector
de ítems.

### F7-E · Media · `redirect` no importado en `item_review.py` (bug latente, pre-existente)
`edit_practice_quota` (línea 598) y `generate_visible_bank_drafts_view` (línea 692) terminan su rama
**no-HTMX** con `return redirect("content:item_extraction")`, pero `redirect` **no está importado**
(`from django.shortcuts import render, get_object_or_404`). En uso normal HTMX siempre manda
`HX-Request`, así que la rama nunca se ejecuta y el bug estaba **dormido**; pero una llamada sin ese
header da `NameError` (HTTP 500). Detectado por un test nuevo de F7-B. **Fix:** importar `redirect`.

### F7-D · Baja · El gate cuenta banco visible sin filtrar por la guía publicada
`activation_gate_service._published_count(scope="banco_visible")` no filtra por `learning_guide`,
mientras que la vista del alumno (`learning_guide_detail`) exige `learning_guide=<guía pública>`. Si
hubiera preguntas visibles publicadas ligadas a una guía anterior, el gate podría contarlas como
cobertura aunque el alumno no las vea. En la práctica la generación siempre liga la guía vigente, pero
conviene endurecer el conteo para que coincida con lo que realmente ve el alumno. **Fix:** filtrar el
conteo de `banco_visible` por la guía pública del tema.

## Observaciones (no se corrigen; decisiones de diseño / no bugs)

- **Una sola sesión `en_curso` por `(user,topic,kind,level)`** bloquea iniciar en paralelo otra
  evaluación de un 2.º recurso del mismo nivel (regla "termina la actual primero"). Es intencional.
- **El gate corre el dry-run de los ensambladores en cada carga del panel** (GET por tema). Es
  admin-only y acotado por `MAX_ASSEMBLY_STATES`; aceptable.
- **El gate usa el usuario que lo invoca** para el dry-run de no-repetición; como el admin no tiene
  sesiones del tema, es equivalente a usar el pool completo. Las verificaciones de reserva
  (`intentos × cuota`) son independientes del usuario y son la garantía real.
- **F6: `@media print { form { display:none } }`** es amplio pero inocuo (todas las forms del detalle
  son interactivas y `no-print`).

## Correcciones aplicadas (rama `fix/guias-fase7-auditoria`)

Los 5 hallazgos quedaron corregidos con tests:
- **F7-A/B:** `merge_items` y `edit_practice_quota` → `structured_bank_editable`.
- **F7-C:** selector propio en la sección de activación (`activation_topics` = todos los temas activos)
  + `activation_panel` acepta `activation_topic_id`. Ahora un tema legacy puede entrar a staging.
- **F7-E:** `from django.shortcuts import ... redirect` en `item_review.py`.
- **F7-D:** el conteo de `banco_visible` del gate filtra por la guía pública.
- **Tests:** `test_activation_gate` pasa de 9 a 13 (merge en staging, cuota en staging, legacy→staging,
  conteo por guía). Sin migraciones nuevas. `test_item_extraction.test_flag_disabled_blocks_panel_and_mutations`
  se ajustó al nuevo comportamiento de F7-C (el tema legacy ya no es editable, pero sí se ofrece en el
  selector de activación) — se verifica contra los contextos `topics`/`activation_topics`.
- **Barrera:** suite completa local (524 tests) verde tras la corrección; el único fallo era ese test
  desactualizado. Sin migraciones.

## Confirmaciones (revisado, sin cambios)

- **Timers F5 100% server-side**; `expires_at` calculado en servidor; el template entrega el deadline
  ISO (`date:'c'`) que el timer parsea correctamente; finalize idempotente con `select_for_update`.
- **Aislamiento del flag:** todas las vistas de alumno siguen exigiendo `structured_bank_enabled`
  (learning_guide_student, structured_evaluation, topic/resource_detail, select_visible_practice).
  Solo los paths admin usan `editable` (salvo los dos guards F7-A/B, ahora corregidos).
- **Parser F4** sin ejecución de código + tope de grado total (anti-DoS) intacto.
- **Dominio F5** 60/40 por último intento, sin N+1 (Prefetch), aislado del progreso legacy.
