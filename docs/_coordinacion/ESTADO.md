# 🟢 ESTADO VIVO — Coordinación de agentes

> Editar este archivo **antes** de tocar el working tree. Mantenerlo corto y al día.
> 🔒 Regla de oro: un solo agente escribe en una misma rama a la vez.
> Brief del sprint actual: [`ARRANQUE-P0.md`](ARRANQUE-P0.md).

## Lock del working tree

| Agente | Rama | Tomado (fecha/hora) | Estado |
| --- | --- | --- | --- |
| _libre_ | - | - | 🟢 sin lock |

<!-- Ejemplo: | 🔨 Antigravity | fix/seed-idempotente | 2026-06-02 10:15 | 🔴 trabajando | -->

## En curso ahora

- **M5 (Analítica) y Verificación de email CERRADAS 🟢 (2026-06-03):** mergeadas vía **PR #36** y **PR #38**
  (Antigravity construyó, Codex auditó, Claude cerró). Analítica interna + verificación obligatoria de email.
- **Sprint de producto:** **Analytics ✅ → Email ✅ → Home → QA a11y**; KaTeX condicional.
  **No hay tarea activa sin bloqueo:** lo siguiente (Home) depende de insumos del 🧑 (ver Bloqueos).
- **Matriz P0/clave:** C1 ⚪ aceptado · C2 ⚪ aceptado · C3 🟢 · A1 🟢 · **M5 🟢**.
- **Infra viva:** prod `www.profeonline.cl` 🟢 200 · staging `web-staging-production-0dfc.up.railway.app` 🟢 200.

## Bloqueos / esperando

- **Home** 🔴 bloqueado por **contenido** del 🧑 (foto/bio/credenciales + 2-3 testimonios) — el código no.
- **QA a11y** 🔴 bloqueado por Home mergeado (cubre también el home nuevo).
- **KaTeX** ⏸️ pendiente decisión del 🧑: ¿el contenido llevará fórmulas en notación?
- **C1/C2** ⚪ aceptados (no son bloqueo; reconsiderar al entrar datos reales).

## Handoffs abiertos (Ready para construir)

- _(ninguno Ready ahora)_ — Email ✅ cerrado (PR #38). Lo siguiente está **bloqueado por insumos del 🧑**:
  Home (contenido), QA a11y (Home mergeado), KaTeX (decisión de fórmulas). Tarjetas en `backlog/1-por-iniciar/`.

## Últimas entregas
- 2026-06-03 — 🏛️🔨🧩 **Verificación de email mergeada y CERRADA 🟢 (PR #38).** Antigravity construyó,
  Codex auditó (P1 duplicados, P2 anti-enumeración, P3 usuarios sin email), Antigravity corrigió, Claude
  cerró (sensible). 202 tests. `mandatory` + Google exento; migración no bloquea a usuarios actuales.
- 2026-06-03 — 🏛️🔨🧩 **M5 Analítica interna mergeada y CERRADA 🟢 (PR #36).** Antigravity construyó,
  Codex auditó y curó privacidad, Claude cerró como 3ª IA (superficie sensible). Suite 191 tests. Matriz M5 → 🟢.
- 2026-06-02 — 🧩 Codex: **cura privacidad M5 en PR #36** — metadata por allowlist de evento,
  `path` sin querystrings, JS sin `href`/texto/`file_url` sensible y regresiones de analitica. Lock liberado.
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
