# C1 — Seed idempotente (no pisar contenido curado)

- **Estado:** Ready (handoff de arquitectura)
- **Creado:** 2026-06-02
- **Prioridad:** P0 · **Cartera:** continuidad operacional
- **Tipo:** infraestructura / datos
- **Dueño sugerido:** 🔨 Antigravity (build) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

## Objetivo (una frase)
Que `seed_math_resources` deje de **sobrescribir** recursos editados a mano, porque corre en **cada
arranque** de Railway y hoy pisa el contenido curado por staff.

## Contexto / diagnóstico (anclado en código real)
- `apps/content/management/commands/seed_math_resources.py`:
  - **Línea 319:** `Resource.objects.update_or_create(slug=slug, defaults={...})` → en cada corrida
    **reescribe** `title`, `description`, `content`, `is_published`, `order`, `subject`, `topic`,
    `video_url` de los 27 recursos. Si staff despublicó o editó uno, el siguiente deploy lo revierte.
  - **Línea 332:** `resource.levels.set([level])` → **resetea** los niveles asignados a mano.
- `Procfile` y `nixpacks.toml`: el *start command* incluye `... && seed_math_resources && gunicorn`,
  así que esto ocurre en **cada** boot/redeploy.

## Alcance (lo que SÍ entra)
1. Cambiar la siembra a **crear-si-no-existe** sin pisar lo existente:
   - Reemplazar `update_or_create` por `get_or_create(slug=slug, defaults={...})`.
   - `levels`: asignar **solo cuando el recurso se crea** (no en cada corrida).
2. Añadir flag explícito `--refrescar-seo` (o `--update`) que, **solo si se pasa**, actualice
   `description`/`content` de los recursos existentes (para refrescar SEO a propósito).
3. Sacar `seed_math_resources` del *start command* de cada boot:
   - Editar `Procfile` y `nixpacks.toml`: quitar `&& python manage.py seed_math_resources`.
   - (El usuario lo corre una vez a demanda, o se mueve a un release hook documentado.)
4. Replicar el mismo criterio en `seed_content.py` si tiene el mismo patrón (revisar).

## Fuera de alcance
- Reescribir las descripciones SEO. No tocar `videos`/`custom_details`.
- Cambiar el modelo `Resource` (sin migraciones).

## Archivos a tocar
| Archivo | Cambio |
| --- | --- |
| `apps/content/management/commands/seed_math_resources.py` | `get_or_create` + levels solo en creación + flag `--refrescar-seo` |
| `apps/content/management/commands/seed_content.py` | Mismo criterio si aplica (revisar antes) |
| `Procfile` · `nixpacks.toml` | Quitar `seed_math_resources` del start command |

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run` (sin migraciones nuevas).
- [ ] Test nuevo en `apps/content/tests/` que pruebe: correr el comando 2 veces **no** cambia un
      recurso cuyo `is_published` se puso en `False` ni su `content` editado (idempotencia real).
- [ ] Test: con `--refrescar-seo` sí se actualiza `description`/`content`.
- [ ] `git grep -n seed_math_resources Procfile nixpacks.toml` → ya **no** aparece en el start.
- [ ] Correr el comando local dos veces seguidas: la 2ª reporta `0 creados` y no altera datos.

## Plan de pruebas
1. `python manage.py seed_math_resources` (crea), editar a mano un recurso (`is_published=False`),
   volver a correr → el recurso sigue despublicado.
2. `python manage.py seed_math_resources --refrescar-seo` → actualiza SEO de los existentes.
3. Suite completa.

## Riesgos / rollback
- Riesgo: que el primer deploy tras el cambio ya no siembre (porque se sacó del boot). Mitigación:
  documentar que el usuario corra el seed una vez post-merge. Rollback: revertir el PR (1 commit).

## Checklist 🧩 Codex (auditoría)
- [ ] Diff = solo lo del alcance. Sin migraciones. Sin tocar SEO.
- [ ] `get_or_create` no reintroduce N+1 ni rompe el rename de asignatura (líneas 213-232).
- [ ] Los tests cubren el caso de borde (recurso despublicado/editado).
- [ ] Añadir label `audit:aprobado` si todo ok.

## Checklist 🏛️ Claude (cierre)
- [ ] Confirmar que el start command quedó sin el seed y documentarlo en `inventario-operacional.md`.
- [ ] Actualizar `matriz-riesgos.md`: C1 → 🟢 mitigado.
