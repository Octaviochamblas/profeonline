# 🚀 Arranque — Sprint P0 (continuidad operacional)

> Brief de kickoff para **Antigravity** y **Codex**. Léelo una vez al empezar. Las reglas vivas
> están en `docs/gobernanza/proceso-multiagente.md` y la automatización en
> `docs/gobernanza/automatizacion-flujo.md`.

## Meta del sprint
Cerrar los **P0 de continuidad operacional** antes de tocar features grandes de producto.
Tarjetas *Ready* en `docs/backlog/2-arquitectura/` (handoffs completos con criterios y pruebas):

| Orden | Tarjeta | Tipo | Quién construye | Depende de |
| --- | --- | --- | --- | --- |
| 1 | `c1-seed-idempotente.md` | código | 🔨 Antigravity | — (empezar por aquí) |
| 2 | `c3-redis-rate-limit.md` | código + Railway | 🔨 Antigravity + 🧑 Usuario | `REDIS_URL` (usuario) |
| 3 | `c2-backups-restore-drill.md` | comandos + runbook | 🔨 Antigravity + 🧑 Usuario | backups del provider (usuario) |
| 4 | `a1-staging-preview.md` | infra + doc | 🧑 Usuario + 🔨 Antigravity | servicio staging (usuario) |

## Cómo arranca cada uno (HOY)

### 🔨 Antigravity (constructor)
1. Lee `docs/README.md` → `docs/gobernanza/proceso-multiagente.md` → la tarjeta `c1-seed-idempotente.md`.
2. **Toma el lock**: edita `docs/_coordinacion/ESTADO.md` (tu nombre + rama + hora) y mueve la
   tarjeta con `git mv` de `2-arquitectura/` a `3-construccion/`.
3. Crea rama `fix/seed-idempotente`, implementa **exactamente el alcance** de la tarjeta (nada de más).
4. Deja la barrera verde: `test` · `check` · `makemigrations --check --dry-run`.
5. Abre PR a `main` usando la plantilla. **No mergees**: el sistema auto-mergea cuando CI esté
   verde **y** Codex ponga `audit:aprobado`. Mueve la tarjeta a `4-auditoria/` y libera el lock.
6. Sigue con C3, luego C2 (sus partes de código).
   > Si tienes **sub-agentes**, paraleliza solo en **ramas/worktrees distintos** (nunca el mismo árbol).

### 🧩 Codex (auditor)
1. **Preflight** (antes de que Antigravity construya): lee la tarjeta `c1` y contrástala con el
   código real (`seed_math_resources.py`); si hay un error de planteamiento, anótalo en
   `bitacora/AAAA-MM-DD.md`. Si todo cuadra, da luz verde en la bitácora.
2. **Auditoría** (cuando haya PR): corre la suite, revisa N+1/migraciones/diff vs. tarjeta y el
   **checklist 🧩 Codex** de la tarjeta. Si pasa → añade el label **`audit:aprobado`** al PR
   (eso habilita el auto-merge). Si no → comenta los hallazgos y la tarjeta vuelve a `3-construccion/`.

### 🏛️ Claude (arquitecto + cierre)
- Firma seguridad en PRs con `seguridad:requiere-claude`, hace el cierre y actualiza
  `matriz-riesgos.md` (C1/C3/C2/A1 → 🟢) y los reportes de sesión.

## 🧑 Acciones del usuario (en paralelo, desbloquean P0)
- **Redis (C3):** crear servicio Redis en Railway y definir `REDIS_URL`.
- **Backups (C2):** confirmar/activar backups diarios del provider.
- **Staging (A1):** crear servicio staging con **DB propia**.

## Reglas no negociables
- **Un solo agente escribe en una rama/árbol a la vez** (lock en `ESTADO.md`).
- **Solo `get_or_create`/cuidado con datos**: nada que pise contenido curado (es justo el P0).
- **El gate manda:** ningún código entra a `main` sin CI verde + `audit:aprobado` de **otra** IA.
- Mover tarjetas siempre con `git mv`.
