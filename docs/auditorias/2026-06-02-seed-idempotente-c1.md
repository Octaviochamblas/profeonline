# Auditoría C1 - Seed idempotente y prevención de sobrescritura

- **Fecha:** 2026-06-02
- **Autor/agente:** Codex
- **Alcance:** rama `fix/seed-idempotente`, comando `seed_math_resources`, arranque Railway,
  tests asociados y documentación operacional relacionada.
- **Estado:** vigente
- **Base auditada:** diff `main...HEAD` y tarjeta `docs/backlog/4-auditoria/c1-seed-idempotente.md`.

## 1. Resumen ejecutivo

La implementación de Antigravity resuelve el riesgo principal de C1: `seed_math_resources` ya no
sobrescribe recursos existentes en cada corrida normal y ya no se ejecuta desde `Procfile` ni
`nixpacks.toml` en cada arranque de Railway.

La estrategia técnica es correcta: cambiar `update_or_create` por `get_or_create`, asignar
`levels` solo cuando se crea el recurso, y dejar cualquier refresco de SEO detrás de un flag
explícito (`--refrescar-seo`). Los tests nuevos cubren el caso central de staff editando un recurso
despublicado y el comportamiento selectivo del flag.

Mi dictamen: **aprobable con una corrección de alcance antes del merge** y con varios cierres
preventivos de documentación/runbook para que el riesgo no reaparezca por otra puerta.

## 2. Evidencia revisada

### Archivos funcionales

- `apps/content/management/commands/seed_math_resources.py`
- `apps/content/tests/test_management_commands.py`
- `Procfile`
- `nixpacks.toml`

### Archivos de proceso/documentación

- `docs/backlog/4-auditoria/c1-seed-idempotente.md`
- `docs/_coordinacion/ESTADO.md`
- `docs/README.md`
- `docs/gobernanza/inventario-operacional.md`
- `docs/gobernanza/matriz-riesgos.md`
- `docs/gobernanza/roadmap-priorizado.md`
- `.claude/settings.local.json`
- `build.sh`

### Comandos ejecutados por Codex

```powershell
.venv\Scripts\python.exe manage.py test apps.content.tests.test_management_commands.SeedMathResourcesCommandTests --verbosity 1
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Resultado local:

- `SeedMathResourcesCommandTests`: 2 tests OK.
- `manage.py check`: sin issues.
- `makemigrations --check --dry-run`: sin cambios detectados.

No ejecuté la suite completa en esta auditoría para respetar economía de tokens/tiempo. Antigravity
reportó suite completa verde (`167 tests OK`); esta auditoría revalidó el núcleo tocado.

## 3. Qué quedó bien implementado

### 3.1. No sobrescritura de recursos existentes

Antes:

```python
Resource.objects.update_or_create(slug=slug, defaults={...})
```

Eso reescribía `title`, `description`, `content`, `is_published`, `order`, `subject`, `topic` y
`video_url` cada vez que el comando corría.

Ahora:

```python
Resource.objects.get_or_create(slug=slug, defaults={...})
```

Eso conserva el recurso existente y solo aplica `defaults` al crearlo. Es exactamente el cambio
necesario para proteger ediciones manuales del staff.

### 3.2. `levels` ya no se resetea en cada corrida

El patrón quedó como corresponde:

```python
if created:
    resource.levels.set([level])
