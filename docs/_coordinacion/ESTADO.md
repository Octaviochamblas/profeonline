# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| 🏛️ Claude | fix/seed-idempotente | 2026-06-02 (cierre) | 🔴 cerrando C1 |

<!-- Ejemplo: | 🔨 Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | 🔴 trabajando | -->

## En curso ahora

- **C1 en cierre** (🏛️ Claude): limpieza de PR `fix/seed-idempotente` (saca `settings.local.json`
  fuera de alcance, alinea `build.sh` + docs, integra auditoría de Codex) → PR + auto-merge.
- **Próximo:** C3 (parte de código: system check de cache) y `c1b` (seed_content idempotente).

## Bloqueos / esperando

- **C3 / C2 / A1** dependen de acciones del 🧑 Usuario en Railway (`REDIS_URL`, backups diarios,
  servicio staging con DB propia).

## Handoffs abiertos (Ready para construir)

- `backlog/2-arquitectura/c1b-seed-content-idempotente.md` — 🔨 Antigravity (sigue a C1)
- `backlog/2-arquitectura/c3-redis-rate-limit.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/c2-backups-restore-drill.md` — 🔨 Antigravity + 🧑 Usuario
- `backlog/2-arquitectura/a1-staging-preview.md` — 🧑 Usuario + 🔨 Antigravity

## Últimas entregas

- 2026-06-02 — 🏛️ Claude: cierre de C1 (seed idempotente) — saneado fuera-de-alcance + `build.sh`
  + docs alineadas; auditoría de Codex integrada. Tarjeta a `6-finalizados`.
- 2026-06-02 — 🧩 Codex: auditoría profunda C1 (`docs/auditorias/2026-06-02-seed-idempotente-c1.md`);
  detectó `settings.local.json` fuera de alcance, `build.sh` con el seed y docs desalineadas.
- 2026-06-02 — 🔨 Antigravity: seed idempotente (C1) en `fix/seed-idempotente` + tests (167 OK).
- 2026-06-02 — 🏛️ Claude: handoffs P0 *Ready* + `ARRANQUE-P0.md`.
- 2026-06-02 — 🏛️ Claude: automatización del flujo (PR #20): auto-merge + gate IA + CI + digest.
- 2026-06-01 — 🏛️ Claude: reestructuración de la documentación (PR #19).
