# Matriz de riesgos técnicos

> Documento **canónico** (Capa 1). Riesgos detectados en la auditoría maestra, condensados con
> mitigación, dueño y estado. Detalle y evidencia en
> [`_fuentes/auditoria-maestra-claude-2026-06-01.md`](_fuentes/auditoria-maestra-claude-2026-06-01.md).
> Última revisión: 2026-06-01.

**Leyenda estado:** 🔴 abierto · 🟡 en curso · 🟢 mitigado. Mantener al día al cerrar cada riesgo.

## 🔴 Críticos (P0)

| ID | Riesgo | Impacto | Mitigación | Dueño | Estado |
| --- | --- | --- | --- | --- | --- |
| **C1** | `migrate` + `seed_math_resources` corren en **cada arranque** sin gate ni backup previo | Migración mala se aplica sola; seed puede pisar contenido curado | Verificar idempotencia del seed (`get_or_create`/`update_or_create`); gate de migraciones + backup previo; documentar rollback | 🏛️+🔨 | 🔴 |
| **C2** | Sin backup verificado / sin drill de restauración | Pérdida de contenido y progreso de alumnos | Confirmar backup diario en DB gestionada + **probar restore** + documentar | 🧑+🏛️ | 🔴 |
| **C3** | Rate-limit del webhook es **por-worker** si no hay Redis (`base.py` no define `CACHES` → `LocMemCache`) | Límite efectivo = 10 × nº workers; se pierde en cada redeploy | Definir `REDIS_URL` en prod y documentarlo como requisito del webhook | 🧑 | 🔴 |

## 🟠 Altos (P1)

| ID | Riesgo | Impacto | Mitigación | Dueño | Estado |
| --- | --- | --- | --- | --- | --- |
| **A1** | No hay staging; se audita/QA contra producción | Riesgo de romper prod; QA tardío | Servicio `staging` o preview deploys por PR | 🧑+🏛️ | 🔴 |
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
| **M5** | Observabilidad parcial (Sentry sin tracing; sin métricas de negocio) | Dashboard interno con `XPEvent`/`QuizAttempt` | 🔴 |
| **M6** | `requirements.txt` pinneado sin hashes | Lockfile con hashes (endurecer cadena de suministro) | 🔴 |

## Cómo se usa esta matriz

- Cada riesgo **abierto** con prioridad P0/P1 debería tener una **tarjeta** en
  [`../backlog/1-por-iniciar/`](../backlog/1-por-iniciar/).
- Al mitigar un riesgo, actualizar su estado aquí y enlazar la tarjeta/PR que lo cerró.
- Revisión recomendada: **trimestral**, o tras cualquier cambio grande de infraestructura.
