# Auditoría C1b - seed_content idempotente

- **Fecha:** 2026-06-02
- **Autor/agente:** Codex
- **Alcance:** rama `fix/seed-content-idempotente`, comando `seed_content`, tests asociados y
  tarjeta `docs/backlog/4-auditoria/c1b-seed-content-idempotente.md`.
- **Estado:** vigente
- **Base auditada:** diff `main...HEAD`.

## 1. Resumen ejecutivo

La implementación C1b aplica correctamente el criterio de C1 a `seed_content.py`: el comando deja
de usar `update_or_create`, pasa a `get_or_create`, y ya no pisa campos curados en ejecuciones
posteriores. También limita `levels.set(...)` a creación y agrega `--refrescar-seo` para actualizar
solo `description` y `content` de recursos existentes.

Dictamen: **código aprobable**. No encontré un hallazgo bloqueante para devolver el PR. Sí dejo dos
observaciones preventivas: el módulo "Ruta de fracciones y decimales" sigue dependiendo de un
fallback porque referencia un recurso que no existe con ese título exacto en el JSON, y la cobertura
de no-clobber es fuerte para recursos/subject/topic/levels, pero no comprueba explícitamente todos
los modelos de la taxonomía.

## 2. Evidencia revisada

### Archivos funcionales

- `apps/content/management/commands/seed_content.py`
- `apps/content/management/commands/seed_resources.json`
- `apps/content/tests/test_management_commands.py`
- `apps/content/models/module.py`
- `apps/content/models/module_resource.py`

### Archivos de proceso

- `docs/backlog/4-auditoria/c1b-seed-content-idempotente.md`
- `docs/_coordinacion/ESTADO.md`

### Comandos ejecutados por Codex

```powershell
.venv\Scripts\python.exe manage.py test apps.content.tests.test_management_commands.SeedContentCommandTests --verbosity 1
.venv\Scripts\python.exe manage.py test apps.content.tests.test_management_commands --verbosity 1
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
git diff --check main...HEAD
```

Resultado local:

- `SeedContentCommandTests`: 4 tests OK.
- `test_management_commands`: 7 tests OK.
- `manage.py check`: sin issues.
- `makemigrations --check --dry-run`: sin cambios detectados.
- `git diff --check main...HEAD`: sin problemas.

No ejecuté la suite completa porque Antigravity reportó `170 tests OK` y esta auditoría revalidó el
núcleo tocado más el archivo completo de management commands.

## 3. Qué quedó bien implementado

### 3.1. Se eliminó el patrón destructivo

El diff reemplaza `update_or_create` por `get_or_create` en:

- `Area`
- `Level`
- `Subject`
- `Topic`
- `Resource`
- `Module`
- `ModuleResource`

Esto evita que una ejecución manual de `seed_content` reescriba campos ya curados por staff.

### 3.2. Los niveles se preservan en reruns

Antes, el comando hacía `levels.set(...)` siempre. Ahora:

```python
if created:
    resource.levels.set([...])
```

y lo mismo para `Module`. Esto protege niveles asignados a mano.

### 3.3. `--refrescar-seo` queda acotado

El flag solo actualiza:

- `Resource.description`
- `Resource.content`

No toca:

- `title`
- `is_published`
- `order`
- `levels`
- `subject`
- `topic`
- relaciones de módulos

Esto coincide con el criterio de C1: refrescar SEO debe ser una acción explícita y limitada.

### 3.4. Tests relevantes

Los tests nuevos cubren:

- Rerun sin flags no pisa `Resource`, `Subject` ni `Topic` editados manualmente.
- `--refrescar-seo` restaura `description`/`content` sin tocar `title` ni `is_published`.
- Rerun sin flags preserva `levels` asignados manualmente en `Resource` y `Module`.
- El test existente de idempotencia sigue validando conteos principales.

## 4. Hallazgos

### Sin hallazgos bloqueantes

No encontré un bug que deba impedir el merge del PR #27.

### P2 preventivo - El módulo usa fallback porque referencia un título ausente en el JSON

