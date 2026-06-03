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

- **Sprint de producto (valor visible) arrancando (2026-06-02):** orden **Analytics → Home → QA a11y**;
  verificación-email intercalable; KaTeX condicional a que se escriban fórmulas. Handoffs en `backlog/2-arquitectura/`.
- **Decisión (2026-06-02, 🧑 Usuario):** **C1 y C2 descartados como trabajo activo** → riesgo
  **aceptado** mientras la base no tenga datos críticos (detalle en `../gobernanza/matriz-riesgos.md`).
- **Matriz P0:** C1 ⚪ aceptado · C2 ⚪ aceptado · C3 🟢 · A1 🟢 · **M5 (analítica) 🟡** (en arquitectura).
- **Infra viva (2026-06-02):** prod `www.profeonline.cl` 🟢 200 · staging
  `web-staging-production-0dfc.up.railway.app` 🟢 200.

## Bloqueos / esperando

- **C2** queda 🟡: hay backup real de prod + restore drill verificados (2026-06-02); para 🟢 falta
  **automatizar** el backup (plan Pro o cron externo) con retención.
- **C1** queda 🟡: `migrate` corre sin backup/gate previo. Ahora que existe backup probado, es el
  siguiente candidato (backup automático antes de migrar).

## Handoffs abiertos (Ready para construir)

- 🔨 **Analytics interno (M5)** — handoff listo en `backlog/2-arquitectura/mejora-analytics-eventos.md`.
  Panel propio sobre el ledger + eventos de cliente (clics WhatsApp/tel, video, adjuntos). **Ready para Antigravity.**
- Resto del sprint en `backlog/1-por-iniciar/` (Home, QA a11y, verificación-email, KaTeX); se redactan al iniciar cada uno.

## Últimas entregas
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **rumbo post-P0 definido.** C1/C2 **aceptados** como riesgo;
  sprint de valor visible (Analytics → Home → QA a11y). Handoff de **Analytics interno** redactado en `2-arquitectura`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **rotación de credenciales de prod** (la URL quedó expuesta en
  chat). Causó un 500 breve (web cacheaba la `DATABASE_URL` vieja); recuperado con redeploy. Staging
  se desincronizó por error y se revirtió. Procedimiento + lecciones en `runbook-backups.md §5`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **A1 → 🟢 staging operativo** en Railway (`Web-staging` +
  `Postgres-Staging` aislada, 200 en `/` y `/admin/`). 2 hallazgos resueltos (`DJANGO_USE_X_FORWARDED_PROTO`,
  `collectstatic`/Custom Start Command) → `runbook-staging.md §8`.
- 2026-06-02 — 🏛️ Claude + 🧑 Usuario: **C2 → backup real de prod + restore drill verificados**
  (`pg_dump` 18.4; runbook §4.B). Riesgo 🟡 (falta automatizar).
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