```

Esto evita que una futura asignación manual de niveles sea reemplazada por el seed durante una
corrida normal.

### 3.3. Refresco SEO explícito y acotado

El flag `--refrescar-seo` actualiza solo:

- `description`
- `content`

No toca:

- `title`
- `is_published`
- `order`
- `levels`
- `subject`
- `topic`
- `video_url`

Para el objetivo C1, esta separación es buena: el comportamiento destructivo deja de ser implícito
y pasa a ser una operación deliberada.

### 3.4. El seed salió del arranque principal

Se removió de:

- `Procfile`
- `nixpacks.toml`

El arranque queda en:

```text
migrate && ensure_admin && ensure_site && gunicorn
```

Esto reduce mucho el riesgo operacional. Aunque el comando tuviera un bug futuro, ya no se ejecuta
en cada boot/redeploy de producción.

### 3.5. Tests nuevos relevantes

Los tests agregados validan:

- Correr el seed dos veces no pisa `is_published=False`, `content`, `title` ni `order`.
- Con `--refrescar-seo`, se actualizan `description` y `content`, pero no `is_published`, `title`
  ni `order`.

El test captura el bug principal que motivó C1.

## 4. Hallazgos

### P1 - Bloqueante de alcance: `.claude/settings.local.json` cambió en el PR

El diff del PR incluye cambios en `.claude/settings.local.json`. Esto no pertenece al alcance C1
y además amplía permisos/comandos locales, incluyendo patrones como `git restore *`, `gh api *`,
`gh workflow *` y comandos contra producción.

Riesgo:

- El PR deja de ser un cambio acotado de infraestructura/datos.
- Se mezclan cambios funcionales con configuración local de agente.
- Comandos permisivos en un archivo trackeado pueden normalizar acciones peligrosas para futuras
  sesiones.

Recomendación antes del merge:

- Sacar `.claude/settings.local.json` del PR, salvo que exista una decisión explícita de gobernanza
  para versionar esos permisos.
- Si se quiere mantener ese cambio, separarlo en otro PR de automatización/seguridad con revisión
  propia.

Estado:

- **Requiere acción antes de aprobar `audit:aprobado`.**

### P1 - `build.sh` todavía ejecuta `seed_math_resources`

`build.sh` sigue incluyendo:

```bash
python manage.py seed_math_resources
```

No encontré referencias a `build.sh` desde `Procfile`, `nixpacks.toml`, `.github/` ni `docs/`.
Con la configuración actual de Nixpacks, parece no ser el camino principal de Railway. Aun así,
es un archivo trackeado y operacionalmente sensible.

Riesgo:

- Si alguien usa `build.sh` como deploy/manual bootstrap, el seed seguirá ejecutándose como parte
  de un flujo automático.
- El repo mantiene dos verdades: `Procfile`/`nixpacks.toml` dicen "no seed en boot", pero
  `build.sh` conserva el patrón antiguo.

Recomendación:

- Decidir explícitamente si `build.sh` se retira, se actualiza o se documenta como script manual.
- Mi preferencia: quitar `python manage.py seed_math_resources` de `build.sh` y dejar un comentario
  apuntando a una ejecución manual bajo demanda:

```bash
# Para poblar recursos matemáticos en una DB nueva:
# python manage.py seed_math_resources
```

Estado:

- **No invalida la lógica del PR**, pero sí debería corregirse antes del cierre de C1 para que la
  mitigación sea completa.

### P1 - Documentación operacional aún describe el arranque antiguo

Siguen referencias vivas a `seed_math_resources` como parte del arranque en:

- `docs/README.md`
- `docs/gobernanza/inventario-operacional.md`
- `docs/gobernanza/matriz-riesgos.md`
- `docs/gobernanza/roadmap-priorizado.md`

Riesgo:

- Futuros agentes pueden volver a razonar como si el seed siguiera corriendo en cada deploy.
- La matriz de riesgos no reflejará que C1 pasó de "activo crítico" a "mitigado parcialmente".
- La documentación podría inducir a reintroducir el seed en el start command.

Recomendación:

- Actualizar el snapshot de deploy en `docs/README.md`.
- Actualizar `inventario-operacional.md` con el nuevo arranque y un runbook de seed manual.
- Actualizar `matriz-riesgos.md`: C1 debe quedar como **mitigado parcialmente** hasta resolver
  `build.sh`, runbook y pruebas de no regresión.
- Actualizar `roadmap-priorizado.md` para marcar C1 como "en auditoría/cierre", no pendiente.

Estado:

- **Debe cerrarse antes de que Claude marque C1 como completado.**

### P2 - La clave de idempotencia sigue siendo el `slug` derivado del título

El comando usa:

```python
slug = slugify(title)
Resource.objects.get_or_create(slug=slug, defaults={...})
```

Esto protege contra reruns idénticos, pero no contra cambios futuros de título en la lista
`videos`. Si alguien corrige un typo del título o renumera una clase, el slug cambia y el comando
creará otro recurso en vez de reconocer el existente por video.

Riesgo:

- Duplicación silenciosa si se cambia un título de `videos`.
- El recurso antiguo conserva progreso, vistas, quizzes y relaciones; el nuevo parte vacío.
- La corrección editorial de un título se vuelve una operación de datos peligrosa.

Recomendación preventiva:

- Introducir una clave estable de origen. Opciones:

| Opción | Pros | Contras |
| --- | --- | --- |
| Buscar primero por `video_url` y luego por `slug` | Sin migración, bajo costo | `video_url` no es único a nivel DB |
| Agregar campo `external_video_id`/`youtube_id` único | Modelo correcto a largo plazo | Requiere migración |
| Mantener un `seed_key` explícito | Robusto para cualquier fuente | Requiere diseño adicional |

Recomendación práctica:

- Para C1 actual no bloquearía por esto, porque el problema ya existía antes.
- Crear una tarjeta posterior: **C1b - clave estable para seeds de recursos**.

### P2 - `--refrescar-seo` actualiza los 27 recursos existentes sin selector ni vista previa

El flag está bien como mecanismo explícito, pero su radio de acción es amplio: refresca todos los
recursos del comando.

Riesgo:

- Una corrida accidental con `--refrescar-seo` reemplaza contenido curado de todos los recursos.
- El nombre del flag deja claro que actualiza SEO, pero no exige confirmación ni permite auditar
  antes qué cambiará.

Recomendación preventiva:

- Añadir en el futuro:
  - `--dry-run`: mostrar qué recursos se crearían/actualizarían.
  - `--video-id <id>` o `--slug <slug>`: refrescar un recurso puntual.
  - `--solo-publicados`: evitar tocar recursos despublicados si esa regla de producto se decide.

No lo bloquearía ahora, porque el flag ya es mucho más seguro que el comportamiento anterior.

### P2 - El test no cubre explícitamente que `levels` modificados a mano se preservan

El código sí preserva niveles en recursos existentes, pero el test principal no lo afirma. Dado que
`resource.levels.set([level])` fue uno de los riesgos originales, conviene dejarlo cubierto.

Riesgo:

- Una regresión futura podría volver a ejecutar `levels.set(...)` fuera del bloque `created` y los
  tests actuales no necesariamente fallarían.

Recomendación:

- Agregar un nivel adicional en el test, asignarlo manualmente al recurso, rerun sin flags y afirmar
  que la relación M2M queda intacta.

Estado:

- No bloqueante, pero recomendado antes de cierre si se quiere una barrera más fuerte.

### P2 - El comando todavía muta taxonomía al renombrar/fusionar asignaturas

El bloque que renombra `Matemáticas Escolar` a `Matemática Escolar` sigue activo. Si existe la
asignatura antigua, el comando mueve `Topic` y `Resource` hacia la nueva y borra/fusiona la antigua.

Riesgo:

- Es una mutación de datos más amplia que "crear recursos si no existen".
- Si alguien reutilizó intencionalmente la asignatura antigua, el seed puede reorganizar contenido.

Contexto:

- Es comportamiento preexistente.
- Al sacar el seed del arranque, el riesgo baja mucho.

Recomendación:

- Convertir ese rename en una migración de datos histórica ya ejecutada, o documentarlo como
  normalización puntual.
- A futuro, los comandos seed deberían evitar operaciones correctivas de taxonomía salvo que tengan
  flag explícito.

## 5. Riesgos futuros y prevención

### Riesgo A - Reintroducir seeds en arranque

Prevención:

- Agregar un test/check de texto en CI o pre-commit que falle si `Procfile` o `nixpacks.toml`
  vuelven a contener `seed_math_resources`.
- Documentar en `inventario-operacional.md`: "Los seeds se ejecutan manualmente, no en boot".

### Riesgo B - Ejecutar un seed destructivo desde otro script

Prevención:

- Auditar `build.sh`, scripts de bootstrap y docs.
- Mantener una lista canónica de comandos permitidos en deploy.

### Riesgo C - Duplicar recursos al cambiar títulos

Prevención:

- Diseñar clave estable (`youtube_id` o equivalente).
- Añadir tests: cambiar título en fixture simulado no debe crear duplicado.

### Riesgo D - Refresco SEO masivo accidental

Prevención:

- `--dry-run` por defecto para operaciones de actualización.
- Selectores por video/slug.
- Mensaje de salida que liste recursos actualizados, no solo conteo.

### Riesgo E - Confundir "idempotente" con "no toca nada"

Prevención:

- Documentar semántica exacta:
  - Sin flags: crea faltantes, no cambia existentes.
  - Con `--refrescar-seo`: cambia `description` y `content`.
  - No forma parte del arranque.

### Riesgo F - Mezclar configuración local de agente con cambios de producto

Prevención:

- No incluir `.claude/settings.local.json` en PRs funcionales.
- Si debe versionarse, tratarlo como cambio de gobernanza con revisión separada.

## 6. Recomendaciones antes de mergear

1. Sacar `.claude/settings.local.json` del PR o moverlo a un PR separado de gobernanza.
2. Alinear `build.sh`: retirar `seed_math_resources` o documentar formalmente que no se usa en
   deploy y que el seed es manual.
3. Actualizar documentación viva (`docs/README.md`, `inventario-operacional.md`,
   `matriz-riesgos.md`, `roadmap-priorizado.md`).
4. Opcional pero recomendable: agregar test de preservación de `levels`.

## 7. Recomendaciones para tarjetas futuras

### C1b - Clave estable para seeds de recursos

Objetivo:

- Evitar duplicados cuando cambian títulos/slugs.

Criterios sugeridos:

- El seed identifica recursos por `youtube_id`/`video_url` antes que por título.
- Cambiar un título en la fuente no crea un recurso duplicado.
- Si se decide actualizar título, debe requerir flag explícito.

### C1c - Runbook de seeds manuales

Objetivo:

- Definir cuándo y cómo ejecutar `seed_math_resources`.

Debe incluir:

- Entorno permitido.
- Backup previo si se usa `--refrescar-seo`.
- Comando exacto.
- Verificación posterior.
- Rollback.

### C1d - Guardrail CI contra seeds en boot

Objetivo:

- Prevenir regresión del start command.

Criterio:

- CI falla si `Procfile` o `nixpacks.toml` incluyen `seed_math_resources`.

## 8. Dictamen

La implementación cumple el objetivo técnico principal de C1 y mejora de forma importante la
seguridad operacional del deploy.

Dictamen Codex:

- **Código funcional:** aprobado.
- **Tests del núcleo:** aprobados, con recomendación de ampliar cobertura de `levels`.
- **Alcance del PR:** requiere retirar o justificar `.claude/settings.local.json`.
- **Cierre operacional:** requiere alinear `build.sh` y documentación viva antes de marcar C1 como
  completamente mitigado.

No pondría `audit:aprobado` todavía hasta resolver el cambio fuera de alcance en
`.claude/settings.local.json`. Una vez corregido eso, el PR queda en buen estado para que Claude
haga el cierre final y convierta los pendientes preventivos en tarjetas pequeñas.