El módulo `Ruta de fracciones y decimales` referencia:

```python
"resource": "Guía de fracciones y decimales"
```

Pero ese título no aparece en `seed_resources.json`. Por eso el comando no encuentra el recurso en
`resource_by_title` y cae en:

```python
fallback_resources = Resource.objects.filter(topic=...)
ref_resource = fallback_resources.first()
```

Este comportamiento ya existía antes del PR, así que no es una regresión de C1b. Aun así, es una
zona frágil: el módulo puede quedar asociado al "primer" recurso del tema, no necesariamente al
recurso pedagógicamente esperado.

Recomendación:

- Crear una tarjeta posterior para reemplazar la referencia por una clave estable (`slug`,
  `video_url` o `youtube_id`) o corregir el título del recurso referenciado.

### P2 preventivo - La cobertura no-clobber no comprueba explícitamente todos los modelos

La tarjeta pide cobertura del no-clobber "para todas las entidades". El test comprueba muy bien:

- `Resource`
- `Subject`
- `Topic`
- `Resource.levels`
- `Module.levels`

Pero no comprueba explícitamente:

- `Area`
- `Level`
- `Module` campos propios (`objective`, `description`, `order`, `is_published`)
- `ModuleResource` campos propios (`order`, `is_required`, `note`)

El código sí usa `get_or_create` para esas entidades, así que la lógica protege esos campos. No lo
bloquearía. Pero para una barrera de regresión más completa, conviene ampliar el test.

Recomendación:

- Agregar en una mejora posterior un test único que edite `Area`, `Level`, `Module` y
  `ModuleResource`, rerun sin flags, y confirme que no se pisan.

### P2 preventivo - La clave de idempotencia de `Resource` sigue siendo el slug derivado del título

Igual que en C1, los recursos se identifican por:

```python
resource_slug = slugify(item["title"])
Resource.objects.get_or_create(slug=resource_slug, ...)
```

Si en el futuro cambia el título en `seed_resources.json`, el slug cambia y puede crearse un
duplicado en vez de reconocer el recurso anterior. Esto no lo introduce C1b, pero sigue siendo una
deuda común de seeds.

Recomendación:

- Diseñar una clave estable para recursos importados (`youtube_id`, `video_url` único o `seed_key`).

## 5. Prevención de errores futuros

### Riesgo A - Alguien vuelve a usar `update_or_create` en seeds curables

Prevención:

- Documentar regla de seeds: por defecto `get_or_create`; actualizaciones solo con flags explícitos.
- Agregar tests de no-clobber cuando se toque cualquier comando seed.

### Riesgo B - Refresco SEO masivo accidental

Prevención:

- Agregar en el futuro `--dry-run` y selector por `--slug` o `--video-id`.
- Mantener `--refrescar-seo` fuera de start commands y runbooks automáticos.

### Riesgo C - Módulos apuntan a recursos por texto visible

Prevención:

- Usar claves estables para relaciones internas.
- Evitar depender de `title` si el staff puede editarlo.

### Riesgo D - Cerrar C1b sin documentar que es comando manual

Prevención:

- Dejar claro en runbooks que `seed_content` es manual y no debe formar parte del arranque de
  producción.

## 6. Checklist de cierre recomendado

Antes de marcar C1b cerrado:

- [ ] CI del PR #27 verde.
- [ ] `audit:aprobado` agregado por Codex si el PR remoto coincide con esta rama.
- [ ] Tarjeta movida a finalizados por el cierre.
- [ ] Reporte de sesión actualizado.
- [ ] Riesgos preventivos opcionales convertidos en tarjetas si se quiere endurecer más.

## 7. Dictamen

Dictamen Codex:

- **Código funcional:** aprobado.
- **Tests del núcleo:** aprobados.
- **Diff vs. tarjeta:** fiel.
- **Riesgo residual:** bajo y no bloqueante.

Yo daría `audit:aprobado` al PR #27 si CI está verde y el PR remoto contiene este mismo diff. Las
observaciones preventivas pueden vivir como hardening posterior; no justifican frenar el merge de
C1b.
