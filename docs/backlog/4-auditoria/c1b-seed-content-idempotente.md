# C1b — seed_content idempotente (toda la taxonomía)

- **Estado:** Done (lista para auditar)
- **Implementado por:** 🔨 Antigravity (2026-06-02)
- **Creado:** 2026-06-02
- **Prioridad:** P1 · **Cartera:** continuidad operacional
- **Tipo:** infraestructura / datos
- **Dueño sugerido:** 🔨 Antigravity → 🧩 Codex → 🏛️ Claude

## Objetivo (una frase)
Aplicar a `seed_content.py` el mismo criterio idempotente que C1 aplicó a `seed_math_resources`,
para que tampoco pise contenido curado por staff.

## Contexto / diagnóstico (anclado en código real)
`apps/content/views/api_video.py` usa `django.core.cache` (líneas ~36-52) para contar intentos.
`apps/content/management/commands/seed_content.py` usa `update_or_create` para **toda** la
taxonomía, no solo recursos:
- Area (L312), Level (L324), Subject (L337), Topic (L349), **Resource (L368)**, Module (L394),
  ModuleResource (L407). Además `resource.levels.set(...)` (L380) y `module.levels.set(...)` (L406)
  se ejecutan siempre.
- **No** está en el start command (no corre en cada deploy) → no es P0, pero al correrse a mano
  pisa todo. Por eso C1 lo dejó **fuera** de su PR: aquí se hace completo y consistente.

## Alcance (lo que SÍ entra)
1. Reemplazar `update_or_create` → `get_or_create` en **todas** las entidades (Area, Level, Subject,
   Topic, Resource, Module, ModuleResource).
2. `levels.set(...)` (resource y module) **solo al crear**.
3. Flag `--refrescar-seo` que, solo si se pasa, actualice `description`/`content` de recursos
   existentes (mismo criterio que C1; **no** tocar `is_published`/`title`/`order`).
4. Mantener el orden de construcción de los diccionarios (`area_by_name`, `subject_by_name`,
   `topic_by_subject`, `resource_by_title`) — `get_or_create` igual devuelve el objeto.

## Fuera de alcance
- Cambiar `seed_resources.json` ni el modelo (sin migraciones).

## Criterios de aceptación
- [x] Barrera verde (`test` · `check` · `makemigrations --check`).
- [x] Test en `SeedContentCommandTests`: re-correr no pisa un recurso/subject/topic editado a mano.
- [x] Test: `--refrescar-seo` actualiza `description`/`content` pero **no** `is_published`.
- [x] Test extra (sugerido por Codex): re-correr **preserva los `levels`** asignados a mano.
- [x] El test idempotente existente (`test_seed_content_command_is_idempotent`) sigue verde.

## Riesgos / rollback
- Riesgo bajo (comando manual). Rollback: revertir el PR.

## Qué se hizo (Implementación)
- Reemplazados todos los `update_or_create` por `get_or_create` en `seed_content.py` para todas las entidades (Area, Level, Subject, Topic, Resource, Module, ModuleResource).
- Modificado para que la asignación de `levels` en `Resource` y `Module` ocurra únicamente al crear el registro.
- Implementado el flag `--refrescar-seo` para permitir la actualización selectiva de `description` y `content` de recursos existentes sin tocar otros campos.
- Añadidos tests unitarios exhaustivos en `apps/content/tests/test_management_commands.py` (`SeedContentCommandTests`) para validar que no se pise el contenido, que `--refrescar-seo` actúe de forma selectiva y que se preserven los niveles asignados a mano.

## Checklist 🧩 Codex
- [ ] Cobertura del no-clobber para todas las entidades, no solo Resource. Label `audit:aprobado` si ok.

## Checklist 🏛️ Claude (cierre)
- [ ] `matriz-riesgos.md` sin cambios (C1b es hardening, no un riesgo P0 abierto).
