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

- **Sprint P0 (continuidad operacional).** Tarjetas *Ready* en `backlog/2-arquitectura/`.
  Próximo movimiento: 🔨 Antigravity toma `c1-seed-idempotente.md` (🧩 Codex hace preflight antes).

## Bloqueos / esperando

- **C3 / C2 / A1** dependen de acciones del 🧑 Usuario en Railway (`REDIS_URL`, backups diarios,
  servicio staging con DB propia). El código de C1 y la parte de código de C3 **no** están bloqueados.

## Handoffs abiertos (Ready para construir)

- `backlog/2-arquitectura/c1-seed-idempotente.md` — 🔨 Antigravity (empezar por aquí)
- `backlog/2-arquitectura/c3-redis-rate-limit.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/c2-backups-restore-drill.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/a1-staging-preview.md` — 🧑 Usuario + 🔨 Antigravity

## Últimas entregas

- 2026-06-02 — 🔨 Antigravity: seed idempotente (C1) implementado en `fix/seed-idempotente`. Tests unitarios agregados (167 OK). Listo para que Codex audite.
- 2026-06-02 — 🏛️ Claude: handoffs P0 *Ready* + brief de arranque (`ARRANQUE-P0.md`). Listo para
  que Antigravity y Codex ejecuten.
- 2026-06-02 — 🏛️ Claude: automatización del flujo mergeada (PR #20): auto-merge + gate IA + CI +
  digest (Issue #22). Branch protection activa.
- 2026-06-01 — 🏛️ Claude: reestructuración de la documentación (PR #19).
