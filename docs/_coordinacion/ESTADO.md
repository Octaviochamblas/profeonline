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
- **Siguiente disponible:** `c1b` (seed_content idempotente) y la parte de código de C3
  (system check de cache). Ver `ARRANQUE-P0.md`.

## Bloqueos / esperando

- **C3 / C2 / A1** dependen de acciones del 🧑 Usuario en Railway (`REDIS_URL`, backups diarios,
  servicio staging con DB propia).

## Handoffs abiertos (Ready para construir)

- `backlog/2-arquitectura/c1b-seed-content-idempotente.md` — 🔨 Antigravity (sigue a C1)
- `backlog/2-arquitectura/c3-redis-rate-limit.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/c2-backups-restore-drill.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/a1-staging-preview.md` — 🧑 Usuario + 🔨 Antigravity

## Últimas entregas
- 2026-06-02 — 🔨 Antigravity: comandos de backup y restore (C2) implementados y documentados en `feat/backups-restore-drill`. Drill de restauración local exitoso. Listo para auditoría.
- 2026-06-02 — 🧩 Codex: auditoría C1b seed_content en
  `docs/auditorias/2026-06-02-seed-content-idempotente-c1b.md`. Código aprobable; sin hallazgos
  bloqueantes.
- 2026-06-02 — 🔨 Antigravity: seed_content idempotente (C1b) implementado en `fix/seed-content-idempotente`. Tests unitarios agregados (170 OK). Listo para que Codex audite.
- 2026-06-02 — 🔨 Antigravity: system check de cache (C3) implementado en `feat/redis-cache-check`. Tests unitarios agregados (170 OK). Listo para que Codex audite.
- 2026-06-02 — 🏛️🔨🧩 **C1 mergeado (PR #24)** por el flujo completo: Antigravity construyó,
  Codex auditó (detectó fuera-de-alcance + `build.sh` + docs), Claude cerró. Lock liberado.
- 2026-06-02 — 🏛️ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 — 🏛️ Claude: automatización del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 — 🏛️ Claude: reestructuración de la documentación (PR #19).
