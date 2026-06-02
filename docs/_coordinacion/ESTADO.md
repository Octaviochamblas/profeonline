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

- **C1 cerrado y mergeado** (PR #24): seed idempotente, fuera del start command, docs alineadas.
- **C3 cerrado y mitigado** (PR #26 + `REDIS_URL` en Railway 2026-06-02): rate-limit del webhook ya
  es compartido entre workers. Tarjeta en `6-finalizados`, matriz **🟢**.
- **C1b en cierre** (PR #27): `seed_content` idempotente, `audit:aprobado`; Claude resolvió el
  conflicto y lo deja para auto-merge. Ver `ARRANQUE-P0.md`.

## Bloqueos / esperando

- **C3 / C2 / A1** dependen de acciones del 🧑 Usuario en Railway (`REDIS_URL`, backups diarios,
  servicio staging con DB propia).

## Handoffs abiertos (Ready para construir)

- `backlog/2-arquitectura/c2-backups-restore-drill.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/4-auditoria/a1-staging-preview.md` — 🧑 Usuario + 🔨 Antigravity

## Últimas entregas
- 2026-06-02 — 🔨 Antigravity: comandos `backup_db`/`restore_db` (C2) + runbook en
  `feat/backups-restore-drill`; drill local exitoso. Auditado por 🏛️ Claude (`restore_db` con guardas
  anti-prod), en cierre.
- 2026-06-02 — 🔨 Antigravity + 🏛️ Claude: **C1b mergeado (PR #27)** — `seed_content` idempotente
  (auditado por Codex, conflicto resuelto y cerrado por Claude).
- 2026-06-02 — 🏛️ Claude: **C3 cerrado en 🟢** — código en `main` (PR #26) + `REDIS_URL` en Railway;
  tarjeta en `6-finalizados`, matriz 🟢 (PR #31).
- 2026-06-02 — 🏛️🔨🧩 **C1 mergeado (PR #24)** por el flujo completo: Antigravity construyó,
  Codex auditó (detectó fuera-de-alcance + `build.sh` + docs), Claude cerró. Lock liberado.
- 2026-06-02 — 🏛️ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 — 🏛️ Claude: automatización del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 — 🏛️ Claude: reestructuración de la documentación (PR #19).
