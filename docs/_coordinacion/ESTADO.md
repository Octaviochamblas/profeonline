# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| _libre_ | — | — | 🟢 disponible |

<!-- Ejemplo: | 🔨 Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | 🔴 trabajando | -->

## En curso ahora

- **Sprint P0 cerrado:** C1, C1b, C2, C3, A1 y el Router del flujo están **mergeados** y sus tarjetas
  en `6-finalizados`. Backlog de construcción/auditoría vacío.
- **Matriz de riesgos:** C1 🟡 · C3 🟢 · C2 🟡 · A1 🟡 (las 🟡 esperan solo acción del 🧑 Usuario en Railway).

## Bloqueos / esperando

- **C2 y A1** quedan 🟡 a la espera de acciones del 🧑 Usuario en Railway:
  - **C2:** activar backups automáticos del proveedor + ejecutar un restore desde backup real → 🟢.
  - **A1:** crear el servicio staging web + DB PostgreSQL propia; validar 200 con DB separada → 🟢.

## Handoffs abiertos (Ready para construir)

- _(ninguno)_ — backlog de ideas en `backlog/1-por-iniciar/` disponible para el próximo sprint.

## Últimas entregas
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
