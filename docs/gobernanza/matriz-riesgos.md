# Matriz de riesgos técnicos

> Documento **canónico** (Capa 1). Riesgos detectados en la auditoría maestra, condensados con
> mitigación, dueño y estado. Detalle y evidencia en
> [`_fuentes/auditoria-maestra-claude-2026-06-01.md`](_fuentes/auditoria-maestra-claude-2026-06-01.md).
> Última revisión: 2026-06-02.

**Leyenda estado:** 🔴 abierto · 🟡 en curso · 🟢 mitigado · ⚪ aceptado (riesgo asumido, sin trabajo
activo por ahora). Mantener al día al cerrar cada riesgo.

## 🔴 Críticos (P0)

| ID | Riesgo | Impacto | Mitigación | Dueño | Estado |
| --- | --- | --- | --- | --- | --- |
| **C1** | `migrate` corre en cada arranque sin gate/backup previo (el **seed** ya no pisa) | Migración mala se aplica sola | **Seed mitigado** (`get_or_create` + fuera del start command). Gate/backup pre-migrate **descartado como trabajo activo** (2026-06-02, 🧑 Usuario): riesgo **aceptado** mientras no haya datos críticos. **Reconsiderar** al entrar alumnos/contenido real. | 🔨+🏛️ | ⚪ |
| **C2** | Sin backup **automático**/retención (drill manual ya verificado) | Pérdida de contenido y progreso de alumnos | **Backup real de prod verificado** (2026-06-02): `pg_dump` 18.4 + restore drill OK (runbook §4.B). Automatizar (Pro/cron) **descartado como trabajo activo** (2026-06-02, 🧑 Usuario): riesgo **aceptado** mientras no haya datos críticos. | 🧑+🔨 | ⚪ |
| **C3** | Rate-limit del webhook es **por-worker** si no hay Redis (`base.py` no define `CACHES` → `LocMemCache`) | Límite efectivo = 10 × nº workers; se pierde en cada redeploy | **Mitigado:** `REDIS_URL` definido en Railway (2026-06-02) → cache/rate-limit compartido entre workers; `system check` (PR #26) avisa si alguna vez falta. | 🧑+🔨 | 🟢 |

## 🟠 Altos (P1)

| ID | Riesgo | Impacto | Mitigación | Dueño | Estado |
| --- | --- | --- | --- | --- | --- |
| **A1** | No hay staging; se audita/QA contra producción | Riesgo de romper prod; QA tardío | **Staging operativo (2026-06-02):** servicio `Web-staging` + `Postgres-Staging` aislada (host propio), 200 en `/` y `/admin/`, `check_environment` confirma entorno staging. Variables clave documentadas en runbook §8. | 🧑+🔨 | 🟢 |
| **A2** | Cobertura de tests sin medir | Regresiones silenciosas | `coverage` en CI + umbral mínimo | 🔨 | 🔴 |
| **A3** | Cero tests de frontend/JS (`enhanced-select.js`, HTMX del quiz) | Lo más frágil (a11y, estados) solo se valida a ojo | Smoke E2E con Playwright en CI | 🔨 | 🔴 |
| **A4** | Sin render LaTeX/KaTeX en sitio STEM | Techo en calidad pedagógica | Integrar KaTeX en `content` y explicaciones de `Question` | 🔨 | 🔴 |
| **A5** | Scaffolding no forzado (Nivel 3 sin aprobar Nivel 1) | Frustración / aprendizaje con vacíos | Bloquear Nivel N sin `passed` en N-1 (vista `quiz`) | 🔨 | 🔴 |
| **A6** | Conexiones DB / pooler al escalar (Supabase + `conn_max_age=600`) | Agotar conexiones al subir workers | Confirmar uso de pooler (pgbouncer) antes de escalar | 🏛️ | 🔴 |

## 🟡 Medios (P2)

| ID | Riesgo | Mitigación | Estado |
| --- | --- | --- | --- |
| **M1** | Sin sandbox de email → correos reales en pruebas | Modo prueba / dominio sandbox de Brevo | 🔴 |
| **M2** | Sin linter/formatter en CI | `ruff` en pre-commit y CI | 🔴 |
| **M3** | Sin tags de release / changelog | Tag por deploy atado al release de Sentry | 🔴 |
| **M4** | Branch protection no verificada | Exigir CI verde + review + no push directo a `main` | 🔴 |
| **M5** | Observabilidad parcial (Sentry sin tracing; sin métricas de negocio) | **Panel interno** sobre el ledger + eventos de cliente (clics, `page_view`, dashboard staff) — **PR #36** mergeado; tarjeta en `../backlog/6-finalizados/mejora-analytics-eventos.md` | 🟢 |
| **M6** | `requirements.txt` pinneado sin hashes | Lockfile con hashes (endurecer cadena de suministro) | 🔴 |

## Cómo se usa esta matriz

- Cada riesgo **abierto** con prioridad P0/P1 debería tener una **tarjeta** en
  [`../backlog/1-por-iniciar/`](../backlog/1-por-iniciar/).
- Al mitigar un riesgo, actualizar su estado aquí y enlazar la tarjeta/PR que lo cerró.
- Revisión recomendada: **trimestral**, o tras cualquier cambio grande de infraestructura.
